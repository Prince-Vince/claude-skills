# Matt Pocock's skills (third-party set)

Source: https://github.com/mattpocock/skills · package version 1.3.1 · upstream commit `49dd158` (2026-10-09) · synced 2026-10-13.

Upstream keeps them under `skills/<bucket>/<name>`; this repo keeps the same names flat under `skills/`. Every folder below is a
verbatim copy. Edit upstream copies only by re-syncing; put Noventech changes in a separate Noventech skill instead.

Engineering: ask-matt, code-review (excluded from Claude Code by link-skills.ps1), codebase-design, diagnosing-bugs, domain-modeling,
grill-with-docs, implement, implement-spec, improve-codebase-architecture, pr, prototype, research, retro, setup-matt-pocock-skills,
tdd, to-spec, to-tickets, triage, wayfinder, wizard.
Productivity: grill-me, grilling, handoff, teach, to-questionnaire, wait-what, writing-for-agents.
Misc: git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit.
In progress (beta): chief-of-staff, claude-handoff, loop-me, setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape.

Removed on 2026-10-13 because Matt retired them (his CHANGELOG names the replacement): design-an-interface (→ codebase-design),
edit-article and obsidian-vault (his personal skills), prd-to-plan (→ to-spec), qa (→ triage, to-tickets), request-refactor-plan
(→ to-spec, improve-codebase-architecture), resolving-merge-conflicts (nothing replaces it), triage-issue (→ triage),
ubiquitous-language (→ domain-modeling), write-a-skill.

## How to re-sync

```bash
git clone --depth 1 https://github.com/mattpocock/skills.git /tmp/mp
for d in /tmp/mp/skills/{engineering,productivity,misc,in-progress}/*/; do n=$(basename "$d"); rm -rf skills/$n; cp -r "$d" skills/$n; done
# then check /tmp/mp/CHANGELOG.md for "Remove" entries and delete those folders here; update this file; run .\link-skills.ps1
```
