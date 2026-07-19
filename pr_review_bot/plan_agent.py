from dataclasses import dataclass

from pr_review_bot.explore_agent import PullRequestContext


@dataclass(frozen=True)
class ReviewPlan:
    run_test_coverage: bool
    run_security: bool
    reasons: tuple[str, ...]


class PlanSubagent:
    """Selects only the review agents relevant to the explored PR context."""

    def plan(self, context: PullRequestContext) -> ReviewPlan:
        run_test_coverage = bool(context.code_files_changed)
        reviewable_files = [
            path
            for path in context.changed_files
            if path.endswith((".py", ".yml", ".yaml", ".json", ".toml", ".sh"))
        ]
        run_security = bool(reviewable_files)

        reasons: list[str] = []
        if run_test_coverage:
            reasons.append("Backend code changed, so test coverage should be reviewed.")
        if run_security:
            reasons.append(
                "Reviewable code or configuration changed, so security patterns should be scanned."
            )
        if not reasons:
            reasons.append(
                "Only non-reviewable files changed; focused code checks can be skipped."
            )

        return ReviewPlan(
            run_test_coverage=run_test_coverage,
            run_security=run_security,
            reasons=tuple(reasons),
        )
