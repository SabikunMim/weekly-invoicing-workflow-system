# Background and Parallel Review Execution

## Implementation

After ExploreSubagent builds compact context and PlanSubagent selects relevant checks, PRReviewRunner submits independent review agents to a ThreadPoolExecutor.

The test-coverage and security checks do not depend on each other, so they run concurrently. Results are collected in a deterministic order to keep tests and PR comments stable.

## Workflow impact

The current rule-based checks are intentionally small, so their absolute runtime is short. Parallel execution prevents their durations from being added together and provides a bounded structure for longer file-level checks later. The main coordination path waits only when it needs the combined findings.

GitHub Actions also separates ordinary review from the optional safe-auto-fix job. The auto-fix job is skipped unless a human applies the `safe-autofix` label, so normal pull requests do not pay the setup cost of installing Ruff.

## Context and safety boundaries

- Maximum review worker count: 2
- Only agents selected by PlanSubagent are submitted
- Only changed paths and added patch lines are reviewed
- Findings are combined after both selected agents complete
- The auto-fix job has separate permissions and cannot run for forked pull requests
