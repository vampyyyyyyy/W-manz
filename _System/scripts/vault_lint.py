#!/usr/bin/env python3
"""Vault linter for the Roblox Dev Knowledge Vault.

Enforces the note rules in AGENTS.md so humans, Claude and ChatGPT/Codex
can all write notes without breaking the graph:

  * every content note (folders 00_ .. 09_) has valid YAML frontmatter
  * every content note links to at least MIN_LINKS distinct notes
  * every [[WikiLink]] resolves to a real note (no ghost nodes)
  * no orphans: every content note has at least one backlink
  * no duplicate note names (Obsidian resolves links by file name)

Standard library only, so it runs anywhere Python 3.8+ exists (CI included).

Usage:
  python3 _System/scripts/vault_lint.py            # lint, exit 1 on errors
  python3 _System/scripts/vault_lint.py --stats    # also print graph stats
  python3 _System/scripts/vault_lint.py --weak     # list notes with few backlinks
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict

MIN_LINKS = 8
CONTENT_DIR_RE = re.compile(r"^\d\d_")
SKIP_DIRS = {".git", ".obsidian", ".github", ".trash", "node_modules"}
# Folders whose notes are not graph content (raw inputs, templates, tooling).
NON_CONTENT_DIRS = {"_Inbox", "_System"}
# Raw material: human drops and their archive. Never link targets, never
# checked, and a name clash with a real note is only a warning.
RAW_DIRS = {"_Inbox", os.path.join("_System", "Inbox_Archive")}
# Links inside these folders are not checked (templates use placeholders,
# inbox items are raw and get rewritten by the agent).
UNCHECKED_LINK_DIRS = RAW_DIRS | {os.path.join("_System", "Templates")}

ALLOWED_TYPES = {"concept", "api", "framework", "code-pattern", "forum-archive", "architecture", "moc"}
ALLOWED_STATUS = {"complete", "draft", "needs-verification", "stub"}
REQUIRED_KEYS = ("aliases", "tags", "type", "last_updated", "status")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

FENCE_RE = re.compile(r"^(\s*)(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
WIKILINK_RE = re.compile(r"!?\[\[([^\[\]\|#\n]+)(#[^\[\]\|\n]*)?(\|[^\[\]\n]*)?\]\]")


def parse_frontmatter(text: str):
    """Minimal YAML subset parser: scalars, inline lists, block lists."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing frontmatter (file must start with ---)"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "unterminated frontmatter (no closing ---)"
    data: dict = {}
    current_list_key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if stripped.startswith("- ") or stripped == "-":
            if current_list_key is None:
                return None, f"list item outside a key: {raw!r}"
            data[current_list_key].append(_unquote(stripped[1:].strip()))
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", stripped)
        if not m or raw.startswith(" "):
            return None, f"unparseable frontmatter line: {raw!r}"
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            data[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_unquote(v.strip()) for v in inner.split(",")] if inner else []
            current_list_key = None
        else:
            data[key] = _unquote(value)
            current_list_key = None
    return data, None


