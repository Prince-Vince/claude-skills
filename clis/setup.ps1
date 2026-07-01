#Requires -Version 5.1
<#
    setup.ps1 — reinstall the CLIs the skills depend on, on a fresh Windows machine.
    Safe to re-run: it skips anything already on PATH.
    System tools use winget; developer tools use npm.

    Usage:
        pwsh -File setup.ps1            # install everything
        pwsh -File setup.ps1 -WhatIf   # show what would be installed, do nothing
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param()

function Test-Cli($name) { [bool](Get-Command $name -ErrorAction SilentlyContinue) }

function Install-Winget($id, $probe) {
    if (Test-Cli $probe) { Write-Host "[skip] $probe already installed" -ForegroundColor DarkGray; return }
    if ($PSCmdlet.ShouldProcess($id, "winget install")) {
        Write-Host "[winget] installing $id ..." -ForegroundColor Cyan
        winget install --id $id --exact --accept-source-agreements --accept-package-agreements
    }
}

function Install-Npm($pkg, $probe) {
    if (Test-Cli $probe) { Write-Host "[skip] $probe already installed" -ForegroundColor DarkGray; return }
    if ($PSCmdlet.ShouldProcess($pkg, "npm i -g")) {
        Write-Host "[npm] installing $pkg ..." -ForegroundColor Cyan
        npm install -g $pkg
    }
}

# --- 1. System tools (winget) ---
if (-not (Test-Cli 'winget')) {
    Write-Warning "winget not found. Install 'App Installer' from the Microsoft Store, then re-run."
} else {
    Install-Winget 'Git.Git'             'git'
    Install-Winget 'GitHub.cli'          'gh'
    Install-Winget 'OpenJS.NodeJS.LTS'   'node'
    Install-Winget 'Python.Python.3.13'  'python'
    Install-Winget 'Microsoft.AzureCLI'  'az'
    Install-Winget 'Docker.DockerDesktop' 'docker'
}

# --- 2. Developer CLIs (npm global) — needs Node from step 1 ---
if (Test-Cli 'npm') {
    Install-Npm '@anthropic-ai/claude-code'                'claude'
    Install-Npm 'firecrawl-cli'                            'firecrawl'
    Install-Npm '@higgsfield/cli'                          'higgsfield'
    Install-Npm 'vercel'                                   'vercel'
    Install-Npm '@executeautomation/playwright-mcp-server' 'playwright-mcp-server'
} else {
    Write-Warning "npm not on PATH yet. Open a new terminal after Node installs, then re-run to finish the npm packages."
}

# --- 3. Register the Playwright MCP with Claude Code ---
if ((Test-Cli 'claude') -and -not $WhatIfPreference) {
    Write-Host "[claude] registering Playwright MCP (idempotent; ignore 'already exists')" -ForegroundColor Cyan
    claude mcp add playwright -- npx -y @executeautomation/playwright-mcp-server 2>$null
}

Write-Host "`nDone. Verify with:  node -v; gh --version; firecrawl --version; claude mcp list" -ForegroundColor Green
Write-Host "Then set API keys (see ..\.env.example): FIRECRAWL_API_KEY, VALYU_API_KEY" -ForegroundColor Green
