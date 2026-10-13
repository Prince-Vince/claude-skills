#!/usr/bin/env bash
# Usage: sync_branch.sh <worktree> - merge main into the worktree's branch; list conflicts, or run CI if clean.
cd ~/wt/"$1" || exit 1
echo "uncommitted: $(git status --short | wc -l)"
if ! git merge main -m "Merge main into $(git branch --show-current)" >/tmp/merge.log 2>&1; then
  tail -5 /tmp/merge.log
  echo "--- conflicts:"; git diff --name-only --diff-filter=U
  exit 2
fi
tail -1 /tmp/merge.log
bin/rails db:migrate >/dev/null 2>&1
timeout 500 bin/ci 2>&1 | grep -E 'runs,|Continuous|offenses|Failure' | tail -4
