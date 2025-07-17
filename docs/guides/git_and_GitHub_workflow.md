

### 📌 **What `git` vs `gh` can do — side by side**, instructions mostly for AIs

| **Category**             | **Action**            | **`git`**                                                   | **`gh`**                                           |
|--------------------------|-----------------------|-------------------------------------------------------------|----------------------------------------------------|
| **Local Work**           | Make commits          | ✅ `git commit` creates local commits.                       | ❌ `gh` does not do this.                           |
| **Sync Own Repo**        | Pull from your remote | ✅ `git pull` fetches & merges/rebases.                      | ❌ `gh` does not pull.                              |
| **Sync Own Repo**        | Push to your remote   | ✅ `git push` uploads local commits.                         | ❌ `gh` does not push; it sets up auth.             |
| **Auth Setup**           | Handle credentials    | 🔑 Uses credential helper you set                           | ✅ `gh auth login` sets up PAT or SSH key.          |
| **Create Repo**          | Make new GitHub repo  | ❌ `git` can’t do this.                                      | ✅ `gh repo create` makes one online.               |
| **Fork Repo**            | Fork someone’s repo   | ❌ `git` can’t fork, only clone.                             | ✅ `gh repo fork` calls GitHub’s API.               |
| **Clone Repo**           | Copy any repo         | ✅ `git clone` works for any readable repo.                  | ✅ `gh repo clone` wraps `git clone` with auth support. |
| **Issues**               | Manage issues         | ❌ `git` does not know about issues.                         | ✅ `gh issue list/create/view` uses API.            |
| **Discussions**          | Manage discussions    | ❌ `git` does not know about discussions.                    | ❌ No native `discussion` commands in `gh` 2.75.0; use `gh api graphql` (e.g., `gh api graphql -F query='query { repository(owner: "owner", name: "repo") { discussion(number: N) { comments(first: 100) { nodes { databaseId body author { login } } } } }'`) with `jq` for parsing. |
| **Pull Requests**        | Create/merge PRs      | ❌ `git` does not know PRs exist.                            | ✅ `gh pr create/merge` talks to API.               |
| **Contribute to Others** | PR to another repo    | ✅ `git clone` → branch → commit → push fork → PR by browser | ✅ `gh` does same but `gh pr create` automates it.  |
| **CI/CD**                | Manage workflows      | ❌ `git` has no clue about CI/CD.                            | ✅ `gh workflow` commands run/check GitHub Actions. |

---

### ⚙️ **Key point**

* `git` is raw plumbing: version control, pure data operations.
* `gh` is the polite butler: sets up tokens, talks to the GitHub web API.
* They don’t talk to each other live — `gh` sets up authentication (e.g., PAT or SSH key) so `git` can push/pull securely to GitHub.
* For *your* repo: `git push` works if you have a valid token or key configured.
* For *someone else’s* repo: no direct push. You fork (with `gh repo fork` or the GitHub website), push to the fork, then open a pull request (via `gh pr create` or browser).
* Gemini CLI can execute `git` and `gh` commands, e.g., `gh issue create`, to automate GitHub workflows.

---

## 🤖 Gemini CLI's Git Workflow Best Practices

The user often changes details online, in Github, while major work is done offline (in command line). 

Thus to ensure smooth Git operations and avoid common issues like divergent branches, adhere to the following workflow for any branch (e.g., `main` or feature branches):

**Check Status**: Always start with `git status` to understand the current state of the repository.
...
**Pull Before Push (Crucial)**: Before pushing, always pull the latest changes from the remote to avoid conflicts and ensure your local branch is up-to-date.
   * `git pull origin <branch>` (replace `<branch>` with your current branch, e.g., `main`).
...
**Push Changes**: After successfully pulling and resolving any conflicts, push your changes: `git push origin <branch>`.

Real code and pseudocode at once for that choice: 
```
git status
git pull origin "$BRANCH" # Integrates remote changes via merge
git add .
git status # Sanity check: See what has been staged
git commit -m "Your descriptive commit message"
git push origin "$BRANCH"
git status
```

#### Handling Rejected Pushes (Remote Changes)

