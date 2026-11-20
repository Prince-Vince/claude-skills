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

## Impeccable: downloaded, installation blocked

The full runtime was reviewed at the user's request. It is **not included in discoverable skill folders and was not executed or installed**. The pinned engine and the newer engine release checked on November 19, 2026 contain affected TLS dependencies. The runtime also supports launching coding agents with approval and sandbox bypass flags.

See the [review and source pins](reviews/2026-11-19-impeccable-humanizer.md). No playbook-only substitute was installed. Reassess a patched upstream release before installing the full runtime.
