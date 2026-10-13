#!/usr/bin/env bash
# Usage: show_conflicts.sh <worktree> - print each conflict hunk with context.
cd ~/wt/"$1" || exit 1
for f in $(git diff --name-only --diff-filter=U); do
  echo "=== $f"
  awk '/^<<<<<<</{p=1; print NR": "$0; next} p{print NR": "$0} /^>>>>>>>/{p=0; print "---"}' "$f"
done