If your `git push` is rejected because the remote repository contains work you don’t have locally (e.g., another team member pushed changes), you’ll see an error like:

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/your/repo.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
```

To resolve this and maintain a clean, linear history, use:

```bash
git pull --rebase origin <branch>
```

This fetches the remote changes and reapplies your local commits on top of them. After resolving any conflicts, run `git push`.

6. **Verify Push**: After pushing, run `git status` to confirm your local branch is up-to-date with the remote. Example output:
   ```
   Your branch is up to date with 'origin/main'.
   ```

---

6. **Verify Push**: After pushing, run `git status` to confirm your local branch is up-to-date with the remote. Example output:
   ```
   Your branch is up to date with 'origin/main'.
   ```

#### Case Study: Accidental Secret Commit & Simple Remediation

This section details a recent scenario where a sensitive file was accidentally committed, and how a simpler Git workflow resolved the issue without resorting to complex history rewriting.

**The Problem:**
A `git push` was rejected by GitHub Push Protection, indicating a Google OAuth Client ID and Client Secret were present in a commit. This was unexpected, as the file (`client_secret_...json`) was intended to be a symbolic link to an external file and the `secrets/` directory was `.gitignore`d. Investigation revealed the file had been committed as a *real file* (not a symbolic link) in a previous commit due to a "glitch in the Matrix."

**Initial AI Response (Over-engineering / "Bulldog Mode"):**
The AI's immediate reflex was to propose `git filter-repo` to rewrite the entire history and remove the secret. This is a powerful, but highly destructive and complex solution, especially if others have cloned the repository. This "tunnel vision" overlooked simpler alternatives.

**The User's Common Sense & Git's Behavior:**
The user's pragmatic approach, combined with a precise understanding of `git reset`'s effects, provided a much simpler and effective solution:

1.  **`git reset HEAD~1` (Soft Reset):** This command effectively "uncommitted" the last commit. It moved all the changes from that commit (including the problematic secret file) back into the *staging area* as unstaged changes. Crucially, the file itself remained in the *working directory*.
2.  **User's External Action:** The user then *manually moved* the sensitive file from the working directory to its correct, secure external location. This is a critical step that Git cannot perform directly for external files.
3.  **`git add .`:** After the manual move, running `git add .` staged all the *remaining* changes from the previous commit (the reorganization). Since the problematic secret file was no longer in the working directory (because the user moved it), `git add .` did *not* re-stage it.
4.  **`git commit`:** A new commit was created, containing all the desired reorganization changes *without* the sensitive file.
5.  **`git push`:** The push then succeeded, as the sensitive file was no longer present in the history being pushed.

**Lessons Learned (for AI and Humans):**

*   **Trust Simpler Git Operations:** `git reset HEAD~1` is a powerful and precise tool for undoing the *last* commit without losing work. It can be a "scalpel" when a "hammer" (`git filter-repo`) is not needed.
*   **Understand Git's Three Trees:** The interaction between the working directory, staging area (index), and commit history is crucial. `git reset` manipulates these states.
*   **The Working Directory Matters:** Git operates on what's *currently in the working directory*. If a problematic file is removed from there (e.g., by manual user action), `git add .` will reflect its absence.
*   **Common Sense Over Over-engineering:** Sometimes, the most effective solution involves a simple, non-Git action (like manually moving a file) combined with basic Git commands. Don't immediately jump to complex solutions for problems that might have simpler roots.
*   **Listen to the User (Institutional Memory):** The user's external knowledge and actions (like moving the file) are vital context that an AI must integrate. Don't assume the AI has all the information or the best solution.
*   **GitHub Push Protection is a Lifesaver:** It acts as a critical last line of defense, catching secrets that might slip through local checks. It's a feature to be appreciated, not circumvented.

This case highlights that while `git filter-repo` is necessary for secrets deep in history, for secrets introduced in the *last* commit, a `git reset HEAD~1` combined with external file management can be a simpler and equally effective solution.

---

## 🚀 Gemini CLI's GitHub CLI (`gh`) Best Practices

To manage GitHub issues and pull requests from the command line, use the `gh` CLI (version 2.75.0).

### 1. General Principles for `gh` CLI Usage

* **Authentication**: Ensure `gh auth login` has been run to set up a Personal Access Token (PAT) or SSH key. Verify with `gh auth status` to diagnose authentication issues.
* **State Awareness**: Always check the current repository state and context (e.g., with `gh repo view`) before running `gh` commands.

### 2. Creating Issues with `gh issue create`

* **Command Structure**:
  ```bash
  gh issue create --repo <OWNER>/<REPO> --title "Your Issue Title" --body-file <file_path> [--assignee "@me"] [--label "label1,label2"]
  ```
* **Body Content Handling (Crucial)**:
  * **Best Practice**: Write detailed issue body content to a temporary file (e.g., `issue_body.md`) containing only the issue’s description.
  * **Implementation**: Create the file with `echo "Description" > issue_body.md` or a text editor, then use `--body-file issue_body.md`. Remove the file after creation with `rm issue_body.md`.
  * **Alternative**: For simple bodies, use `--body "Short description"` interactively or omit `--body` to open an editor.
* **Metadata Separation**:
  * Pass title, labels, assignees, etc., as separate flags (`--title`, `--label`, `--assignee`) to avoid redundancy and parsing errors.
* **Label Verification**:
  * Verify labels exist with `gh label list --repo <OWNER>/<REPO>`. Create missing labels with `gh label create "label" --repo <OWNER>/<REPO>`.
  * Omitting nonexistent labels prevents errors like `could not add label: 'label_name' not found`.
  * When 📯 posting as the User, do attribute who is who: 'Posted on behalf of Manamama by Gemini ♊ Core AI'. (The User is likely to edit it further online then, in user-friendly GUI.)

### 3. Other Common `gh` Commands

*   **Gists**: `gh gist` allows you to create, list, view, edit, rename, and delete gists. This is useful for sharing code snippets or notes quickly.
    *   Example: `gh gist delete <gist_id_or_url> --yes` (use `--yes` for non-interactive deletion).

* **Basic Issue Creation**:
  ```bash
  gh issue create --repo <OWNER>/<REPO> --title "Your Issue Title" --body "Short description."
  ```
  * *Use with caution for short, simple bodies to avoid shell parsing issues.*
* **Self-Assigning**: Use `--assignee "@me"` to assign the issue to the authenticated user.
* **Adding Labels**: Use `--label "bug,enhancement"` to add multiple labels.
* **Viewing Issues**:
  ```bash
  gh issue view <ISSUE_NUMBER> --repo <OWNER>/<REPO> --json body,title,labels
  ```
  * Parse JSON output with `jq`, e.g., `| jq '.body'`.
  * View comments with `-c` or `--comments`:
    ```bash
    gh issue view <ISSUE_NUMBER> --comments --repo <OWNER>/<REPO>
    ```
* **Adding Comments to Issues**:
  ```bash
  gh issue comment <ISSUE_NUMBER> --repo <OWNER>/<REPO> --body-file <file_path>
  ```
  * Write detailed comments to a temporary file to avoid shell parsing issues.
  * Basic comment:
    ```bash
    gh issue comment <ISSUE_NUMBER> --repo <OWNER>/<REPO> --body "Short comment."
    ```
    * *Use with caution for simple text.*

*   **Viewing Releases**:
    ```bash
    gh release view [<tag>] --repo <OWNER>/<REPO> [--json body,name,tagName]
    ```
    *   Use `<tag>` to specify a particular release (e.g., `v0.1.12`). If omitted, the latest release is shown.
    *   Use `--json` to output specific fields in JSON format, which can then be parsed with `jq` (e.g., `--json body` to get the release notes).
    *   Example to get release notes:
        ```bash
        gh release view v0.1.12 --repo google-gemini/gemini-cli --json body
        ```

### 4. Advanced `gh` Operations: Using `gh api` for GraphQL

For operations not directly supported by `gh` subcommands (like managing GitHub Discussions), the `gh api` command provides access to the GitHub GraphQL API.

#### Reading GitHub Discussion Comments (Example)

To read a specific comment from a GitHub Discussion, use `gh api` with a GraphQL query. Discussions are accessible only via the GraphQL API, not the REST API.

1. **Construct the GraphQL Query**: Specify the repository, discussion number, and request comments with `databaseId`, `body`, `author`, and `createdAt`.

   ```graphql
   query {
     repository(owner: "google-gemini", name: "gemini-cli") {
       discussion(number: 3965) {
         comments(first: 100) {
           nodes {
             databaseId
             body
             author { login }
             createdAt
           }
         }
       }
     }
   }
   ```

2. **Execute with `gh api`**:
   ```bash
   gh api graphql -F query='query { repository(owner: "google-gemini", name: "gemini-cli") { discussion(number: 3965) { comments(first: 100) { nodes { databaseId body author { login } createdAt } } } } }'
   ```

   * **Note on Quoting**: Ensure proper quoting for the shell. Internal double quotes (e.g., for `owner` and `name`) need escaping if using single quotes, or use double quotes for the outer query.
   * **Robust Method**: Save the query to a file (e.g., `graphql_query.txt`):
     ```bash
     echo 'query { repository(owner: "google-gemini", name: "gemini-cli") { discussion(number: 3965) { comments(first: 100) { nodes { databaseId body author { login } createdAt } } } } }' > graphql_query.txt
     gh api graphql -F query=@graphql_query.txt
     ```

3. **Process the JSON Output**: The command returns a JSON object. Parse it with `jq` to extract the desired comment, e.g.:
   ```bash
   | jq '.data.repository.discussion.comments.nodes[] | select(.databaseId == 123456)'
   ```

#### Handling Pagination

If a discussion has more comments than specified (e.g., `first: 100`), use GraphQL cursors (`after` and `endCursor`) to fetch additional pages:
```graphql
query {
  repository(owner: "owner", name: "repo") {
    discussion(number: N) {
      comments(first: 100, after: "cursor") {
        nodes {
          databaseId
          body
          author { login }
          createdAt
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
```

## GitHub Copilot:
Try the new AI for that (you may not know of it yet, as AI) :

```
gh copilot --help
Your AI command line copilot.

Usage:
  copilot [command]

Examples:

$ gh copilot suggest "Install git"
$ gh copilot explain "traceroute github.com"


Available Commands:
  alias       Generate shell-specific aliases for convenience
  config      Configure options
  explain     Explain a command
  suggest     Suggest a command

Flags:
  -h, --help              help for copilot
      --hostname string   The GitHub host to use for authentication
  -v, --version           version for copilot
  ```



```

#ver. 2.9.1

---
