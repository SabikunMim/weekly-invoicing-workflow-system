# Background and Parallel Sessions

## Purpose

This document explains how the PR review bot uses a parallel-ready review design.

The assignment asks for background or parallel sessions to avoid blocking the main review process. In this project, the current implementation keeps review work separated into independent agents so that each check can run separately and later be executed in parallel.

## Current Approach

The bot uses separate review agents:

- ExploreSubagent
- TestCoverageReviewAgent
- SecurityReviewAgent
- PRReviewRunner

The ExploreSubagent gathers a compact pull request context first. After that, each review agent can inspect the same context independently.

This structure avoids one large review process doing everything at once.

## Why This Helps

Separating review work improves the workflow because:

- Each review agent has one responsibility
- Agents can be tested independently
- A slow review check does not need to block other checks in future versions
- More agents can be added without rewriting the whole bot
- The runner can combine results from multiple agents into one final report

## Current Implementation

The current implementation runs agents sequentially through PRReviewRunner.

This is intentional for the first working version because it keeps the code simple, predictable, and easy to test.

Current flow:

1. ExploreSubagent gathers changed-file context
2. TestCoverageReviewAgent checks test coverage risk
3. SecurityReviewAgent checks simple security risk patterns
4. PRReviewRunner combines findings

## Parallel-Ready Design

Although the current runner is sequential, the design is parallel-ready.

The review agents do not depend on each other. Each one receives the same PullRequestContext and returns a list of ReviewFinding objects.

Because of this, future versions can run the agents in parallel using:

- Python concurrent.futures
- background tasks
- separate GitHub Actions jobs
- separate worker processes

## Example Future Parallel Flow

Future runner flow:

1. ExploreSubagent creates PullRequestContext
2. TestCoverageReviewAgent runs in one background task
3. SecurityReviewAgent runs in another background task
4. Additional agents run independently
5. PRReviewRunner combines all findings

## Honest Limitation

This version does not yet run true concurrent background workers.

Instead, it uses a modular subagent structure that makes parallel execution safe and straightforward to add later.

This is a deliberate tradeoff because the current assignment version prioritizes correctness, tests, and reliable CI behavior before adding concurrency complexity.

## Conclusion

The project uses a parallel-ready subagent architecture.

The current version runs checks sequentially, but the review agents are isolated and can be moved into background or parallel execution in a future version without changing their core behavior.
