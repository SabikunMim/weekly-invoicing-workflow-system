# Guardrails

## Purpose

This document defines the guardrails for the PR review bot.

The bot is designed to provide structured review feedback on pull requests. It supports human reviewers by flagging common issues, but it does not replace human judgment.

## What the Bot Is Allowed to Do

The bot is allowed to:

- Identify changed files in a pull request
- Summarize pull request context
- Flag backend code changes that do not include related test changes
- Flag obvious risky security patterns in changed file content
- Produce structured review findings
- Recommend that a human reviewer checks a risky change
- Explain why a finding was created
- Keep feedback limited to the pull request changes

## What the Bot Is Not Allowed to Do

The bot must not:

- Auto-merge pull requests
- Approve pull requests automatically
- Reject pull requests automatically
- Change business logic without human approval
- Modify production code on its own
- Claim that a pull request is fully secure
- Claim that a pull request is bug-free
- Expose secrets in review output
- Replace human code review
- Make broad claims about unrelated files
- Comment on files that were not part of the pull request context

## Security Guardrails

The SecurityReviewAgent only detects simple risky patterns.

Examples include:

- password =
- api_key =
- secret =
- token =
- eval(
- exec(
- shell=True

The bot should describe these as potential risks, not confirmed vulnerabilities.

Correct wording:

- Potential security risk
- Review this carefully
- Move secrets to environment variables

Incorrect wording:

- This code is definitely insecure
- This PR is unsafe
- This PR is secure after this finding is fixed

## Test Coverage Guardrails

The TestCoverageReviewAgent can flag backend code changes that do not include test changes.

The bot should not assume that every code change requires a new test. It should only flag this as a review concern.

Correct wording:

- Backend code changed without related test changes
- Consider adding or updating tests
- Human reviewer should confirm whether tests are needed

Incorrect wording:

- This PR must be rejected
- This code is broken
- This PR has no valid test coverage

## Context Guardrails

The bot should only use relevant pull request context.

It should avoid:

- Loading the entire repository unnecessarily
- Reviewing unrelated files
- Making claims about unchanged code
- Passing all file contents to every review agent
- Producing long unfocused feedback

The bot should prefer:

- Changed file paths
- Compact summaries
- Relevant file contents only
- Structured findings

## Human Review Requirement

The bot is advisory.

A human reviewer is still responsible for:

- Final approval
- Business logic decisions
- Security judgment
- Production readiness
- Merge decisions

The bot can support those decisions, but it cannot make them independently.

## Safe Output Format

Each finding should include:

- severity
- file
- line, if known
- title
- message
- recommendation

The bot should avoid emotional, accusatory, or absolute language.

Good example:

Potential security risk found in app/main.py. The changed file contains a risky pattern: api_key=. Review this carefully and move secrets to environment variables.

Bad example:

This PR leaks secrets and should never be merged.

## Current Guardrails in Implementation

The current implementation follows these guardrails by:

- Using ExploreSubagent to limit context
- Using ReviewFinding for structured output
- Keeping review agents narrow and testable
- Returning findings instead of changing code
- Running tests in GitHub Actions before accepting changes

## Future Guardrails

Future versions should add:

- Maximum file size limits
- Ignoring generated files
- Redacting detected secret values
- Pull request permission restrictions
- Human approval before posting or acting on findings
- Clear labels for advisory feedback

## Conclusion

The PR review bot is a focused assistant for pull request review.

It should flag risks, summarize issues, and recommend human review. It should not approve, reject, merge, rewrite business logic, or claim complete security.
