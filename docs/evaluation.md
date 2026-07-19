# PR Review Bot Evaluation

## Implemented capabilities

The deployed rule-based bot now:

- Reads the real pull request number from the GitHub event payload.
- Retrieves every changed-file page from the GitHub API.
- Passes changed paths through ExploreSubagent.
- Uses PlanSubagent to select relevant review agents.
- Passes only added patch lines to content-based checks.
- Runs independent test-coverage and security checks in parallel.
- Posts or updates one advisory Markdown comment on the pull request.
- Avoids duplicate bot comments after synchronized commits.
- Ignores test fixtures and environment-sourced secret assignments to reduce noise.
- Supports a separate human-approved safe-auto-fix job.

## TDD coverage

Automated tests cover:

- ExploreSubagent classification and summary behavior.
- PlanSubagent selection for backend and documentation-only changes.
- Pull-request event validation and added-line extraction.
- Missing-test detection.
- Hard-coded secret and unsafe-execution detection.
- False-positive controls for test fixtures, environment variables, and the detector's own patterns.
- Parallel runner coordination and PR comment formatting.
- The assignment's known-bad-PR scenario.

## Live PR evidence

Draft pull request #3 is the live end-to-end test:

- [Live pull request #3](https://github.com/SabikunMim/weekly-invoicing-workflow-system/pull/3)
- [Bot review comment](https://github.com/SabikunMim/weekly-invoicing-workflow-system/pull/3#issuecomment-5014613776)
- [Passing backend test run](https://github.com/SabikunMim/weekly-invoicing-workflow-system/actions/runs/29675716567)
- [Passing PR Review Bot run](https://github.com/SabikunMim/weekly-invoicing-workflow-system/actions/runs/29675716554)

The first live review exposed false positives for an environment-loaded token and a test fixture. Regression tests and filtering rules were added, after which the bot updated the same PR comment and reported no focused findings.

## Safe auto-fix evidence

A maintainer applied the `safe-autofix` label to pull request #3. The isolated auto-fix job:

1. Ran Ruff only on changed Python files.
2. Ran the full pytest suite.
3. Created a commit only after tests passed.
4. Pushed the mechanical formatting changes to the PR branch.

Evidence:

- [Human-approved auto-fix commit](https://github.com/SabikunMim/weekly-invoicing-workflow-system/commit/472e6e11406892b7ba10a955a49ee086355cc3c2)
- [Successful labeled workflow run](https://github.com/SabikunMim/weekly-invoicing-workflow-system/actions/runs/29675839274)

The approval label was removed after the demonstration to prevent repeated auto-fix attempts.

## Guardrails

The ordinary review job has `contents: read` and `pull-requests: write`. The auto-fix job is separate and receives `contents: write` only when its job-level condition is satisfied.

The auto-fix job cannot run for forked pull requests. It does not approve, merge, change permissions, rewrite business logic, or bypass tests. Maintainers remain responsible for review and merge decisions.

## Remaining limitations

The bot uses deterministic rules rather than semantic code reasoning. It does not prove security, detect complex business-logic bugs, scan dependencies, or guarantee that tests are sufficient. GitHub may omit a patch for binary or very large files; those files remain in the changed-file summary but have no added-line content for the security check.

## Result

The assignment's deployed-bot path is demonstrated: actual PR changes flow through Explore, Plan, and focused review agents; results are posted on a live PR; tests run in CI; and a human-approved safe auto-fix produced a verified mechanical commit.
