# Lessons from the first conversion (AI Governance Deployment Tracker, Oct 2026)

Each item: what happened, why it mattered, what to do instead.

## UI/UX (the big one)
- **The template's look replaced the app's.** Agents built every screen from the template's `tw_*` helpers (indigo),
  as the conventions say, and the "theme pass later" never happened. The person's first click-through found most of the
  UI/UX stripped. → Port the theme into the template's helper constants and `application.css` in phase 1, before any
  screen exists. The conventions only require styling to live in the helpers; they don't require indigo.
- **Agents simplified layouts and reported it as a "deviation"**, and the reviewer accepted it because data and rules
  matched (tree + side panel → collapsible sections; list columns and filters dropped; dashboard chips and tabs dropped;
  panels → full pages). → Treat UI deviations like logic deviations: not accepted without the person's OK. Give agents
  reference screenshots and require them to match.
- **"List your UI deviations" still produced 25 deviations**, most of them agent preference or skipped work (menus moved,
  tables turned into cards, shortcuts and dialogs dropped, colours and date formats changed). The person reverted almost all
  of them. → The brief must say: **match the source exactly; deviate only where the web platform makes it impossible**
  (hover on touch screens, URLs per record) **or the template conventions forbid it, and give that reason.** "I didn't have
  time" and "I think this is better" are not reasons — build it, or report it as not done.
- **Nobody looked at a screen until the end.** Agents can't run servers; the reviewer had no browser. → Get a screenshot
  path working in phase 1 (headless browser, or the person sends screenshots) and compare each phase's screens.
- Things that only show up in a browser: a link inside a Turbo Frame without `data-turbo-frame` opens into that frame
  ("Content missing"). Check frame targets in review.

## Process
- **Subagent got stuck by the permission classifier** (git merge, edits to shared files, rm). Agents must stop and
  report; you must not do the blocked action on their behalf without the person's OK (permission laundering). Ask the
  person once for a standing OK to resolve merge conflicts and merge-stale tests yourself.
- **An agent stalled** (watchdog after 10 min without output). Resume it with SendMessage; it keeps its context. Briefs
  say: commit after each step, never run commands that can sit silently (no servers, use `timeout`).
- **Parallel branches collide** on shared files (tab list, routes, menu, tab-count tests). Tell agents to keep shared
  edits minimal and separated, to write tests that derive counts from the shared list instead of hard-coding them, and to
  `git merge main` before finishing.
- **Merges can paste route blocks into the wrong parent** (a register route block landed inside `resource :service_scope`,
  90 dead routes). Add a routes test that asserts each resource is routed once, under the right parent.
- **Two agents built the same thing** (two ways to raise a risk, two sensitive-content checks), causing double logging.
  When an agent builds something cross-cutting, tell the others to reuse it; dedupe at merge.

## Data and parity
- Dump the source's final schema from a freshly migrated DB; compare Rails columns to it table by table.
- Generate real fixtures with the source app itself (its export, its demo seed), commit them, and test the Rails import
  against them value by value. Then compute the same outputs in both apps (overview numbers, templates, reports, scripts)
  and diff. This caught nothing wrong in logic, which is exactly the confidence you want.
- Expected-values files written by an agent: regenerate them yourself with the source app before trusting them.
- Time zones: Rails defaults to UTC; the desktop app used local time. Set `config.time_zone` early, check imported
  timestamps (local, no zone) convert correctly, and write fixtures in local time.
- Stored values must stay identical to the source (vocab strings, JSON shapes, keys) so imported data works.

## Security
- Active Storage serves files to anyone with a signed link by default. Require sign-in on `ActiveStorage::BaseController`.
- Read-only API clients: refuse writes at the lowest layer, and refuse GETs to endpoints that act (allow-list `List*`).
- Secrets: encrypted credentials only; filter params; scrub errors; never in job arguments or the DB.
- CSV exports: prefix text starting with `= + - @ \t \r` with an apostrophe (formula injection).
- Browser storage: even reading `window.localStorage` throws when site data is blocked; wrap the access itself in try/catch.
- Generated HTML reports: serve with `Content-Security-Policy: sandbox`.

