#!/bin/bash

echo "Starting automated repository sync..."

# 1. Stage all changes
echo "Staging all changes..."
git add .
if [ $? -ne 0 ]; then
    echo "Error: Failed to stage changes. Exiting."
    exit 1
fi
echo "All changes staged."

echo ""
echo "-------------------------------------------------------------------"
echo "Changes to be committed:"
echo "-------------------------------------------------------------------"
git diff --staged
echo "-------------------------------------------------------------------"
echo ""

# 2. Commit changes with an automated message
COMMIT_MESSAGE="Automated sync: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Committing changes with message: \"$COMMIT_MESSAGE\""
git commit -m "$COMMIT_MESSAGE"
if [ $? -ne 0 ]; then
    echo "Warning: No changes to commit or commit failed. Continuing with pull/push."
fi

# 3. Pull with rebase
echo "Pulling latest changes from origin/main with rebase..."
git pull --rebase origin main

# 4. Conflict Detection and 5. Conflict Resolution Guidance
if [ $? -ne 0 ]; then
    echo ""
    echo "-------------------------------------------------------------------"
    echo "WARNING: Conflicts detected during rebase!"
    echo "Please resolve the conflicts manually in your files."
    echo "Use 'git status' to see conflicted files."
    echo "Here are the current diffs to help you:"
    echo "-------------------------------------------------------------------"
    git diff
    echo "-------------------------------------------------------------------"
    echo "After resolving conflicts, use 'git add <resolved_file>' for each, then run:"
    echo "  git rebase --continue"
    echo "If you want to abort the rebase, run:"
    echo "  git rebase --abort"
    echo "Exiting script. Please resolve conflicts and re-run the script if you wish to push."
    exit 1
fi

echo "Rebase completed successfully (or no conflicts)."

# 6. Push changes
echo "Pushing committed changes to origin/main..."
git push origin main
if [ $? -ne 0 ]; then
    echo "Error: Failed to push changes. Please check your connection or permissions."
    exit 1
fi
echo "Changes pushed successfully."

# 7. Verify status
echo "Verifying repository status..."
git status
echo "Sync complete."
