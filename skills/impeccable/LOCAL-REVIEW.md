# Locally patched Impeccable

This is Vince's reviewed Windows distribution, built from a patched source checkout. It is not an official upstream release. The included Apache-2.0 license and upstream notices apply; local modifications are identified here and in the source patch.

Use the bundled `scripts/impeccable.cmd` on Windows, or `scripts/impeccable` from Git Bash. The launcher checks the engine SHA-256 on every invocation and never downloads, updates, or substitutes an upstream/PATH binary. `scripts/local-engine.json` records the source and binary identity.

The full engine and design references are included. Live-edit work uses the parent chat by default, retaining that agent's approvals. Telemetry and automatic critique/health uploads are off. No hooks or MCP servers are installed by copying this skill. Explicit feature requests can still contact websites or Impeccable services; this is not an offline-only engine.

## Routine work without repeated prompts

The patched workers no longer use Codex's unrestricted bypass flag or Claude's `bypassPermissions` mode. Codex uses a named permission profile with minimal OS reads, project writes, secret-file exclusions, and command networking disabled. Claude uses file tools only, no shell/connectors, and file reads/writes restricted to the project. Blocked actions fail and return to the parent chat; there is no unrestricted retry. Worker code rejects filesystem roots and the user home as unattended project scopes.

These settings need compatible agent runtimes. The installed Codex Windows sandbox rejected the strict read profile because it requires root read access; this package does not weaken that profile to make it run. The installed Claude 2.1.220 predates the required file-boundary controls (2.1.314+). Consequently, standalone workers are not enabled in this Windows package. Parent-chat live edits remain available. Routine edit approval is governed by the parent application's existing policy.

TLS dependency versions were raised to `rustls-webpki 0.103.16` and `webpki-roots 1.0.10`. The source patch and review document the tests, scan findings, and limitations. Future upgrades require rebuilding and reviewing the package; do not replace the engine with a stock upstream binary.
