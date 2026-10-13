#!/usr/bin/env bash
# Usage: jscopy.sh <worktree> - copy the branch's new/changed Stimulus controllers to the scratchpad as .mjs for node --check.
S="${JSCHECK_DIR:?set JSCHECK_DIR to a /mnt/c/... folder}"
rm -rf "$S"; mkdir -p "$S"
cd ~/wt/"$1" || exit 1
echo "uncommitted: $(git status --short | wc -l)"
for f in $(git diff --name-only main...HEAD -- 'app/javascript/*.js'); do cp "$f" "$S/$(basename "$f" .js).mjs"; echo "$f"; done
