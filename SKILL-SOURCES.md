# Added skills — 2026-09-14

## Humanizer — 2026-11-19

- Upstream: [blader/humanizer](https://github.com/blader/humanizer/tree/a32f24407364c74c812b43c15926d638bee1e072).
- Pinned commit: `a32f24407364c74c812b43c15926d638bee1e072`; skill version 4.0.0; MIT license retained.
- Exact upstream payload: `SKILL.md`, `LICENSE`, and `agents/openai.yaml`. No candidate runtime or validator was executed.
- Reviewed using NVIDIA SkillSpector 2.11.2 `--no-llm` plus independent source inspection. See [findings and limitations](reviews/2026-11-19-impeccable-humanizer.md).
- [Portable install helper and agent locations](SHARED-SKILLS.md). Local copies were verified against the repository payload.

Impeccable was also downloaded and reviewed at commit `b49177d32788f2dc585c42831d845dacf1ebed2c`, but its full runtime was rejected for installation at the reviewed revisions. It is deliberately absent from discoverable skill folders; the review records its pinned sources and blockers.

## Scrolling presentation kit — 2026-09-25

- `scrolling-presentations`: created from the browser-presentation workflow and Microsoft example developed in this session; includes original workflow guidance, supporting references, and a no-overwrite copy helper.
- `reference-led-ui`: the user's custom local reference-led design skill, copied without machine-specific paths.
- `rtf`: the user's supplied RTFSkill.zip with local safety fixes and portability adjustments. See `skills/rtf/PORTABILITY.md` for the source hash, changes, dependencies, and validation limits. No new license is assigned to the original code.
- `frontend-design` and `web-animation-design`: already present in this repository; left unchanged and linked as companions.
- Microsoft SVG icons: official unmodified Power Platform and Azure icons, used in the educational example under their original terms. See `skills/scrolling-presentations/assets/microsoft-example/ASSET-NOTICES.md`.

No scraped source pages, external transcripts, private account settings, environments, or downloaded videos are included in the new kit.

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
