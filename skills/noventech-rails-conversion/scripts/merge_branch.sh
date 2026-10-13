#!/usr/bin/env bash
# Set APP_DIR to the main checkout (default: ~/app), e.g. APP_DIR=~/ai-governance-tracker.
# Usage: merge_branch.sh <worktree-name> <branch> "<merge message>"
# Merges the branch into main, migrates, runs CI, pushes, removes the worktree. Stops on any failure.
set -e
NAME="$1"; BRANCH="$2"; MSG="$3"
cd "${APP_DIR:-$HOME/app}"
git merge -q --no-ff "$BRANCH" -m "$MSG"
bin/rails db:migrate >/dev/null
OUT=$(timeout 500 bin/ci 2>&1 || true)
echo "$OUT" | grep -E 'runs,|Continuous|failed|Failure' | tail -4
echo "$OUT" | grep -q "Continuous Integration passed" || { echo "CI FAILED - not pushing. The merge commit is on local main: fix forward, or undo with: git reset --hard ORIG_HEAD"; exit 1; }
git push -q origin main
git log --oneline -1
git worktree remove --force ~/wt/"$NAME"
git branch -d "$BRANCH"