## Environment
- Ruby 3.4+/4.0 no longer loads `csv` by default (it needs a Gemfile entry, which needs Joe's approval).
- Windows: see `environment.md` (Git Bash `~` is the Windows home; PowerShell mangles quotes; write files via the UNC path).
- An agent working in Git Bash created stray folders in the Windows home and then tried `rm -rf ~/...` there. The classifier
  blocked it. Briefs now say: write only through the UNC worktree path; never `rm` outside the worktree.

## Added 2026-10-13 (Rails audit, regulatory rulesets, MCP endpoint)

### Running WSL from the Bash tool (Git Bash), not PowerShell
- `wsl.exe -d Ubuntu -- bash -c '... $f ...'` loses `$var` and breaks quoting; `bash /mnt/c/...script.sh` gets its path
  rewritten to `C:/Program Files/Git/mnt/c/...`. What works every time: write the script to the scratchpad with a heredoc,
  then `MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu -- bash "/mnt/c/Users/<user>/AppData/Local/Temp/claude/.../script.sh"`.
  Put `export PATH="$HOME/.local/bin:$HOME/.local/share/mise/shims:$PATH"` at the top of every script.
- `python` is not on the Git Bash PATH on this PC (Windows Store alias). Run Python inside WSL (`python3`).

### Reviewing and merging agent branches
- `merge_branch.sh` merges first and runs CI after, so a failed gate leaves the merge commit on local main (not pushed).
  Fix forward on main (that is what happened: three test assertions after a review fix-up) or `git reset --hard ORIG_HEAD`
  right away. The script now prints that hint.
- A review fix-up you make yourself must run the branch's tests before the merge, not after. Grep the tests for the value
  you removed (the whoami email) before committing.
- Two agents sharing one constant list (`Mcp::Tools::TOOL_NAMES`) is a cheap, predictable conflict: tell both agents the
  file is yours to merge, then write the combined list by hand during sync. Better than a registry that needs code.
- Give parallel agents a written contract (class shape, where the user comes from, how errors are reported) and tell each
  one what the other owns. Both delivered without touching the other's files.

### The `mcp` gem (official Ruby SDK, 1.7)
- A tool that raises gets wrapped in a JSON-RPC "Internal error"; only `MCP::Tool::Response.new(..., error: true)` is a
  tool error. We subclass `MCP::Server` and override the private `call_tool` to turn our `Mcp::Tools::Error` into one; a
  test guards the private-method dependency.
- `StreamableHTTPTransport` in `stateless: true, enable_json_response: true` mode is the right fit for a Rails action; use
  the transport, not `handle_json`, so Accept/Content-Type/MCP-Protocol-Version are handled. Its DNS-rebinding check
  allows localhost only; turn it off and rely on `config.hosts`. `serve_subscriptions_listen: false` or the streaming body
  breaks in a buffered Rails response. GET is 405 in stateless mode (expected).
- Bearer tokens: digest-only storage, show once, revoke keeps the row, `filter_parameters` already covers `authorization`.
  Never put the secret in a flash or redirect; render it in the modal with `Cache-Control: no-store`.
- Claude clients: Claude Code takes `--header "Authorization: Bearer …"`; Claude Desktop custom connectors may not;
  claude.ai connectors want OAuth. Say which is verified.

### Regulatory content
- Primary sources that block or hide text: ecfr.gov redirects automated reads to an "unblock" page (use the LII mirror
  for a cross-check, cite eCFR); le.utah.gov section pages render by script (fetch the chapter PDF under /xcode/...);
  state bill PDFs come back as binary to WebFetch (extract text with pypdf; a wheel is in `~/fwsrc`, unzip it and set
  PYTHONPATH rather than installing).
- Codified numbering differs from enrolled bills (Utah SB 226 enacted "13-75", codified as 13-77). Cite the code, not the
  bill, and record the retrieval date per requirement.
- Verdict logic must read `in_force?`; a requirement with a future `applies_from` is not a gap today. Tallies on screens,
  reports and digests all need the same rule, so put it in the verdict, not in the view.
- "Met" means client-confirmed. Say so wherever the word appears, and never default a ruleset to every client without a
  jurisdiction fact.

### Audit method that worked
- Read-only probes with `RAILS_ENV=test bin/rails runner` on catalog value objects (conditions, grading, keyword matching)
  found real defects in minutes without touching data. Keep that script in the scratchpad.
- Keyword substring matching on app names ("motion", "otter", "jamie") produces false findings; use word boundaries.
