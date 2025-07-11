### 📌 **What `git` vs `gh` can do — side by side**

| **Category**             | **Action**            | **`git`**                                                   | **`gh`**                                           |
| ------------------------ | --------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| **Local Work**           | Make commits          | ✅ `git commit` creates local commits.                       | ❌ `gh` does not do this.                           |
| **Sync Own Repo**        | Pull from your remote | ✅ `git pull` fetches & merges/rebases.                      | ❌ `gh` does not pull.                              |
| **Sync Own Repo**        | Push to your remote   | ✅ `git push` uploads local commits.                         | ❌ `gh` does not push; it sets up auth.             |
| **Auth Setup**           | Handle credentials    | 🔑 Uses credential helper you set                           | ✅ `gh auth login` sets up PAT or SSH key.          |
| **Create Repo**          | Make new GitHub repo  | ❌ `git` can’t do this.                                      | ✅ `gh repo create` makes one online.               |
| **Fork Repo**            | Fork someone’s repo   | ❌ `git` can’t fork, only clone.                             | ✅ `gh repo fork` calls GitHub’s API.               |
| **Clone Repo**           | Copy any repo         | ✅ `git clone` works for any readable repo.                  | ✅ `gh repo clone` wraps `git clone`.               |
| **Issues**               | Manage issues         | ❌ `git` does not know about issues.                         | ✅ `gh issue list/create/view` uses API.            |
| **Pull Requests**        | Create/merge PRs      | ❌ `git` does not know PRs exist.                            | ✅ `gh pr create/merge` talks to API.               |
| **Contribute to Others** | PR to another repo    | ✅ `git clone` → branch → commit → push fork → PR by browser | ✅ `gh` does same but `gh pr create` automates it.  |
| **CI/CD**                | Manage workflows      | ❌ `git` has no clue about CI/CD.                            | ✅ `gh workflow` commands run/check GitHub Actions. |

---

### ⚙️ **Key point, no sugarcoating**

* `git` is raw plumbing: version control, pure data ops.
* `gh` is the polite butler: sets up tokens, talks to the GitHub *web API*.
* They don’t talk to each other live — `gh` just wires up the keys so `git` can push/pull securely.
* For *your* repo: `git push` works if you have a valid token/key.
* For *someone else’s* repo: no direct push. You fork (with `gh` or website), push *to the fork*, then open a PR (browser or `gh`).

Gemini CLI can operate both, e.g. `gh issue` 

## 🤖 Gemini CLI's Git Workflow Best Practices

To ensure smooth Git operations and avoid common issues like divergent branches, I will adhere to the following workflow:

1.  **Check Status:** Always start with `git status` to understand the current state of the repository.
2.  **Stage Changes:** Use `git add <file>` or `git add .` to stage changes for commit.
3.  **Commit Changes:** Create meaningful commits with `git commit -m "Your descriptive commit message"`.
4.  **Pull Before Push (Crucial):** Before pushing, always pull the latest changes from the remote to avoid conflicts and ensure your local branch is up-to-date.
    *   `git pull origin main` (or your current branch name)
    *   If a "divergent branches" error occurs, use `git pull --rebase origin main` to rebase your local commits on top of the remote's history. This keeps the commit history clean.
5.  **Push Changes:** After successfully pulling and resolving any conflicts (if necessary), push your changes to the remote: `git push origin main` (or your current branch name).
6.  **Verify Push:** After pushing, run `git status` again to confirm that your local branch is up-to-date with the remote.

This workflow prioritizes pulling and rebasing before pushing to maintain a linear and clean commit history, especially when working in a collaborative environment or when the remote might have been updated by others.

## 🚀 Gemini CLI's GitHub CLI (`gh`) Best Practices

To manage GitHub issues and pull requests directly from the command line, I will use the `gh` CLI.

### 1. General Principles for `gh` CLI Usage

*   **Authentication:** Ensure `gh auth login` has been successfully run to set up PAT or SSH key for authentication. Operations requiring authentication will fail otherwise.
*   **State Awareness:** Always be aware of the current repository state and the context of the `gh` command being executed.

### 2. Creating Issues with `gh issue create`

*   **Command Structure:**
    `gh issue create --repo <OWNER>/<REPO> --title "Your Issue Title" --body-file <file_path> [--assignee "@me"] [--label "label1,label2"]`
*   **Body Content Handling (Crucial):**
    *   **Best Practice:** Always write the detailed issue body content to a temporary file first.
    *   **Reasoning:** Passing multi-line or complex text directly to the `--body` flag can lead to `bash: syntax error` due to shell misinterpretation of special characters (e.g., parentheses, quotes) within the text.
    *   **Implementation:** Use `write_file` to create a temporary markdown file (e.g., `issue_body.md`) containing *only* the issue's description. Then, use `--body-file /path/to/issue_body.md` to provide the content.
    *   **Cleanup:** Remember to remove the temporary file after the issue is successfully created.
*   **Metadata Separation:**
    *   **Best Practice:** Title, labels, assignees, and other issue metadata must be passed as separate command-line arguments (`--title`, `--label`, `--assignee`, etc.), not embedded within the `--body-file` content.
    *   **Reasoning:** Including metadata within the body file leads to redundancy (e.g., duplicated title) and can cause errors with `gh` CLI parsing.
*   **Label Verification:**
    *   **Best Practice:** Before attempting to add labels (`--label "label1,label2"`), verify that these labels already exist in the target GitHub repository.
    *   **Reasoning:** Applying non-existent labels will result in a `could not add label: 'label_name' not found` error. If labels are not found, either omit them or inform the user.

### 3. Other Common `gh` Commands

*   **Basic Issue Creation (without file):**
    `gh issue create --repo <OWNER>/<REPO> --title "Your Issue Title" --body "Detailed description of the issue."`
    *   *Use with caution for short, simple bodies to avoid shell parsing issues.*
*   **Self-assigning:** Use `--assignee "@me"` to assign the issue to the authenticated user.
*   **Adding Labels:** Use `--label "bug,enhancement"` to add multiple labels.
*   **Viewing Issues:** `gh issue view <ISSUE_NUMBER> --repo <OWNER>/<REPO> --json body,title,labels`

#ver. 1.6
