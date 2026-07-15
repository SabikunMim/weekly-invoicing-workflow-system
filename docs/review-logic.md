# PR Review Bot Logic Definition

## Purpose

The PR review bot is designed to review pull requests opened against the Weekly Invoicing Workflow System repository.

The bot provides structured, advisory feedback to help catch common issues before code is merged. It does not replace human review.

## Target Repository

Repository: `weekly-invoicing-workflow-system`

This repository was chosen because it contains real FastAPI backend code, multiple business workflow modules, an existing test suite, and a GitHub Actions CI workflow.

## Good Review Definition

A good review should be:

- Specific
- Actionable
- Low-noise
- Connected to changed files
- Focused on correctness, tests, security, and maintainability

The bot should avoid vague comments and should only report findings that a developer can reasonably act on.

## Review Criteria

### 1. Logic Correctness

The bot should check whether a pull request may introduce logic errors in backend workflow behavior.

Examples:

- Changing client, invoice, exception, verification, or monthly statement logic without clear reason
- Returning the wrong in-memory collection from an endpoint
- Referencing the wrong ID field
- Forgetting to validate that a related record exists
- Returning the wrong HTTP status code
- Accidentally duplicating endpoint logic

Example finding:

```text
Severity: High
File: app/main.py
Issue: Endpoint may return the wrong data collection.
Recommendation: Confirm that GET /invoice-records returns invoice_records, not clients or another collection.
```

### 2. Test Coverage

The bot should check whether changed backend behavior has matching tests.

Examples:

- A new endpoint is added without a test file update
- A schema is changed without updating tests
- New validation logic is added without a failure-case test
- Existing endpoint behavior changes without a regression test

Example finding:

```text
Severity: Medium
File: app/main.py
Issue: Backend endpoint changed but no related test file was updated.
Recommendation: Add or update tests under the tests/ folder.
```

### 3. Security and Safety

The bot should check for obvious security or safety issues.

Examples:

- Hardcoded secrets, API keys, or passwords
- Use of eval or exec
- Unsafe shell execution
- Overly broad GitHub Actions permissions
- Logging sensitive client or financial data
- Accidentally exposing private business information in test data or documentation

Example finding:

```text
Severity: High
File: app/main.py
Issue: Possible hardcoded secret detected.
Recommendation: Move secrets into environment variables or GitHub Actions secrets.
```

### 4. Maintainability and Style

The bot should check for maintainability issues that make the system harder to extend.

Examples:

- Duplicated endpoint logic
- Very large functions
- Inconsistent naming between schemas, endpoints, and tests
- Unclear status values
- Repeated validation patterns that should later be refactored
- Inconsistent error messages

Example finding:

```text
Severity: Low
File: app/main.py
Issue: Similar record-existence validation is repeated across multiple endpoints.
Recommendation: Consider refactoring into a helper function in a later cleanup step.
```

### 5. CI and Workflow Safety

The bot should check changes to GitHub Actions workflow files.

Examples:

- Removing pytest from CI
- Removing PYTHONPATH configuration
- Using unnecessary write permissions
- Adding unsafe secrets exposure
- Running untrusted code with broad permissions

Example finding:

```text
Severity: Medium
File: .github/workflows/test.yml
Issue: Test workflow changed in a way that may prevent tests from running.
Recommendation: Confirm that pytest still runs on push and pull_request.
```

## Severity Levels

### High

Issues likely to break functionality, expose sensitive data, or cause incorrect business workflow behavior.

### Medium

Issues that may reduce reliability, test coverage, or workflow safety.

### Low

Maintainability or style issues that are worth improving but do not immediately break behavior.

## Bot Output Format

Each review finding should use this structure:

```json
{
  "severity": "medium",
  "file": "app/main.py",
  "line": 42,
  "title": "Missing test coverage",
  "message": "This PR changes backend endpoint behavior without updating tests.",
  "recommendation": "Add or update a pytest test under the tests/ folder."
}
```

## What the Bot Should Not Do

The bot should not:

- Replace human review
- Make unsupported claims
- Comment on unchanged code unless it is directly related to the PR
- Produce vague feedback
- Auto-merge code
- Automatically change business logic without human approval
- Block a PR unless a clear high-severity issue is detected

## Current Scope

The first version of the PR review bot will be rule-based and deterministic.

It will inspect changed files, file names, and diff content to identify common issues. LLM-based review can be added later, but the first version should be simple, testable, and reliable.
