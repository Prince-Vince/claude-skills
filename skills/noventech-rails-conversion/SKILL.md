---
name: noventech-rails-conversion
description: Convert an existing application (Python, desktop, Node, PHP or anything else) into a Ruby on Rails web app using Joe's Noventech Rails template (gitlab.nvtlabs.com/joew/noventech-rails-template), by planning the port, delegating it to subagents in git worktrees, and reviewing every branch for logic, data, security and UI/UX parity with the original. Use this whenever someone wants to port, rewrite, migrate or rebuild an app "in Ruby", "in Rails", "as a web app" for Noventech, mentions Joe's template, bin/new-app, or the Noventech Rails standard stack, even if they only ask a first question such as "can we convert this to Rails?" or "what do you need from me to rewrite this in Ruby?".
---

# Converting an app to Rails on Joe's Noventech template

This skill is the playbook from the first conversion (the AI Governance Deployment Tracker, Python/customtkinter →
Rails, Oct 2026). It worked: 45 tables, ~23k lines, five phases, 1,474 tests, data and outputs verified identical to the
original. It also went wrong in one big way: **the UI/UX was quietly simplified and restyled, and nobody looked at a
screen until the end.** The steps below are ordered so that doesn't happen again.

Read `references/lessons.md` once before starting; it lists the concrete mistakes and their fixes.

## The shape of the work

1. **Set up** the template, the dev environment and the new repo (`references/environment.md`).
2. **Inventory the source app**, including how it looks and behaves, not just its code.
3. **Write the porting plan** as a shared doc for the person and Joe, and get the open decisions answered.
4. **Port in phases**, each with a gate checked against the original app, by delegating to subagents in worktrees.
5. **Review and merge every branch yourself** (`references/review-checklist.md`).
6. **Hand over**: status, what's blocked on whom, a click-through, and records (decision register, progress log).

## 1. Set up

Clone the template (HTTPS clone works without login) and read its `README.md`, `template.rb`, `recipes/`,
`files/CONVENTIONS.md.tt` and `files/CLAUDE.md.tt`. The conventions are binding and shape the whole port:
- No `app/services`: business logic goes in models, concerns, POROs under `app/models`, API clients under `app/models`.
- Controllers use only the seven REST actions; anything else is a nested resource. Routes always pass `only:`.
- Views use the `tw_*` Tailwind helpers; every colour has a `dark:` pair.
- Any new gem needs Joe's approval: list them early, they gate whole features (Word/PDF, MCP, zip, csv).

The template assumes Linux (bash, mise, Solid Queue forks). On Windows use WSL2 + Ubuntu; see
`references/environment.md` for the exact setup, the GitLab repo creation, and the shell gotchas that cost hours.

## 2. Inventory the source app — behaviour AND appearance

