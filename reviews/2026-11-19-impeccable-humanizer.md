# Humanizer and Impeccable review — November 19, 2026

## Decisions

- **Humanizer: APPROVE** the three-file payload in `skills/humanizer`, after independently resolving the scanner's false positives. Installed locally and verified byte-for-byte.
- **Impeccable full runtime: REJECT for installation at the reviewed revisions.** Confirmed vulnerable TLS dependency versions remain unresolved. This is an installation decision, not a claim that the project is malicious.

Vince's saved rule requires reviewing exact source with skill-inspector and NVIDIA SkillSpector `--no-llm`, then stopping on unresolved serious risks. No candidate skill, installer, or runtime was executed. No scanner updates, extra providers, or dependencies were installed. External LLM analysis stayed disabled. An OSV query sent 200 public Cargo package names and versions to `https://api.osv.dev/v1/querybatch`; `--no-llm` does not imply an offline review.

## Exact sources

| Artifact | Revision |
|---|---|
| [Humanizer](https://github.com/blader/humanizer/tree/a32f24407364c74c812b43c15926d638bee1e072) | `a32f24407364c74c812b43c15926d638bee1e072`, skill 4.0.0 |
| [Impeccable](https://github.com/pbakaus/impeccable/tree/b49177d32788f2dc585c42831d845dacf1ebed2c) | `b49177d32788f2dc585c42831d845dacf1ebed2c`, skill 4.10.0 |
| [Pinned engine 0.1.27](https://github.com/pbakaus/impeccable/releases/tag/engine-v0.1.27) | `645925acd71b18558488c5b8d8f263404cb68db8` |
| [Newer engine 0.1.28](https://github.com/pbakaus/impeccable/releases/tag/engine-v0.1.28) | `80f576894c6157cd895f749565e8755f8406bce2` |

Humanizer `SKILL.md` SHA-256: `e32d1aa54b2230bd355f2f16bcc9c5afbc8c74bfe227cad55dd686cff0206e5d`.

The Windows x64 engine 0.1.27 was downloaded for inspection only. SHA-256 `ba9627d4552bca5666020624d8e994aea8b8b44c46b995e18b5babad0f431fc8` matched the source checksum and release digest; Windows reported a valid Authenticode signature. Neither proves the runtime is safe. The binary was never executed and is not distributed in this repository. Version 0.1.28 was checked through its source, not run.

## Static evidence and limits

NVIDIA SkillSpector 2.11.2 ran with `--no-llm` on both source packages and again on the exact Humanizer installation payload.

| Target | Raw scanner result | Coverage limits |
|---|---|---|
| Humanizer repository | 49/100, MEDIUM, CAUTION; highest issue HIGH | All discovered files inspected; overall status partial because two prose fragments were mistaken for local references |
| Humanizer installation payload | 30/100, MEDIUM, CAUTION; highest issue HIGH | Same reference-resolution limitation; independent review covered all three files |
| Impeccable compiled skill | 100/100, CRITICAL, DO_NOT_INSTALL; highest individual issue HIGH | 65 of 69 components fully inspected, four partial; 94.2% coverage and degraded analyzer/reference-resolution limits |

An additional scan of the 542-file Rust runtime source was attempted but ended without a complete report after blocking dependency findings were confirmed. It is not counted as a completed scan. Source inspection covered execution, downloads, agent subprocesses, filesystem boundaries, hooks, browser behavior, telemetry, uploads, and dependency handling; this was not an exhaustive formal audit.

Local raw reports, source clones, and the downloaded binary are retained under `~/Downloads/skill-review-20261119/`. Raw reports are not copied here because they contain machine-specific paths and large source excerpts.

## Humanizer findings

The two HIGH `AR2` matches at `SKILL.md:208` and `:211` are the words “announced without warning” inside before/after grammar examples. They do not instruct an agent to bypass consent. The apparent unresolved paths at lines 10 and 253 are a heading separator and the prose variants “gate/gated/gating,” not missing executable resources. The full repository also contains unpinned `npx` development/install examples and a missing `allowed-tools` warning; those examples are not part of the installed payload.

The instructions preserve facts, quotations, code, links, and uncertainty and treat text being edited as untrusted content. The installed files are exactly upstream `SKILL.md`, `LICENSE`, and `agents/openai.yaml`. No upstream validation scripts, package manifests, or plugin installers were installed. The upstream validator was inspected without execution. The semantic APPROVE decision resolves the raw HIGH examples as false positives; it does not relabel the scanner report as clean or complete.

## Impeccable blocking findings

### TLS trust dependencies

The engine lockfile contains:

| Dependency | Pinned version | Advisory | Fixed version |
|---|---|---|---|
| `rustls-webpki` | 0.103.15 | [RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) | 0.103.16 |
| `webpki-roots` | 1.0.9 | [RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) | 1.0.10 |

These advisories concern certificate chains through distrusted emSign intermediates whose private keys are known. `crates/context/src/http.rs` includes bundled roots alongside platform roots, so an updated Windows trust store alone does not remove the affected bundled trust anchor. This is a relevant runtime dependency, not merely unused development metadata.

The skill's runtime source matches engine 0.1.27 for `crates/`, `Cargo.toml`, and `Cargo.lock`. Engine 0.1.28 changes internal package versions but retains both affected external dependency versions. Thus switching to that release does not resolve these findings. This is a source/dependency assessment; no exploit or runtime test was performed.

### Subprocess permissions and network behavior

`crates/live/src/copy_edit_agent.rs` launches Codex with `--dangerously-bypass-approvals-and-sandbox` and Claude with `--permission-mode bypassPermissions`. Automatic provider selection can choose these paths. `IMPECCABLE_LIVE_COPY_AGENT=chat` avoids those subprocesses in the live-server flow, but a direct provider argument can override the preference; this is not a complete sandbox boundary.

The launcher downloads a pinned engine from GitHub and checks its source-pinned SHA-256. It can also use a configured `IMPECCABLE_BIN` or PATH executable. Optional hooks modify Claude settings. Runtime code supports telemetry and automatic critique/design-health uploads; `DO_NOT_TRACK` or `IMPECCABLE_NO_TELEMETRY` disables the reviewed telemetry/upload paths. Those controls do not repair TLS validation or remove subprocess bypass capabilities.

Positive boundaries inspected include loopback binding, a random live-session token, canonicalized file paths, and a fresh browser profile with sandboxing enabled by default. These reduce specific risks but do not override the blocking findings.

### Scanner false positives investigated

Some high scores reflect design language: “never judge” concerns screenshot quality, “new identity” means visual branding, and “clear states” means UI states. A `Remove` keyboard-handler comment is not a destructive shell command. Local browser fetches carrying the session token are the intended live-edit protocol. Ignoring a design-detector warning is not disabling a security scanner. These were assessed in their surrounding source rather than accepted as evidence of malware.

The partial components were `scripts/data/font-index.json`, `scripts/impeccable`, `scripts/live-browser.js`, and `scripts/modern-screenshot.umd.js`. Manual inspection helped explain behavior but did not turn scanner partial coverage into a clean scan.

## Installation and next review

Humanizer was copied to the shared `.agents` directory, Claude Code, and Hermes default/daily/linkedin/research/video skill directories. All seven copies matched the three repository files. The previous Hermes Humanizer 2.5.1 was backed up outside discovery at `~/Downloads/skill-review-20261119/local-backups/`.

Impeccable remains outside active skill directories. No hooks, MCP servers, startup entries, runtime settings, or telemetry preferences were installed for it. No playbook-only edition was substituted after the user requested full-runtime review.

Before reconsidering installation, review a release with fixed TLS dependencies and an acceptable agent-permission configuration, verify source and artifact identity again, and resolve incomplete static coverage. Do not silently update to an unreviewed runtime.
