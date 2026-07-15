from pr_review_bot.explore_agent import PullRequestContext
from pr_review_bot.review_agents.test_coverage_agent import ReviewFinding


class SecurityReviewAgent:
    """
    Checks changed file content for obvious security risks.
    """

    risky_patterns = [
        "password =",
        "password=",
        "api_key =",
        "api_key=",
        "secret =",
        "secret=",
        "token =",
        "token=",
        "eval(",
        "exec(",
        "shell=True",
    ]

    def review(self, context: PullRequestContext, file_contents: dict[str, str]) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []

        for file_path in context.changed_files:
            content = file_contents.get(file_path, "")
            lowered_content = content.lower()

            for pattern in self.risky_patterns:
                if pattern.lower() in lowered_content:
                    findings.append(
                        ReviewFinding(
                            severity="high",
                            file=file_path,
                            line=None,
                            title="Potential security risk",
                            message=f"The changed file contains a risky pattern: {pattern}",
                            recommendation="Review this carefully and move secrets to environment variables or remove unsafe code.",
                        )
                    )
                    break

        return findings