Before planning, collect:
- **Data**: the final schema (dump it from a freshly migrated database, don't read migrations), the export/import format.
- **Logic**: every service/module with line counts and a one-line purpose; the source app's tests.
- **Catalogs/config** the app treats as data (they usually copy across unchanged and stay the source of truth).
- **Integrations**: external APIs, how secrets are held today, what writes to customer systems.
- **UI/UX reference set** — this is the step that was skipped last time:
  - a screenshot of every screen and important state (empty, populated, error, modal open), from the real app;
  - the theme: colours, fonts, spacing, status tones (look for a theme file, e.g. `theme.py`);
  - interaction details: keyboard shortcuts, inline editing, side panels vs pages, what opens where, live updates;
  - any UI review docs or mockups the team already has.
  Save these in the new repo under `docs/porting/ui/` so every agent can see them. If you can't capture screenshots
  yourself, ask the person for them now; it is cheaper than redoing screens later.

## 3. The porting plan (a shared doc)

Use the docs connector (or an Artifact page) so the person can share it with Joe. Sections that worked:
summary · what changes going desktop→web · data model (tables → models) · services → models · screens → controllers
(custom actions recast as nested resources) · catalogs/reports/integrations · **UI/UX: theme and per-screen layout
parity** · gems needing approval · phases with gates · open questions.

Ask these decisions up front (each one bit us when asked late):
- Who uses it and who sees what (per-client access or everyone sees everything)?
- Hosting (the template ships Kamal), domain, internal or VPN.
- **Time zone** — Rails defaults to UTC, so "today" rolls over in the US afternoon. Set `config.time_zone` in phase 1.
- Where secrets live (encrypted Rails credentials on the server, never the DB) and who may trigger writes to customer systems.
- Which gems Joe needs to approve, and whether optional features (e.g. an MCP server) are actually used.
- Whether the old app stays in use during the port (usually yes, until the last gate).

Phases that worked: 1 foundation (schema, models, catalog loader, **theme**, main lists, import of the old export format)
· 2 core workflow screens · 3 registers/secondary screens · 4 external integrations · 5 outputs/reports, extras, go-live.
Each phase's gate is checked against the original app with real data.

## 4. Delegating to subagents

Only delegate when the person asks for it (they did last time: "use the optimal model for each task, then review").

- **One git worktree per agent** under `~/wt/<name>` on branch `<phase>/<name>`, symlink `config/master.key`, run
  `db:prepare`. Scripts in `scripts/` (`wt_add.sh`, `merge_branch.sh`, `sync_branch.sh`, `finish_sync.sh`,
  `show_conflicts.sh`, `jscopy.sh`) do this; copy them to your scratchpad and run them through `wsl.exe -d Ubuntu -- bash -l`.
- **Model choice**: Opus for the data model, import/export fidelity, complex domain logic, anything that writes to
  customer systems or holds secrets, and the API client foundation. Sonnet for screens on top of a documented model API,
  CRUD registers, reports ported from templates, tours/help/seeds.
- **Sequence**: foundation first (alone), then parallel agents on disjoint areas. A shared base (API clients, a register
  UI helper, the theme) goes first and documents itself (e.g. `docs/porting/CIPP.md`) for the agents that follow.
- **Every brief** follows `references/agent-brief.md`. The non-negotiables in it: the exact worktree and how to run
  commands, files are written only via the `\\wsl.localhost\...` path, commit after each step, `git merge main` before
  finishing, stop and report if a permission check blocks anything, **match the original's layout and theme using the
  reference screenshots, and list every UI deviation for approval** rather than simplifying silently.
- **Give agents eyes for UI work.** Each UI agent runs its own branch on a private port in the background
  (`bin/rails server -p 31xx -d`, `bin/rails tailwindcss:build` after class changes), screenshots it with the bundled
  `scripts/ui-shots/shots.mjs` (Windows node + Playwright driving the installed Edge, signing in as a development-only
  user via `screens_user.rb` / `otp.rb`), reads the PNGs and compares them with the source app's reference screenshots.
  Without this, agents build screens blind and simplify. See `references/screenshots.md`.

## 5. Reviewing and merging

You own quality; agents' reports are claims to verify. Follow `references/review-checklist.md`. In short: rerun CI,
read the risky code, **diff behaviour against the original app with real data** (round-trip the export, compute the same
outputs in both apps and diff them), check security rules by trying to break them, compare screens against the reference
screenshots, then merge with the CI gate and push. Fix merge conflicts and tests that went stale from the merge yourself
(get the person's OK for this once); for any other action an agent was blocked from, ask the person — never do it for
the agent.

## 6. Hand over

- Status by phase with gates, what's blocked on whom (Joe: gems, hosting, test tenants/credentials).
- A click-through: `bin/rails db:migrate && bin/rails db:seed:demo && bin/dev`, sign in, set up 2FA (1Password can scan
  the QR code from the page), demo client loaded.
- Record decisions in the team's decision register and a pointer in the old app's progress log.
- Ticket updates: as short as possible, owners' checklists first.
