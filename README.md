# Weekly Invoicing Workflow System

A backend-first workflow system for service businesses to track weekly invoicing, client records, exceptions, verification checks, and monthly client statements.

## Business Problem

Service businesses often manage invoicing from multiple sources such as calendars, sales records, accounting tools, and client communications. Without a structured workflow, invoices can be delayed, missing information can go unnoticed, and monthly client statements can become difficult to manage.

This project provides a simple API foundation for managing a weekly invoicing workflow.

## Phase 1 Features

- Client database
- Weekly invoice records
- Exception report tracking
- Two-level verification checklist
- Monthly statement tracker

## API Modules

### Clients

Create and list clients.

Endpoints:

- `POST /clients`
- `GET /clients`
- `GET /clients/{client_id}`

### Weekly Invoice Records

Track weekly invoice records for each client.

Endpoints:

- `POST /invoice-records`
- `GET /invoice-records`

### Exception Reports

Track missing data, pricing mismatches, calendar issues, or records needing review.

Endpoints:

- `POST /exceptions`
- `GET /exceptions`

### Verification Checks

Track two-level invoice verification:

1. Completeness check
2. Accuracy check

Endpoints:

- `POST /verification-checks`
- `GET /verification-checks`

### Monthly Statements

Track monthly statement preparation and status for group clients.

Endpoints:

- `POST /monthly-statements`
- `GET /monthly-statements`

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pytest
- HTTPX

## Current Scope

This is a Phase 1 backend prototype. It currently uses in-memory storage to prove API behavior and workflow design.

## Future Improvements

- Add persistent database storage
- Add CSV export
- Add authentication
- Add dashboard UI
- Add calendar/accounting import workflow
- Add deployment
- Prepare for future CRM migration

## Positioning

This project demonstrates backend API design for operations-heavy service businesses, focusing on invoicing workflow control, exception tracking, and process verification.

## PR Review Bot

The repository includes a rule-based PR review bot that reads actual pull-request patches, routes compact context through Explore and Plan subagents, runs focused checks in parallel, and posts one advisory PR comment.

A separate safe-auto-fix job is available only after a maintainer adds the `safe-autofix` label. It is limited to same-repository pull requests, mechanical Ruff fixes, and changes that still pass the full pytest suite.

Documentation:

- [Review Logic](docs/review-logic.md)
- [Subagent Architecture](docs/subagent-architecture.md)
- [Context Management Strategy](docs/context-management.md)
- [Parallel Execution](docs/parallel-execution.md)
- [Live PR Bot and Safe Auto-Fix](docs/live-pr-bot.md)
- [Guardrails](docs/guardrails.md)
- [Evaluation](docs/evaluation.md)
