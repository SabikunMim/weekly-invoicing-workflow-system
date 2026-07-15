# Context Management Strategy

## Purpose

This document explains how the PR review bot manages context while reviewing pull requests.

The goal is to keep the review focused, efficient, and reliable. The bot should avoid loading unnecessary repository content and should only pass relevant information to each review subagent.

## Why Context Management Matters

Pull requests can contain many changed files. If the bot tries to review the entire repository every time, the review process becomes noisy, slow, and harder to verify.

The bot treats context as a limited resource.

Instead of passing everything to every subagent, the bot uses a staged process:

1. Identify changed files.
2. Summarize the pull request.
3. Select relevant review agents.
4. Pass only the needed information to each agent.
5. Combine findings into a final report.

## Current Context Flow

The current bot uses this flow:

Pull request changed files  
→ ExploreSubagent  
→ PullRequestContext summary  
→ Review agents  
→ Structured findings  
→ Final review output

## ExploreSubagent Context Reduction

The ExploreSubagent receives a list of changed files.

It does not review the whole repository.

It creates a compact PullRequestContext containing:

- changed_files
- code_files_changed
- test_files_changed
- workflow_files_changed
- affected_modules
- summary

This keeps the rest of the bot focused on only the files related to the pull request.

## Passing Only Relevant Information

The review agents do not receive the full repository.

They receive only:

- the PullRequestContext
- selected file contents when needed

For example:

The TestCoverageReviewAgent only needs to know whether backend code files changed and whether test files changed.

The SecurityReviewAgent needs changed file paths and the content of those changed files.

This avoids unnecessary processing and keeps each agent narrow.

## File-Level Context Strategy

The bot separates files into categories:

- Backend code files: app/*.py
- Test files: tests/*.py
- Workflow files: .github/workflows/*
- Documentation files: docs/*.md and README.md

This allows the bot to decide which checks are relevant.

Examples:

- If only documentation changes, the bot should not require test updates.
- If app/main.py changes, the bot should check for test coverage.
- If .github/workflows/test.yml changes, the bot should check workflow safety.
- If changed file contents contain risky patterns, the bot should create a security finding.

## Summary-Based Review

The ExploreSubagent creates a short summary of the pull request context.

Example summary:

Code files changed: app/main.py. Test files changed: tests/test_invoice_records.py. Affected modules: invoice_records.

This summary is useful because it gives the runner and future review agents a compact view of the PR without loading unrelated files.

## Context Boundaries

The current bot intentionally avoids:

- Loading the entire repository
- Reviewing unchanged files
- Commenting on unrelated code
- Making broad architectural claims from a small diff
- Passing all file contents to every agent

This reduces noise and keeps the review tied to the pull request.

## Current Implementation

Current implementation files:

- pr_review_bot/explore_agent.py
- pr_review_bot/runner.py
- pr_review_bot/review_agents/test_coverage_agent.py
- pr_review_bot/review_agents/security_agent.py

Current tests:

- tests/test_explore_agent.py
- tests/test_runner.py
- tests/test_test_coverage_agent.py
- tests/test_security_agent.py

## How Context Is Used by Each Agent

## TestCoverageReviewAgent

Input:

- PullRequestContext

Uses:

- code_files_changed
- test_files_changed

It does not need file contents.

Output:

- A medium-severity finding if backend code changed without matching test changes.

## SecurityReviewAgent

Input:

- PullRequestContext
- file_contents dictionary for changed files

Uses:

- changed_files
- file content for changed files only

Output:

- A high-severity finding if risky patterns are found.

## Runner Context Management

The PRReviewRunner coordinates the full process.

It:

1. Sends changed_files to the ExploreSubagent.
2. Receives a compact PullRequestContext.
3. Sends the PullRequestContext to review agents.
4. Sends file contents only to agents that need file contents.
5. Combines findings into one final output.

This keeps the runner simple and avoids large, unfocused review logic.

## Future Improvements

Future versions can improve context management by:

- Reading actual git diffs instead of full file content
- Passing only changed lines to review agents
- Limiting file content size per file
- Skipping generated or vendor files
- Creating per-file summaries for large pull requests
- Running review agents in parallel
- Adding a PlanSubagent to select only relevant agents for each PR

## Conclusion

The PR review bot manages context by reducing the pull request to changed files, summaries, affected modules, and relevant file contents.

This keeps the bot focused, testable, and aligned with the assignment requirement to treat context as a limited resource.
