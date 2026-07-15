# PR Review Bot Subagent Architecture

## Purpose

This document explains how the PR review bot splits review work across focused subagents.

The goal is to keep the bot useful, testable, and low-noise. Each subagent has a narrow responsibility so the final review is easier to verify.

## Architecture Overview

The PR review bot uses this flow:

Pull Request  
→ Main Runner  
→ Explore Subagent  
→ Plan Subagent  
→ Focused Review Subagents  
→ Final Review Comment

## Main Runner

The Main Runner controls the full review process.

Responsibilities:

- Read pull request metadata
- Load changed files and diffs
- Call the Explore Subagent
- Call the Plan Subagent
- Run selected review subagents
- Combine findings into one structured review report
- Post the final result to the pull request

The Main Runner should not perform detailed review logic itself. Its job is coordination.

## Explore Subagent

The Explore Subagent gathers context from the pull request.

Responsibilities:

- Identify changed files
- Separate code files from test files
- Detect changed GitHub Actions workflow files
- Summarize the diff
- Identify which business modules are affected
- Return a compact review context

Example output:

Changed files:
- app/main.py
- tests/test_invoice_records.py

Code files changed:
- app/main.py

Test files changed:
- tests/test_invoice_records.py

Summary:
This pull request changes invoice record endpoint behavior and updates related tests.

The Explore Subagent exists because the main review process should not load unnecessary repository context. It reduces the pull request into a focused summary.

## Plan Subagent

The Plan Subagent decides which review agents should run.

Responsibilities:

- Read the Explore Subagent summary
- Decide which review areas are relevant
- Avoid running unnecessary checks
- Create a review plan

Example plan:

- Run Logic Review Agent because app/main.py changed
- Run Test Coverage Agent because backend code changed
- Run Security Review Agent because all code changes should be scanned for basic risks
- Skip Workflow Safety Agent because no GitHub Actions files changed

The Plan Subagent exists to keep the review efficient and avoid noisy output.

## Logic Review Agent

The Logic Review Agent checks for possible backend behavior problems.

Focus areas:

- Wrong collection returned from an endpoint
- Missing related-record validation
- Wrong HTTP status code
- Incorrect ID usage
- Duplicated or misplaced endpoint logic
- Business workflow behavior changes

Example finding:

Severity: High  
File: app/main.py  
Title: Possible wrong return value  
Message: This endpoint may return the wrong in-memory collection.  
Recommendation: Confirm the endpoint returns the correct resource list.

## Test Coverage Agent

The Test Coverage Agent checks whether backend behavior changes include matching tests.

Focus areas:

- New endpoint without a test
- Schema change without a test
- New validation logic without a failure-case test
- Modified behavior without regression coverage

Example finding:

Severity: Medium  
File: app/main.py  
Title: Missing test coverage  
Message: Backend behavior changed, but no related test file was updated.  
Recommendation: Add or update pytest coverage in the tests folder.

## Security Review Agent

The Security Review Agent checks for obvious safety issues.

Focus areas:

- Hardcoded secrets
- API keys or passwords in code
- Use of eval or exec
- Unsafe shell execution
- Sensitive business or financial data in logs
- Unsafe GitHub Actions permissions

Example finding:

Severity: High  
File: app/main.py  
Title: Possible hardcoded secret  
Message: The change appears to include sensitive data in source code.  
Recommendation: Move secrets to environment variables or GitHub Actions secrets.

## Maintainability Review Agent

The Maintainability Review Agent checks whether the code is becoming harder to extend.

Focus areas:

- Duplicated endpoint logic
- Long functions
- Inconsistent naming
- Inconsistent error messages
- Repeated validation patterns
- Unclear status values

Example finding:

Severity: Low  
File: app/main.py  
Title: Repeated validation logic  
Message: Similar record-existence checks appear in multiple endpoints.  
Recommendation: Consider extracting a helper function during a later refactor.

## Workflow Safety Agent

The Workflow Safety Agent checks changes to CI/CD configuration.

Focus areas:

- Removing pytest from GitHub Actions
- Removing PYTHONPATH configuration
- Adding unnecessary write permissions
- Exposing secrets in workflow logs
- Running risky scripts in CI

Example finding:

Severity: Medium  
File: .github/workflows/test.yml  
Title: Test workflow may not run correctly  
Message: The workflow configuration changed in a way that may prevent tests from running.  
Recommendation: Confirm that pytest still runs on push and pull_request.

## Output Format

Each review agent returns findings using the same structure:

severity: high, medium, or low  
file: path to affected file  
line: optional line number  
title: short issue title  
message: explanation of the issue  
recommendation: suggested fix or next action

## Why This Architecture Works

This architecture keeps the bot focused and maintainable.

The Explore Subagent reduces context.  
The Plan Subagent decides what matters.  
The review agents perform narrow checks.  
The Main Runner combines the results.

This prevents one large review process from becoming noisy, hard to test, or difficult to debug.

## Current Scope

The first version will be rule-based.

It will use file names, changed file lists, and diff patterns to produce structured findings. More advanced AI-based reasoning can be added later after the rule-based version is working and tested.
