#!/usr/bin/env bash
# Set APP_DIR to the main checkout (default: ~/app), e.g. APP_DIR=~/ai-governance-tracker.
# Usage: PHASE=phase2 wt_add.sh name [name...]  - create ~/wt/<name> on branch <phase>/<name> from main.
PHASE="${PHASE:-phase1}"
cd "${APP_DIR:-$HOME/app}" || exit 1
for n in "$@"; do
  git worktree add -q -b "$PHASE/$n" ~/wt/"$n" main
  ln -sf "${APP_DIR:-$HOME/app}"/config/master.key ~/wt/"$n"/config/master.key
  (cd ~/wt/"$n" && bin/rails db:prepare >/dev/null 2>&1)
done
git worktree list
