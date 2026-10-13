# Subagent brief template

Fill the brackets. Keep the environment and rules sections verbatim; they prevent the failures listed in lessons.md.

```
You are porting [source app, one line] to Rails. [What's already merged.] Your job: [area] — [domain logic and/or
screens], [what's explicitly out of scope and why].

## Where things are
- Your worktree (branch `[phase]/[name]`): WSL `/home/[user]/wt/[name]`, Windows `\\wsl.localhost\Ubuntu\home\[user]\wt\[name]`.
  Work ONLY here.
- Write and edit files only with the Write/Edit tools on the `\\wsl.localhost\...` path. In the Bash tool, `~` and `/tmp`
  are Windows paths: never write project files from Bash, never `rm` outside the worktree.
- Run Ruby inside WSL from PowerShell: `wsl.exe -d Ubuntu -- bash -lc "cd ~/wt/[name] && bin/rails test"`. PowerShell
  mangles quotes and `$` — for anything non-trivial write a .sh into the worktree's `tmp/` and run it with
  `wsl.exe -d Ubuntu -- bash -l /home/[user]/wt/[name]/tmp/x.sh`. Use `timeout`; never start servers.
  JS syntax: copy to `.mjs` on Windows and `node --check`.
- READ FIRST (binding): `CONVENTIONS.md`, `CLAUDE.md`, `docs/porting/PLAN.md`, `docs/porting/RENAMES.md`
  [, `docs/porting/<shared API doc>.md`].
- Existing pieces to use, not rebuild: [models, POROs, helpers, concerns, test helpers].
- Source reference (read-only, never edit): [path]: [files with what each holds], tests [paths] (port all), docs [paths].
- UI reference: `docs/porting/ui/[screen]*.png` and the theme tokens. Match the original exactly: layout, information
  density, tables vs cards, menus, dialogs, keyboard shortcuts, colours, date formats, what opens where. Deviate only where
  the web platform makes it impossible or the template conventions forbid it, and give that reason. Your own preferences
  and "out of time" are not reasons: build it, or report it as not done. Never remove something Joe's template ships
  (e.g. the light/system/dark theme switch, 2FA, the menu DSL) to match the original: keep it, defaulting to the
  original's choice.

## Build
[Domain: classes and methods, the rules that must hold, stored values identical to the source.]
[Screens: REST resources, which actions become nested resources, which shared files you may touch (minimal, separate).]
[Tests: port the source tests, model tests per rule, controller tests per controller, parity tests on real fixtures.]

## Rules
No new gems, no `app/services`, REST only, `params.expect`, `tw_*` helpers, dark mode, `lock_version` on edit forms.
Tests derive counts from shared lists, never hard-code them. Commit after each logical step (end messages with the
session's Co-Authored-By line). Before finishing: `git merge main`, resolve, re-run `bin/ci` (must pass). Don't push or
merge to main; don't touch other worktrees. If any command or edit is blocked by a permission check, stop and report it —
don't work around it and don't try to clean up outside the worktree.

## Report back (concise)
Commits; routes; domain API; source tests ported (count, skipped with reason); logic deviations; UI deviations;
`bin/ci` result; anything undone.
```
