from concurrent.futures import ThreadPoolExecutor

from pr_review_bot.explore_agent import ExploreSubagent
from pr_review_bot.findings import ReviewFinding
from pr_review_bot.plan_agent import PlanSubagent
from pr_review_bot.review_agents.security_agent import SecurityReviewAgent
from pr_review_bot.review_agents.test_coverage_agent import TestCoverageReviewAgent


class PRReviewRunner:
    """Coordinates Explore -> Plan -> focused parallel review agents."""

    def __init__(self):
        self.explorer = ExploreSubagent()
        self.planner = PlanSubagent()
        self.test_coverage_agent = TestCoverageReviewAgent()
        self.security_agent = SecurityReviewAgent()

    def review(
        self,
        changed_files: list[str],
        file_contents: dict[str, str] | None = None,
    ) -> list[ReviewFinding]:
        file_contents = file_contents or {}
        context = self.explorer.explore(changed_files)
        plan = self.planner.plan(context)

        jobs = {}
        with ThreadPoolExecutor(max_workers=2) as executor:
            if plan.run_test_coverage:
                jobs["test_coverage"] = executor.submit(
                    self.test_coverage_agent.review,
                    context,
                )
            if plan.run_security:
                jobs["security"] = executor.submit(
                    self.security_agent.review,
                    context,
                    file_contents,
                )

            findings: list[ReviewFinding] = []
            for job_name in ("test_coverage", "security"):
                if job_name in jobs:
                    findings.extend(jobs[job_name].result())

        return findings


def format_findings(findings: list[ReviewFinding]) -> str:
    lines = [
        "<!-- pr-review-bot -->",
        "## PR Review Bot",
        "",
        "_Automated advisory review. Human review is still required._",
        "",
    ]

    if not findings:
        lines.append("No focused review findings were detected in the changed lines.")
        return "\n".join(lines)

    lines.append("### Findings")
    lines.append("")
    for index, finding in enumerate(findings, start=1):
        lines.append(f"{index}. **[{finding.severity.upper()}] {finding.title}**")
        lines.append(f"   - File: `{finding.file}`")
        if finding.line is not None:
            lines.append(f"   - Line: {finding.line}")
        lines.append(f"   - {finding.message}")
        lines.append(f"   - Recommendation: {finding.recommendation}")

    return "\n".join(lines)
