# Daily repository maintainer

This scheduled GitHub Actions workflow scans non-fork, non-archived repositories
owned by the account where the GitHub App is installed. Gemini may propose up to
one small code-fix pull request per repository per day. It does not merge PRs or
write to a repository's default branch. Existing pull requests must pass that
repository's own checks and be reviewed by a person.

## GitHub setup

1. Create a GitHub App under your account. Grant **Contents: Read and write**,
   **Pull requests: Read and write**, and **Metadata: Read-only** permissions.
2. Install the App on the repositories you want scanned. The workflow filters
   to repositories owned by the account that contains this bot repository.
3. In this repository's **Settings → Secrets and variables → Actions**, add:
   - `REPO_BOT_APP_ID`: the numeric GitHub App ID.
   - `REPO_BOT_APP_PRIVATE_KEY`: the private key downloaded for the App.
   - `GEMINI_API_KEY`: a Google AI API key with usage limits configured.
4. Run **Actions → Daily repository maintenance → Run workflow** once to test;
   scheduled runs start daily at 08:17 UTC.

The App private key and Gemini key must stay in GitHub Actions secrets, never in
the repository or chat. Source files from each selected repository are sent to
Gemini for analysis, so only install the App on repositories whose code you are
comfortable sending to that service. Each generated PR is a proposal: inspect its
diff and CI results before merging.

The scanner currently reads at most 40 source files and 80,000 characters per
repository, and changes only existing files in supported source-code languages.
It skips repositories with an open maintenance PR and reports `no_change` when
it cannot justify a concrete fix.