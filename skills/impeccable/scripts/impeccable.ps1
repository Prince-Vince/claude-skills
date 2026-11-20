$ErrorActionPreference = 'Stop'
# This reviewed distribution never searches PATH or downloads an engine.
$engine = Join-Path $PSScriptRoot 'bin\windows-x64\impeccable.exe'
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'local-engine.json') -Raw | ConvertFrom-Json
if (-not (Test-Path -LiteralPath $engine -PathType Leaf)) { throw 'Reviewed local engine is missing. Rebuild this package; no download was attempted.' }
$hasher = [System.Security.Cryptography.SHA256]::Create()
$stream = [System.IO.File]::OpenRead($engine)
try { $digest = [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '').ToLowerInvariant() }
finally { $stream.Dispose(); $hasher.Dispose() }
if ($digest -ne $manifest.sha256) { throw 'Reviewed local engine hash mismatch. Refusing to run.' }
if ($args.Count -gt 0 -and $args[0] -in @('install', 'update', 'upgrade', 'pro')) { throw 'This reviewed local runtime is pinned. Update and review the patched source first.' }
$env:IMPECCABLE_BIN = $engine
$env:IMPECCABLE_PRO = 'off'
$env:IMPECCABLE_NO_TELEMETRY = '1'
$env:IMPECCABLE_LIVE_COPY_AGENT = 'chat'
& $engine @args
exit $LASTEXITCODE
