#!/usr/bin/env bash
# Usage: finish_sync.sh <worktree> - after resolving conflicts: check no markers remain, commit, run CI.
cd ~/wt/"$1" || exit 1
if git diff --name-only --diff-filter=U | xargs -r grep -l '^<<<<<<<\|^>>>>>>>' ; then echo "MARKERS LEFT"; exit 1; fi
git add -A
git commit -q -m "Merge main into $(git branch --show-current)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git log --oneline -1
bin/rails db:migrate >/dev/null 2>&1
timeout 500 bin/ci 2>&1 | grep -E 'runs,|Continuous|offenses|Failure' | tail -4
