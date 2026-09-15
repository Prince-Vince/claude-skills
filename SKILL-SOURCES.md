# Added skills — 2026-09-14

| Skill | Upstream | Pinned commit | License |
|---|---|---|---|
| skill-inspector | https://github.com/NVIDIA/SkillSpector | 03e8f56bdb9ddb85d7db09ca592f97dd0f545c41 | Apache-2.0 |
| archify | https://github.com/tt-a1i/archify | 851b279f3710c3ed6f152f4b044a504ca4eb207c | MIT; bundled third-party notices retained |

Skill folders contain upstream files. NVIDIA's repository license is included with skill-inspector. No environments, credentials, or installed dependencies are backed up.

## Restore

Copy each folder under skills/ into ~/.agents/skills/ for Codex, or ~/.claude/skills/ for Claude Code. Codex discovers them on the next turn; start a new Claude Code session after restoring.

Archify requires Node.js 18 or newer. No npm installation is required for its packaged renderer. Check with `node <skill-directory>/bin/archify.mjs doctor`.

Skill Inspector uses the separate SkillSpector CLI. Install it in an isolated environment with Python 3.12–3.14:

```powershell
python -m venv "$env:USERPROFILE\tools\skillspector\venv"
& "$env:USERPROFILE\tools\skillspector\venv\Scripts\python.exe" -m pip install 'git+https://github.com/NVIDIA/SkillSpector.git@03e8f56bdb9ddb85d7db09ca592f97dd0f545c41'
& "$env:USERPROFILE\tools\skillspector\venv\Scripts\skillspector.exe" scan <skill-directory> --no-llm
```

Add the environment's Scripts directory to PATH to use the short `skillspector` command. Static scans require no LLM key; optional LLM review needs a configured provider. The skill supports manual source review when the CLI is unavailable.