#!/bin/bash

# Philosophy: "Commit First, Then Pull" (Merge-based, True History)
# This workflow prioritizes encapsulating local changes into a commit before integrating remote updates.
# It preserves a complete, auditable history with merge commits, reflecting all branching and merging events.
# Untracked files are generally safe as Git operations primarily affect tracked files.

# Assume <branch> is set, e.g., main or current branch name

git status
git add .
git status # Sanity check: See what has been staged
git commit -m "Your descriptive commit message"
git pull origin "$BRANCH" # Integrates remote changes via merge
git push origin "$BRANCH"
git status
