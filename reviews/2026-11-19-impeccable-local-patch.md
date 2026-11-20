# Locally patched Impeccable — November 19, 2026

**Combined verdict: CAUTION, suitable for the scoped Windows installation described here.** The original stock-runtime rejection remains valid for its reviewed releases. This follow-up addresses the two TLS dependency advisories and unrestricted copy-edit workers in our own source checkout.

## What changed

- `rustls-webpki` is locked to 0.103.16 and `webpki-roots` to 1.0.10. OSV's batch check returned no known advisories for the 200 locked registry packages. This is a database snapshot, not a guarantee of no vulnerabilities.
- Codex workers use a strict named filesystem profile, project writes, secret-file exclusions, no command networking, and no repeated approval prompts. Hooks, plugins, apps, browser tools, extra agents, and MCP configuration are disabled for the worker. Unsupported versions fail closed. The Windows worker is explicitly disabled because a real local sandbox probe rejected the required read isolation.
- Claude workers have file tools only, `dontAsk` mode, project-only file boundaries, secret-file exclusions, and no shell, browser, or connector tools. They require 2.1.314+. Vince's installed 2.1.220 is refused.
- The installed package therefore uses the parent-chat flow for live edits. Existing parent-agent permission controls remain in force. It does not enable general-purpose unattended bypasses.
- Local launchers verify the executable's SHA-256 each time, refuse missing/tampered binaries and self-update commands, disable telemetry/automatic critique-health uploads and Pro dispatch, and never fall back to upstream downloads or PATH binaries. Feature-specific network requests remain possible when the user invokes those features.

## Source and artifact

- Upstream base: [`5261629497162ccdc68618421f29863db2be094a`](https://github.com/pbakaus/impeccable/tree/5261629497162ccdc68618421f29863db2be094a).
- Patched engine source: `b627afbc74fedb7983103f6bfd173dc1329b13f3`; reproduction patches and subsequent packaging fixes are under [`patches/impeccable`](../patches/impeccable).
- Skill version: 4.10.0; engine reports 0.1.27; local distribution identifier: `vince-reviewed-windows-1`. This is not an official upstream release.
- Windows engine SHA-256: `c27021bacb38f32c5b28ddcd1cb901d24897d6ec1549cb1afe132050b6087fac`.
- Built from source in an isolated Docker container with only the checkout mounted, no user credentials or home-directory mount. The Windows executable requires only Windows system DLLs and was tested on the host.
- The `next` base also changes explicit agent/Loop connection code compared with the first review. That code can register MCP entries, install and trust its own hooks, and update marked instruction blocks when connection commands are explicitly invoked. It was inspected as a configuration-writing surface; no Loop connections, hooks, MCP servers, trust grants, or agent-rule changes were performed by this installation.

## Scanner evidence

NVIDIA SkillSpector 2.11.2 scanned the exact staged package with `--no-llm`. Raw result: **100/100, CRITICAL, DO_NOT_INSTALL**, highest individual severity HIGH. Coverage: 70 of 74 components fully inspected, four partial, 94.6%; overall status partial. The combined CAUTION verdict is independent of this raw score.

All 13 HIGH findings were investigated in their surrounding source:

| Rules | Locations | Assessment |
|---|---|---|
| AR2 | `reference/animate.md:92`, `critique.md:285`, `new-work.md:105`, finish-reviewer agent/degraded references | Design-quality language and descriptions of a hard turn limit; not instructions to disable approvals |
| MP3 | `reference/colorize.md:23`, `mode-operate.md:15` | Visual brand identity and UI state, not agent identity or memory changes |
| AS1 | `reference/hooks.md:17,115` | Real configuration-writing capability, documented as an explicit hook feature; no hooks installed |
| P2 | `reference/live.md:200` | An HTML/CSS variant example, not a system-message injection |
| TM1 | `scripts/live-browser.js:8401` | A keyboard handler comment describing removing a preview element, not a destructive shell command |

Medium findings include local live-server fetches with session tokens, documented CLI/file operations, and hook/design-detector configuration. These behaviors match the product's function; token checks, loopback binding, path handling, permissions, downloads, and telemetry were independently inspected. The previous full-source review and focused patched-source inspection supplement the scan.

Partial coverage remains for the compiled executable, font-index data, live-browser JavaScript, and minified screenshot vendor code. Source-built artifact identity, Windows import inspection, targeted source review, and runtime tests provide additional evidence; the scanner did not fully inspect the binary or deobfuscate all vendor code. The report is not described as a clean or exhaustive scan. No external LLM review was enabled. OSV received public package names and versions only.

## Verification

- Four permission regression tests pass; the two bypass tests failed before the fix and passed after it.
- Skill generation and upstream manifest, prose, and token-budget checks pass after using LF source line endings.
- Native Windows smoke checks pass: engine handshake, static HTML detection, real headless-browser detection, refused self-update, refused missing binary, and refused hash-mismatched binary. The detector identified the intentionally tiny, low-contrast text.
- The real Codex Windows sandbox probe failed closed on strict read isolation. This is a documented platform limitation, not a passing sandbox test; no model was called.
- Broad Rust and JavaScript suite results are recorded in the completion note below. Initial environment failures involved root-user file permissions, a missing Arial font, Windows CRLF shebang/workflow files, a missing curl test utility, and a short file-copy timeout. Fixes were confined to the build/test environment; fonts are not bundled or published.

### Completion evidence

| Check | Result |
|---|---|
| Rust workspace | 3,354 passed initially; all three failures passed after correcting the test environment, for 3,357 passing cases across the run and targeted reruns; nine ignored |
| JavaScript core | 499 Bun tests passed; 286 Node tests passed across the full run and corrected hook-manifest rerun; four skipped |
| Oracle corpus | 1,443 passed, zero unexpected differences, 22 upstream-accepted deltas, one platform skip |
| Extension compatibility | 480 passed |
| Live behavior | 275 passed, two skipped |
| Framework fixtures | 196 passed |
| Claude plugin end-to-end | Skipped: Claude CLI is not installed in the isolated container |
| Native Windows package | Six smoke checks passed; PowerShell, Command Prompt, and Git Bash launchers all return the pinned engine handshake |

The oracle was rerun from a distinct directory because `/src` collided with ordinary source paths in the upstream output normalizer. The live suite was rerun under a process reaper because the initial container left exited orphan processes as zombies. Expected results and runtime permission boundaries were not weakened. These are results across corrected runs, not a claim that one initial full sweep passed. No paid/model-backed tests or autonomous worker sessions were run.

All 74 package files were hash-verified against the scanned staging directory and the seven installed copies: Codex's shared `.agents/skills`, Claude Code, Hermes's default creative skills, and Hermes's daily, linkedin, research, and video profiles. Git attributes preserve the reviewed package bytes across checkouts. This verifies local installation; fresh agent sessions must discover the skill, and actual project use has not yet been validated with Vince.

## Installation boundary

Only the reviewed skill files, references, local launchers, license, manifest, and Windows engine are copied to agent skill directories. The engine is local-only by default for telemetry and approvals, but not an offline-only product. Use the bundled launcher and resolve example script paths relative to the actual loaded skill directory. Models hosted in other applications or on other computers need their own installation.

The generic binary still contains upstream administrative commands. Running it directly bypasses the local launcher's distribution defaults. Future upgrades require reviewing and rebuilding the patched source, not replacing the binary with an upstream release.
