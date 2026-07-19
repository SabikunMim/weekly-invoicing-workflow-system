# Live PR Review and Safe Auto-Fix

## Pull request review

The PR Review Bot workflow runs for opened, synchronized, reopened, and labeled pull requests.

The workflow:

1. Checks out the pull request branch.
2. Runs the repository test suite.
3. Reads the pull request's real changed-file list and paginated patches through the GitHub API.
4. Keeps only added patch lines for content-based checks.
5. Runs ExploreSubagent, PlanSubagent, and the selected review agents.
6. Posts one advisory Markdown comment to the pull request.
7. Updates the existing bot comment on later commits instead of creating duplicates.

The ordinary review job has `contents: read` and `pull-requests: write`. It cannot push code.

## Human-approved safe auto-fix

Automatic code changes are disabled by default. A maintainer must add the `safe-autofix` label before the separate auto-fix job can run.

The job is additionally restricted to pull requests whose head branch belongs to this repository. Fork pull requests cannot use its write token.

For eligible changed Python files, the job:

1. Runs Ruff's supported fixes and formatter.
2. Runs the complete pytest suite.
3. Stops without committing if tests fail.
4. Stops without committing if Ruff made no changes.
5. Commits and pushes only the changed eligible Python files when tests pass.

This path is appropriate for mechanical formatting and lint fixes. It does not rewrite business logic, change authentication, alter billing or invoicing behavior, merge the pull request, or approve it.

## Human responsibility

A maintainer still controls the label, reviews any resulting commit, approves the pull request, and decides whether to merge.
