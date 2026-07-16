from concurrent.futures import ThreadPoolExecutor

from pr_review_bot.explore_agent import ExploreSubagent
from pr_review_bot.findings import ReviewFinding
from pr_review_bot.review_agents.security_agent import SecurityReviewAgent
from pr_review_bot.review_agents.test_coverage_agent import TestCoverageReviewAgent


class PRReviewRunner:
    """
    Coordinates the PR review process.

    Flow:
    changed files + file contents
    -> ExploreSubagent
    -> review agents
    -> combined findings
    """

    def __init__(self):
        self.explorer = ExploreSubagent()
        self.test_coverage_agent = TestCoverageReviewAgent()
        self.security_agent = SecurityReviewAgent()

    def review(
        self,
        changed_files: list[str],
        file_contents: dict[str, str] | None = None,
    ) -> list[ReviewFinding]:
                if file_contents is None:
            file_contents = {}

        context = self.explorer.explore(changed_files)

        with ThreadPoolExecutor(max_workers=2) as executor:
            test_coverage_future = executor.submit(
                self.test_coverage_agent.review,
                context,
            )

            security_future = executor.submit(
                self.security_agent.review,
                context,
                file_contents,
            )

            findings: list[ReviewFinding] = []
            findings.extend(test_coverage_future.result())
            findings.extend(security_future.result())

        return findings


def format_findings(findings: list[ReviewFinding]) -> str:
    if not findings:
        return "PR Review Bot completed. No issues found."

    lines = ["PR Review Bot Findings", ""]

    for index, finding in enumerate(findings, start=1):
        lines.append(f"{index}. [{finding.severity.upper()}] {finding.title}")
        lines.append(f"File: {finding.file}")

        if finding.line is not None:
            lines.append(f"Line: {finding.line}")

        lines.append(f"Message: {finding.message}")
        lines.append(f"Recommendation: {finding.recommendation}")
        lines.append("")

    return "\n".join(lines)


def main():
    changed_files = [
        "app/main.py",
    ]

    file_contents = {
        "app/main.py": "api_key = 'fake-secret-value'",
    }

    runner = PRReviewRunner()
    findings = runner.review(changed_files, file_contents)

    print(format_findings(findings))


if __name__ == "__main__":
    main()
