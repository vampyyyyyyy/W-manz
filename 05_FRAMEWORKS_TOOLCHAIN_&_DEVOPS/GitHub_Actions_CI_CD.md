---
aliases: [CI/CD, GitHub Actions, Continuous integration Roblox, Deploy pipeline]
tags:
  - roblox-dev
  - devops/ci-cd
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# GitHub Actions CI/CD for Roblox

> **TL;DR:** For a file-based project ([[Rojo]] or [[Script_Sync]] + Git), the pipeline is: **format check → lint → typecheck → tests → build → deploy**. That's [[StyLua]] `--check`, [[Selene]], [[Luau_LSP]] `analyze`, then [[Lune]] or Luau Execution tests, then `rojo build`, then [[Open_Cloud_Place_Publishing]]. Gate production deploys behind a GitHub **Environment** with required reviewers, and keep the API key there as a secret.

## Reference workflow
```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
  push:
    branches: [main]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Rokit + project tools (rokit.toml pins versions)
        run: |
          curl -sSf https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | bash
          echo "$HOME/.rokit/bin" >> "$GITHUB_PATH"
      - run: rokit install
      - run: stylua --check src/
      - run: selene src/
      - name: Typecheck
        run: |
          rojo sourcemap default.project.json --output sourcemap.json
          curl -sSfLo globalTypes.d.luau https://raw.githubusercontent.com/JohnnyMorganz/luau-lsp/main/scripts/globalTypes.d.luau
          luau-lsp analyze --sourcemap=sourcemap.json --definitions=globalTypes.d.luau --base-luaurc=.luaurc src/
      - run: lune run tests        # pure-logic tests outside the engine
      - run: rojo build default.project.json -o build/game.rbxl
      - uses: actions/upload-artifact@v4
        with: { name: place, path: build/game.rbxl }

  deploy:
    needs: check
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production          # required reviewers + secrets live here
    steps:
      - uses: actions/download-artifact@v4
        with: { name: place, path: build }
      - name: Publish via Open Cloud
        env:
          ROBLOX_API_KEY: ${{ secrets.ROBLOX_API_KEY }}
          UNIVERSE_ID: ${{ vars.UNIVERSE_ID }}
          PLACE_ID: ${{ vars.PLACE_ID }}
        run: |
          curl --fail -X POST \
            "https://apis.roblox.com/universes/v1/$UNIVERSE_ID/places/$PLACE_ID/versions?versionType=Published" \
            -H "x-api-key: $ROBLOX_API_KEY" -H "Content-Type: application/octet-stream" \
            --data-binary @build/game.rbxl
```
> Verify tool flags against each tool's `--help` and your pinned versions. The tools move fast. If Rokit hits GitHub API rate limits on shared runners, authenticate it with a token (`rokit authenticate`).

## Security notes
- **Scope the API key** to `universe-places` Write on *one* experience, and set an expiry. GitHub-hosted runners have changing IPs, so an IP allowlist only works with a self-hosted runner (fixed IP) ([[Open_Cloud_APIs]]).
- Separate **staging** and **production** universes and keys ([[Access_Control_and_Confidentiality]]).
- Never echo secrets. Don't run deploy jobs on `pull_request` from forks.
- Wally/Pesde installs pull third-party code, so pin versions and review lockfile diffs ([[Third_Party_Code_and_Backdoors]]).

## Engine-level tests in CI
Pure logic runs under [[Lune]]. For engine behavior, upload with `versionType=Saved` to a test place and run a **Luau Execution** task via Open Cloud, then read its logs ([[Testing_Frameworks]]). A self-hosted Windows/macOS runner can also launch Studio from the command line with `--task RunScript --runScriptFile smoke.luau --outputFile out.log --quitAfterExecution` ([[Studio_Testing_Modes]]).

## Related
[[Rojo]] · [[Rokit]] · [[StyLua]] · [[Selene]] · [[Luau_LSP]] · [[Lune]] · [[Open_Cloud_Place_Publishing]] · [[Open_Cloud_APIs]] · [[Testing_Frameworks]] · [[Version_Control_Workflow]] · [[Third_Party_Code_and_Backdoors]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/cloud/guides/usage-place-publishing · https://create.roblox.com/docs/studio/cli
- https://github.com/rojo-rbx/rokit · https://github.com/JohnnyMorganz/luau-lsp