def _unquote(v: str) -> str:
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    return v


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code so Luau long strings like
    [[ ... ]] are never mistaken for WikiLinks."""
    out = []
    in_fence = False
    fence_token = ""
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if m:
            token = m.group(2)
            if not in_fence:
                in_fence, fence_token = True, token
                continue
            if token == fence_token:
                in_fence = False
                continue
        if in_fence:
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(out)


def body_without_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("\n---", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def collect_notes(root: str):
    notes = {}  # relpath -> abspath
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                abspath = os.path.join(dirpath, fn)
                notes[os.path.relpath(abspath, root)] = abspath
    return notes


def top_dir(rel: str) -> str:
    return rel.split(os.sep, 1)[0] if os.sep in rel else ""


def is_content(rel: str) -> bool:
    return bool(CONTENT_DIR_RE.match(top_dir(rel)))


def links_unchecked(rel: str) -> bool:
    return any(rel.startswith(d + os.sep) for d in UNCHECKED_LINK_DIRS)


def is_raw(rel: str) -> bool:
    return any(rel.startswith(d + os.sep) for d in RAW_DIRS)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    ap.add_argument("--stats", action="store_true", help="print graph statistics")
    ap.add_argument("--weak", action="store_true", help="list content notes with fewer than 3 backlinks")
    ap.add_argument("--min-links", type=int, default=MIN_LINKS)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    notes = collect_notes(root)
    errors: list[str] = []
    warnings: list[str] = []

    # name index (Obsidian resolves [[Name]] by file name, case-insensitively)
    by_name: dict[str, list[str]] = defaultdict(list)
    for rel in notes:
        if not is_raw(rel):
            by_name[os.path.splitext(os.path.basename(rel))[0].lower()].append(rel)
    for name, rels in by_name.items():
        if len(rels) > 1:
            errors.append(f"duplicate note name '{name}': {', '.join(rels)}")
    for rel in notes:
        name = os.path.splitext(os.path.basename(rel))[0].lower()
        if is_raw(rel) and name in by_name:
            warnings.append(f"{rel}: same name as {by_name[name][0]} (rename the raw note to avoid ambiguous links)")

    def resolve(target: str):
        target = target.strip()
        if target.lower().endswith(".md"):
            target = target[:-3]
        if "/" in target:
            suffix = target.replace("/", os.sep).lower() + ".md"
            hits = [r for r in notes if r.lower().endswith(suffix)]
            return hits[0] if hits else None
        hits = by_name.get(target.lower())
        return hits[0] if hits else None

    outgoing: dict[str, set] = {}
    incoming: dict[str, set] = defaultdict(set)

    for rel, abspath in notes.items():
        with open(abspath, encoding="utf-8") as fh:
            text = fh.read()
        content = is_content(rel)

        if content:
            fm, err = parse_frontmatter(text)
            if err:
                errors.append(f"{rel}: {err}")
            else:
                for key in REQUIRED_KEYS:
                    if key not in fm:
                        errors.append(f"{rel}: frontmatter missing '{key}'")
                tags = fm.get("tags", [])
                if not isinstance(tags, list) or "roblox-dev" not in tags:
                    errors.append(f"{rel}: tags must be a list that includes 'roblox-dev'")
                elif not any("/" in t for t in tags):
                    errors.append(f"{rel}: tags need at least one category/subcategory tag")
                if not isinstance(fm.get("aliases", []), list):
                    errors.append(f"{rel}: aliases must be a list")
                if fm.get("type") not in ALLOWED_TYPES:
                    errors.append(f"{rel}: type '{fm.get('type')}' not in {sorted(ALLOWED_TYPES)}")
                if fm.get("status") not in ALLOWED_STATUS:
                    errors.append(f"{rel}: status '{fm.get('status')}' not in {sorted(ALLOWED_STATUS)}")
                if not DATE_RE.match(str(fm.get("last_updated", ""))):
                    errors.append(f"{rel}: last_updated must be YYYY-MM-DD")
            if " " in os.path.basename(rel):
                warnings.append(f"{rel}: file name contains spaces (use Title_Case_Underscores)")

        if links_unchecked(rel):
            continue

        targets = set()
        for m in WIKILINK_RE.finditer(strip_code(body_without_frontmatter(text))):
            # inside tables Obsidian needs [[Note\|alias]], so drop the escaping backslash
            raw_target = m.group(1).rstrip("\\")
            hit = resolve(raw_target)
            if hit is None:
                errors.append(f"{rel}: unresolved link [[{raw_target.strip()}]]")
                continue
            if hit != rel:
                targets.add(hit)
        outgoing[rel] = targets
        for t in targets:
            incoming[t].add(rel)

    content_notes = [r for r in notes if is_content(r)]
    for rel in content_notes:
        n_out = len([t for t in outgoing.get(rel, ()) if is_content(t)])
        if n_out < args.min_links:
            errors.append(f"{rel}: only {n_out} distinct note links (minimum {args.min_links})")
        backlinks = {s for s in incoming.get(rel, ()) if is_content(s)}
        if not backlinks:
            errors.append(f"{rel}: orphan (no backlinks from other notes)")

    edges = sum(len([t for t in outgoing.get(r, ()) if is_content(t)]) for r in content_notes)
    reciprocal = sum(
        1 for r in content_notes for t in outgoing.get(r, ()) if is_content(t) and r in outgoing.get(t, ())
    )

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    print()
    print(f"Content notes : {len(content_notes)}")
    print(f"Links (edges) : {edges}")
    if content_notes:
        print(f"Avg out-links : {edges / len(content_notes):.1f}")
        print(f"Reciprocal    : {reciprocal / max(edges, 1):.0%} of links are bi-directional")

    if args.stats and content_notes:
        by_folder = defaultdict(int)
        for r in content_notes:
            by_folder[top_dir(r)] += 1
        print("\nNotes per folder:")
        for folder in sorted(by_folder):
            print(f"  {by_folder[folder]:4d}  {folder}")
        hubs = sorted(content_notes, key=lambda r: len(incoming.get(r, ())), reverse=True)[:15]
        print("\nMost-linked notes (hubs):")
        for r in hubs:
            print(f"  {len(incoming.get(r, ())):4d}  {os.path.basename(r)[:-3]}")

    if args.weak:
        weak = sorted(
            (len({s for s in incoming.get(r, ()) if is_content(s)}), r) for r in content_notes
        )
        print("\nNotes with < 3 backlinks:")
        for n, r in weak:
            if n < 3:
                print(f"  {n}  {r}")

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
