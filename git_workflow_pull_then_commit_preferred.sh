#!/bin/bash

# Philosophy: "Pull First, Then Commit" (Merge-based, True History)
# This workflow ensures local work is always based on the latest remote state.
# It integrates remote changes before local commits are finalized, allowing for early conflict resolution.
# It maintains a complete, auditable history with merge commits.
# Untracked files are generally safe as Git operations primarily affect tracked files.

# Assume <branch> is set, e.g., main or current branch name

git status
git pull origin "$BRANCH" # Integrates remote changes via merge
git add .
git status # Sanity check: See what has been staged
git commit -m "Your descriptive commit message"
git push origin "$BRANCH"
git status
