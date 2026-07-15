from dataclasses import dataclass

from pr_review_bot.explore_agent import PullRequestContext


@dataclass
class ReviewFinding:
    severity: str
    file: str
    line: int | None
    title: str
    message: str
    recommendation: str


class TestCoverageReviewAgent:
    """
    Checks whether backend code changes include related test changes.
    """

    def review(self, context: PullRequestContext) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []

        if context.code_files_changed and not context.test_files_changed:
            findings.append(
                ReviewFinding(
                    severity="medium",
                    file=", ".join(context.code_files_changed),
                    line=None,
                    title="Missing test coverage",
                    message="Backend code changed, but no related test files were changed.",
                    recommendation="Add or update pytest coverage under the tests folder.",
                )
            )

        return findings
