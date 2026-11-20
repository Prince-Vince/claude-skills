# Impeccable local source patch

The numbered Git patches contain Vince's local changes and reproduction instructions. They are based on upstream `next` commit `5261629497162ccdc68618421f29863db2be094a`. Apply them in order to that exact checkout with `git am`.

The engine source commit is `b627afbc74fedb7983103f6bfd173dc1329b13f3`; subsequent patches update Windows launcher compatibility and test/build helpers without changing the Rust engine. The local working repository is `~/tools/impeccable-patched`, branch `fix/local-sandbox`. No upstream issue, pull request, or release was published.

The source's `local-build/README.md` explains the isolated build, tests, packaging, and review. The shared runtime package is in [`skills/impeccable`](../../skills/impeccable). It contains a native Windows x64 engine; it does not download executables for other platforms.

This patch was prepared with AI assistance. Retain upstream's Apache-2.0 license and the local change notices when redistributing.

## Test environment notes

Use an LF checkout and Node 24 for the JavaScript suites. Install the locked development dependencies in the disposable container with lifecycle scripts disabled and optional engine packages omitted. Do not expose model credentials. The Windows bind mount can exceed Bun's default five-second copy timeout; the local test adapter allows twenty seconds.

Run oracle fixtures from a distinct path such as `/opt/impeccable-validation`, not `/src`: the upstream normalizer otherwise replaces ordinary `/src/` path segments with `<REPO>`. Run permission-denial cases as an unprivileged user. The component screenshot test also requires Arial in the test environment; no font is redistributed with this package. These adjustments change the test environment, not expected results or runtime permissions.

Use Docker's `--init` or run the suites under `tini -s` so orphaned processes are reaped. Without an init, the server-cleanup test sees an already-exited zombie process and reports it as still alive.
