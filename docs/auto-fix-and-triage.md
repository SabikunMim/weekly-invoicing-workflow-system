# Auto-Fix and Issue Triage

## Purpose

This document explains how the PR review bot handles auto-fix behavior and issue triage.

The goal is to add useful automation while keeping code changes safe and human-reviewed.

## Issue Triage

The repository includes an issue triage workflow:

.github/workflows/issue-triage.yml

This workflow runs when an issue is opened or edited.

It labels issues based on simple keywords in the issue title and body.

## Automatic Issue Labels

The triage bot can apply these labels:

- bug
- enhancement
- security
- documentation
- needs-review

## Issue Triage Rules

The workflow uses conservative keyword matching.

Examples:

- "bug", "error", "fail", "broken", "exception" -> bug
- "feature", "enhancement", "request", "improve" -> enhancement
- "security", "secret", "token", "password", "api key" -> security
- "documentation", "docs", "readme" -> documentation

If no clear category is found, the bot applies:

- needs-review

## Human Review Requirement

Issue labels are automatic suggestions.

A human maintainer should still confirm:

- issue priority
- whether the label is correct
- whether the issue should be assigned
- whether the issue should be closed, deferred, or worked on

## Auto-Fix Policy

The bot does not automatically modify production code without human approval.

This is intentional.

Auto-fixing code can be risky because an automated change might:

- break existing behavior
- hide a deeper bug
- introduce a security issue
- change business logic incorrectly
- pass tests while still being wrong

## What the Bot May Do Automatically

The bot may automatically:

- identify missing test coverage
- identify simple security risk patterns
- produce structured review findings
- run checks in GitHub Actions
- label issues based on keywords
- suggest possible safe next actions

## What Requires Human Approval

The bot must not automatically apply these changes without human approval:

- production code changes
- security-related changes
- authentication or permission changes
- database or data model changes
- billing, invoicing, or financial logic changes
- dependency upgrades
- deletion of files
- generated patches that affect business behavior

## Safe Auto-Fix Scope

For the current version, auto-fix is limited to advisory output.

The bot can suggest fixes such as:

- add tests for changed backend behavior
- move hardcoded secrets to environment variables
- avoid eval or exec
- review shell=True usage
- add documentation for workflow changes

The bot does not push commits automatically.

## Future Safe Auto-Fix Design

A future version could implement safe auto-fix through a human-approved workflow.

Possible flow:

1. Bot detects a fixable issue
2. Bot creates a suggested patch
3. Bot opens a separate branch
4. Bot opens a pull request
5. GitHub Actions runs tests
6. Human reviewer approves or rejects the fix PR
7. The fix is merged only after review

## Guardrails

The bot should follow these guardrails:

- never commit directly to main
- never auto-merge changes
- never edit secrets
- never change billing or financial logic without review
- never claim a fix is guaranteed correct
- always run tests after generated changes
- always require human approval for code modifications

## Current Status

Implemented:

- automatic issue triage workflow
- keyword-based issue labeling
- automated issue comment
- safe auto-fix policy
- human approval rules

Not implemented yet:

- automatic code modification
- automatic pull request creation for fixes
- automatic test repair
- automatic merge

## Conclusion

Step 11 is implemented as a safe automation prototype.

Issue triage is automatic. Auto-fix behavior is intentionally limited to suggestions and documentation because code changes should require human approval.
