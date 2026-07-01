# MCP Servers

Unlike skills, MCP servers can't be "restored" by copying a folder — they're either **claude.ai account connectors** (configured in the cloud) or **locally-installed packages** (wired into Claude Code config). This file is the checklist for re-creating the same MCP setup on another account/machine.

> No credentials are stored here. Connectors re-authenticate through their own OAuth flow when you add them.

## claude.ai connectors (account-bound)

These are configured in **claude.ai → Settings → Connectors** (not in any local file). On a new Claude account, re-add each one there and complete its OAuth sign-in.

| Connector | What it's used for |
|---|---|
| **Google Drive** | Search, read, and create files in Drive |
| **Higgsfield** | Image / video / audio / 3D generation (also has a local CLI — see below) |
| **Supabase** | Manage Postgres projects — tables, migrations, SQL, edge functions, logs |
| **Microsoft 365** | Teams / Outlook / Office data. **Needs re-authorization** — sign in again via the connector settings |

## Local MCP servers (npm-installed, wired into Claude Code)

| Server | Package | Status |
|---|---|---|
| **Playwright** | `@executeautomation/playwright-mcp-server` | Installed globally, but **not currently wired into Claude config** |

To register the Playwright MCP with Claude Code on any machine (after `npm i -g @executeautomation/playwright-mcp-server`, or just use `npx`):

```powershell
claude mcp add playwright -- npx -y @executeautomation/playwright-mcp-server
```

Verify what's registered:

```powershell
claude mcp list
```

## Notes

- Local MCP servers registered with `claude mcp add` are stored in `~/.claude.json` (per-project or global scope). Back them up by re-running the `claude mcp add` commands above rather than copying that file — it also contains project history and should not be committed.
- If you later add local (non-connector) MCP servers with API keys, keep the keys in your environment or a local `.env`, never in this repo. See [`../.env.example`](../.env.example).
