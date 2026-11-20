# Shared skills

This repository stores portable skill files. Skills are loaded by the agent application, so they can be used with the models supported by that application. Copying a skill does not change model settings or make cloud chats inherit local files.

## Humanizer 4.0.0

The reviewed upstream files are in [`skills/humanizer`](skills/humanizer). They include the writing instructions, MIT license, and OpenAI agent metadata. No runtime, package installation, API key, or network access is required by this payload.

On Vince's Windows machine, matching copies were installed in:

| Agent | Skill location |
|---|---|
| Codex; compatible Gemini CLI and Copilot CLI versions | `~/.agents/skills/humanizer` |
| Claude Code | `~/.claude/skills/humanizer` |
| Hermes default profile | `%LOCALAPPDATA%/hermes/skills/creative/humanizer` |
| Hermes daily, linkedin, research, video profiles | `%LOCALAPPDATA%/hermes/profiles/<profile>/skills/creative/humanizer` |

All seven installed directories were checked against the repository files by SHA-256. Gemini and Copilot support the shared directory, but their interactive discovery was not tested. Start a fresh agent session or reload skills before use. Example request: “Use Humanizer to edit this draft while preserving its facts, links, and quotations.”

### Install on another computer

From the repository root, use Python 3 to copy only this reviewed skill:

```powershell
python scripts/install-reviewed-writing-skill.py --destination "$env:USERPROFILE/.agents/skills" --destination "$env:USERPROFILE/.claude/skills"
```

```sh
python3 scripts/install-reviewed-writing-skill.py --destination ~/.agents/skills --destination ~/.claude/skills
```

Repeat `--destination` for other applications' actual skill directories. Existing copies are refused unless you explicitly add `--replace --backup-dir <directory-outside-skill-folders>`. The helper uses Python's standard library, backs up replaced copies, verifies copied files, and does not execute skill code. Installed copies do not automatically sync after a repository update; review the new version before copying it again.

For an application without local skill discovery, supply `skills/humanizer/SKILL.md` as project instructions or a supported skill upload, retaining the license when redistributing. Cloud applications and other computers need their own setup.

## Impeccable: patched Windows runtime

[`skills/impeccable`](skills/impeccable) contains the locally built Windows x64 runtime, full design references, and a launcher that verifies the engine hash. The TLS dependencies are patched. Live edits use the parent chat's existing approval policy; standalone workers stay off where their required boundaries cannot be enforced. Telemetry and automatic critique/health uploads are disabled by the launcher. No hooks or MCP servers are installed.

Use `scripts/impeccable.cmd` from the installed skill directory on Windows, or its extensionless launcher from Git Bash. Resolve example `.agents/skills/impeccable/...` paths against the actual loaded skill's location. This package cannot automatically provision Linux, macOS, cloud chats, or another computer.

Install only the reviewed package from this repository:

```powershell
python scripts/install-reviewed-skill.py --skill impeccable --destination "$env:USERPROFILE/.agents/skills" --destination "$env:USERPROFILE/.claude/skills"
```

Repeat `--destination` for your actual Hermes profile skill directories. The helper refuses differing existing installations unless replacement and an external backup directory are explicitly supplied, and verifies every copied file. Reload skills or start fresh sessions after installation.

See the [local-patch review](reviews/2026-11-19-impeccable-local-patch.md) and [reproducible source patches](patches/impeccable). The [earlier upstream review](reviews/2026-11-19-impeccable-humanizer.md) remains a historical record; its rejected stock runtime is not the binary bundled here.
