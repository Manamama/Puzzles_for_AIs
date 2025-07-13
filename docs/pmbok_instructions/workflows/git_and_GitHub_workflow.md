

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

To ensure smooth Git operations and avoid common issues like divergent branches, adhere to the following workflow for any branch (e.g., `main` or feature branches):

1. **Check Status**: Always start with `git status` to understand the current state of the repository.
2. **Stage Changes**: Use `git add <file>` or `git add .` to stage changes for commit.
3. **Commit Changes**: Create meaningful commits with `git commit -m "Your descriptive commit message"`.
4. **Pull Before Push (Crucial)**: Before pushing, always pull the latest changes from the remote to avoid conflicts and ensure your local branch is up-to-date.
   * `git pull origin <branch>` (replace `<branch>` with your current branch, e.g., `main`).
   * If a "divergent branches" error occurs, use `git pull --rebase origin <branch>` to rebase your local commits on top of the remote’s history. This keeps the commit history clean.
   * If conflicts arise during rebase, resolve them manually, then run `git rebase --continue` or `git rebase --abort` to cancel.
5. **Push Changes**: After successfully pulling and resolving any conflicts, push your changes: `git push origin <branch>`.

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

### 3. Other Common `gh` Commands

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

#ver. 2.8.0

---
