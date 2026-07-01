# CLIs

The command-line tools the skills (and Vince's day-to-day work) depend on. Run [`setup.ps1`](setup.ps1) on a fresh Windows machine to install them all, or install individually below.

## What's needed and why

| CLI | Install | Used by |
|---|---|---|
| **Node.js + npm** | winget `OpenJS.NodeJS.LTS` | `hyperframes*`, `gsap`, `valyu-best-practices`, `remotion`, `website-to-hyperframes`, `frontend-design`, `web-animation-design`, `setup-pre-commit`, `migrate-to-shoehorn` |
| **Python 3** | winget `Python.Python.3.13` | `gsap` (audio-data script), assorted `py` workflows |
| **firecrawl-cli** | `npm i -g firecrawl-cli` | all 8 `firecrawl-*` skills |
| **git** | winget `Git.Git` | `git-guardrails-claude-code`, `tdd`, `setup-pre-commit`, all GitHub-issue skills |
| **GitHub CLI (`gh`)** | winget `GitHub.cli` | `write-a-prd`, `prd-to-issues`, `triage-issue`, `qa`, `request-refactor-plan` (all open GitHub issues) |
| **Claude Code (`claude`)** | `npm i -g @anthropic-ai/claude-code` | runs the skills themselves + `claude mcp add` |
| **Playwright MCP server** | `npm i -g @executeautomation/playwright-mcp-server` | local browser-automation MCP (see [`../mcp/`](../mcp/)) |
| **Higgsfield CLI** | `npm i -g @higgsfield/cli` | Higgsfield media generation (pairs with the connector) |
| **Vercel CLI** | `npm i -g vercel` | deploys (portfolio, MemberView, etc.) |
| **Azure CLI (`az`)** | winget `Microsoft.AzureCLI` | MemberView / IPRA Azure deploys |
| **Docker** | winget `Docker.DockerDesktop` | general containerized work |

### On-demand (no global install needed)
- **hyperframes** and **valyu** CLIs — invoked per-project (`npx hyperframes …`) or via scripts the skills bundle, so they don't need a global install.

## Verify after install

```powershell
node -v; npm -v; python --version; git --version
gh --version; az version; docker --version
firecrawl --version; vercel --version; claude --version
claude mcp list
```

## API keys
Several CLIs need keys (Firecrawl, Valyu). Put them in your environment or a local `.env` — see [`../.env.example`](../.env.example). Never hard-code them.
