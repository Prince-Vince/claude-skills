# Review checklist for each agent branch

1. **State**: worktree clean, commits as reported (`git log main..HEAD`, `git diff --stat main...HEAD`).
2. **Sync**: `scripts/sync_branch.sh <name>` merges main; resolve conflicts keeping both sides (tabs, routes, concerns);
   `scripts/finish_sync.sh <name>` commits and runs CI.
3. **CI yourself**: don't trust the report's numbers.
4. **Conventions**: public controller methods are only REST actions; routes pass `only:`; no `app/services`.
5. **Read the risky code**: anything that writes externally, handles secrets, parses input files, runs JS in the browser.
6. **Parity with the source, using real data** (keep these scripts in the scratchpad and reuse them):
   - import the source's real export and compare every table/column/value;
   - compute the same outputs in both apps (progress numbers, generated templates and fingerprints, scripts, reports
     as plain text) and diff; any difference must be explained (timestamps, a source bug kept or fixed on purpose);
   - regenerate any "expected values" file an agent committed, using the source app, and diff.
7. **Security, by trying to break it**: unauthenticated access to files and pages, read-only clients writing, secrets in
   logs/errors/params, CSV formula injection, frames/links targeting, browser storage access in try/catch, raw HTML
   injection in JS.
8. **UI/UX**: compare the branch's screens with `docs/porting/ui/` screenshots (headless browser or the person). Every
   UI deviation either matches the original or has the person's OK.
9. **JS**: `scripts/jscopy.sh <name>` then `node --check` each copied `.mjs`.
10. **Merge**: `scripts/merge_branch.sh <name> <branch> "<message>"` (CI gate, push, remove worktree).
11. **Tell the remaining agents** what changed in main that affects them (shared helpers, renamed APIs, counts keys).
12. **Record**: memory/progress notes; decisions that came up go to the decision register.
