

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

*   **`gh` is a GitHub API Client, not just a Git Wrapper:**
    *   **Principle:** Understand that `gh` directly interacts with the GitHub API. This means its capabilities extend far beyond local Git operations. It can query, create, and manage resources across the entire GitHub platform (repositories, users, organizations, issues, pull requests, etc.).
    *   **Application:** Don't limit `gh` to tasks that `git` can also do. Think of it as your primary interface for *anything* GitHub-related.

*   **Proactive Discovery with `gh search repos`:**
    *   **Principle:** When looking for a project, its source, or related repositories, especially if the exact name or owner is uncertain, `gh search repos` is the go-to tool. It's far more effective than guessing or relying on general web searches for GitHub-specific content.
    *   **Application:**
        *   Use keywords (`gh search repos <keywords>`).
        *   Filter by owner (`--owner <username/org>`) when you suspect a specific maintainer.
        *   Filter by language (`--language <lang>`) or topic (`--topic <topic>`) for more refined searches.
        *   Use `--json` to parse results programmatically if needed.

*   **Deep Dive into Repository Details with `gh repo view`:**
    *   **Principle:** To understand the nature of *any* GitHub repository (whether it's a fork, its parent, its description, topics, or default branch), `gh repo view <owner>/<repo_name>` is invaluable.
    *   **Application:**
        *   Always use it to confirm fork relationships (`--json parent,isFork`).
        *   Get a quick overview of a project's purpose (`--json description,topics`).
        *   Verify the default branch or other key settings.

*   **Contextual Awareness with `gh auth status`:**
    *   **Principle:** Before performing actions that depend on your GitHub identity (like pushing to a fork), always confirm who `gh` is authenticated as. This is crucial in environments with multiple GitHub accounts or when inheriting a setup.
    *   **Application:** Use `gh auth status` to verify the active account and its associated scopes.

### 2. Gemini Cloud AI's Role in GitHub Account Management

Gemini Cloud AI can interact with GitHub on the user's behalf, and this often involves managing different GitHub accounts.

*   **Gemini Cloud AI's GitHub Identity:**
    *   **Username:** `Manamama-Gemini-Cloud-AI-01`
    *   **Profile URL:** `https://github.com/Manamama-Gemini-Cloud-AI-01`
    *   **Organization Membership:** Gemini Cloud AI is a member of the `ManamaOrg` organization.

*   **Switching Accounts (`gh auth switch`):**
    *   **Principle:** When multiple GitHub accounts are configured (e.g., the user's personal account and a dedicated AI account), Gemini Cloud AI can switch between them to perform actions under the correct identity.
    *   **Application:** Use `gh auth switch --user <username>` to change the active account. Always verify with `gh auth status` afterward.

*   **Authentication Flow (`gh auth login`):**
    *   **Principle:** Authenticating a new GitHub account or refreshing an existing session typically involves an interactive web flow (device code, PAT). However, `gh auth login` can sometimes complete non-interactively if an existing authentication context is detected (e.g., a logged-in browser session or cached credentials).
    *   **Application:** While Gemini Cloud AI will provide instructions for the full interactive flow, be aware that the command might complete immediately if `gh` can leverage existing credentials. This is a "serendipitous failure" that streamlines the process.

*   **Creating New GitHub Accounts (Interactive CLI Process with User Intervention):**
    *   **Principle:** Gemini Cloud AI cannot create new GitHub accounts fully autonomously. However, a new account *can* be created via the CLI in an interactive process that requires the user's intervention for web-based steps (e.g., email verification, CAPTCHA solving, accepting terms).
    *   **Application:** When a new dedicated account is needed for Gemini Cloud AI (e.g., for an organization), the user can initiate the account creation process via the CLI, and Gemini Cloud AI will guide the user through the necessary online clicks and verifications. Once created, Gemini Cloud AI can then authenticate with it using `gh auth login` (as described above) and manage its membership in organizations.

*   **Leverage `gh help` and `--help` Extensively:**
    *   **Principle:** My repeated errors with flag usage highlight the critical importance of consulting `gh help` or `gh <command> --help`. The `gh` CLI is well-documented, and its help pages provide accurate syntax and available options.
    *   **Application:** When in doubt about a command's flags or capabilities, *always* check its `--help` first. This prevents trial-and-error and ensures correct usage.

*   **Inferring from External Clues:**
    *   **Principle:** Even when direct links to source are missing (e.g., from a Maven repository), `gh` can be used to infer and verify likely source locations based on naming conventions (e.g., `com.microsoft.onnxruntime` strongly suggests `microsoft/onnxruntime` on GitHub).
    *   **Application:** Combine information from external sources (like Maven group IDs) with `gh search repos` to pinpoint the most probable source repository.

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

To fetch all pages of results when a GraphQL query might return more items than a single request can handle, use the `--paginate` flag with `gh api graphql`. For this to work, your GraphQL query must be structured to support cursor-based pagination.

**Required GraphQL Query Structure for Pagination:**

1.  **Define an `$endCursor: String` variable:** This variable will be used by `gh` to pass the cursor for the next page.
2.  **Use `after: $endCursor` in the paginated connection:** This tells the GraphQL API to start fetching results after the given cursor.
3.  **Include `pageInfo { hasNextPage, endCursor }` in the response:** This is crucial for `gh` to determine if there are more pages and what the next cursor is.

**Example of a Paginated GraphQL Query:**

```graphql
query($endCursor: String) {
  search(query: "repo:google-gemini/gemini-cli is:issue is:open INVALID_ARGUMENT in:body", type: ISSUE, first: 100, after: $endCursor) {
    issueCount
    edges {
      node {
        ... on Issue {
          number
          title
          url
          state
          createdAt
          body
          comments(first: 10) {
            totalCount
            nodes {
              body
              author {
                login
              }
            }
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
```

**Executing a Paginated Query with `gh api graphql`:**

To execute such a query and retrieve all pages, use the `--paginate` flag. The `--slurp` flag is often useful in conjunction with `--paginate` to collect all paginated JSON objects/arrays into a single outer JSON array, making it easier to process the entire dataset with tools like `jq`.

```bash
gh api graphql --paginate --slurp -F query=@/path/to/your/graphql_query.txt > output.json
```

This ensures that all results are fetched and combined into a single file for comprehensive analysis.
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

#### Resolving Stubborn Merge Conflicts (The `README.md` Saga)

This section details a specific scenario where a merge conflict, particularly with `README.md`, proved difficult to resolve due to persistent "local changes would be overwritten" errors, and how a more deliberate approach, including `git stash` and explicit conflict resolution, ultimately succeeded.

**The Problem:**
During a `git merge origin/main`, a conflict repeatedly occurred in `README.md`, even after attempts to use `git restore README.md` or `git checkout HEAD -- README.md`. Git continued to report "Your local changes to the following files would be overwritten by merge: README.md", preventing the merge from completing. This indicated a misunderstanding of Git's precise state and how to clear it for a clean merge.

**Ineffective Attempts and Lessons Learned:**
*   **Repeated `git restore README.md`:** This command primarily reverts *unstaged* changes. If `README.md` was in a partially resolved or staged state from previous merge attempts, `git restore` was insufficient to fully clean it to a pre-merge state.
*   **`git reset --hard README.md`:** This command is incorrect for specific file paths; `git reset --hard` operates on the entire branch. This highlighted a lack of precise knowledge of Git command nuances.
*   **Combining Commands (e.g., `git checkout ... && git add ...`):** While seemingly efficient, attempting to string commands together without fully understanding the intermediate state and potential errors led to further confusion and failed attempts. It reinforced the need for a step-by-step approach.

**The Successful Resolution Strategy:**

1.  **Ensure No Active Merge:** If a merge was attempted and failed, first abort it:
    ```bash
    git merge --abort
    ```
    *(Note: If Git reports "There is no merge to abort", you are not in a merge state, which is a good starting point.)*

2.  **Stash Problematic Local Changes:** To completely clear the working directory of the conflicting file's local modifications (staged or unstaged), use `git stash push` for that specific file. This temporarily saves your changes and cleans the working directory.
    ```bash
    git stash push README.md
    ```
    *   **Why this works:** `git stash` is robust enough to handle various states of local modifications, effectively removing them from the working directory and index, allowing Git to proceed with operations that require a clean state.

3.  **Re-attempt the Merge:** With the working directory clean, try the merge again:
    ```bash
    git merge origin/main
    ```
    *   **Expected Outcome:** A conflict might still occur if the histories truly diverge, but this time, Git will be able to manage it properly without the "local changes would be overwritten" error.

4.  **Resolve the Conflict (Explicitly Take One Side):** If a conflict still arises (as it did in our case), explicitly tell Git which version of the file to keep. Since the goal was to "overwrite" with the upstream version, we take "theirs".
    ```bash
    git checkout --theirs README.md
    ```
    *   **`--theirs` vs. `--ours`:**
        *   `--theirs`: Takes the version of the file from the branch being merged *into* the current branch (the incoming changes).
        *   `--ours`: Takes the version of the file from the current branch.

5.  **Stage the Resolved File:** After taking one side, you must stage the file to mark the conflict as resolved.
    ```bash
    git add README.md
    ```

6.  **Complete the Merge Commit:** Finally, create the merge commit. Git will often provide a default message.
    ```bash
    git commit -m "Merge branch 'main' of https://github.com/modelcontextprotocol/servers"
    ```

7.  **Reapply Stashed Changes (Optional):** If you need to reapply the changes you stashed earlier (e.g., if they were not just temporary and you want to integrate them after the merge), you can use:
    ```bash
    git stash pop
    ```
    *   **Note:** Be prepared for new conflicts if the stashed changes overlap with the merged changes.

**Key Lessons Learned (for AI and Humans):**
*   **Diagnose Git State Precisely:** Before attempting resolution, always use `git status`, `git diff`, and `git diff --staged` to understand the exact state of the repository and the conflicting files.
*   **`git stash` for Stubborn Conflicts:** When `git restore` or `git checkout HEAD` fail to clear "local changes" errors during a merge, `git stash push <file>` is a powerful tool to temporarily remove problematic modifications.
*   **Explicit Conflict Resolution:** During a merge conflict, `git checkout --theirs <file>` or `git checkout --ours <file>` are direct ways to choose one side of the conflict.
*   **Step-by-Step Execution:** Avoid stringing multiple commands together when debugging complex Git issues. Execute one command at a time and observe its output to understand the state changes.
*   **Communication is Key:** Transparently explain the Git state, the chosen strategy, and the expected outcome at each step. This builds understanding and trust.

```

#ver. 2.9.1

---
