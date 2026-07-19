import re

from pr_review_bot.explore_agent import PullRequestContext
from pr_review_bot.findings import ReviewFinding


class SecurityReviewAgent:
    """Checks added production/configuration lines for obvious security risks."""

    sensitive_assignment = re.compile(
        r"\b(password|api_key|secret|token)\s*=\s*(.+)",
        re.IGNORECASE,
    )
    unsafe_patterns = ("eval(", "exec(", "shell=true")
    safe_secret_sources = (
        "os.environ",
        "os.getenv",
        "getenv(",
        "secrets.",
        "${{ secrets.",
    )

    def review(
        self,
        context: PullRequestContext,
        file_contents: dict[str, str],
    ) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []

        for file_path in context.changed_files:
            if file_path.startswith("tests/"):
                continue

            content = file_contents.get(file_path, "")
            for line_number, line in enumerate(content.splitlines(), start=1):
                lowered = line.lower()

                unsafe = next(
                    (pattern for pattern in self.unsafe_patterns if pattern in lowered),
                    None,
                )
                if unsafe:
                    findings.append(
                        self._finding(file_path, line_number, unsafe)
                    )
                    break

                assignment = self.sensitive_assignment.search(line)
                if assignment and not any(
                    source in lowered for source in self.safe_secret_sources
                ):
                    findings.append(
                        self._finding(
                            file_path,
                            line_number,
                            f"{assignment.group(1)} assignment",
                        )
                    )
                    break

        return findings

    @staticmethod
    def _finding(
        file_path: str,
        line_number: int,
        pattern: str,
    ) -> ReviewFinding:
        return ReviewFinding(
            severity="high",
            file=file_path,
            line=line_number,
            title="Potential security risk",
            message=f"The added lines contain a risky pattern: {pattern}",
            recommendation=(
                "Review this carefully and move secrets to environment variables "
                "or remove unsafe code."
            ),
        )
