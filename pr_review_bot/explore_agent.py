from dataclasses import dataclass


@dataclass
class PullRequestContext:
    changed_files: list[str]
    code_files_changed: list[str]
    test_files_changed: list[str]
    workflow_files_changed: list[str]
    affected_modules: list[str]
    summary: str


class ExploreSubagent:
    """
    ExploreSubagent gathers compact PR context without doing the actual review.
    """

    def explore(self, changed_files: list[str]) -> PullRequestContext:
        code_files = [
            file for file in changed_files
            if file.startswith("app/") and file.endswith(".py")
        ]

        test_files = [
            file for file in changed_files
            if file.startswith("tests/") and file.endswith(".py")
        ]

        workflow_files = [
            file for file in changed_files
            if file.startswith(".github/workflows/")
        ]

        affected_modules = self._detect_affected_modules(changed_files)

        summary = self._build_summary(
            code_files=code_files,
            test_files=test_files,
            workflow_files=workflow_files,
            affected_modules=affected_modules,
        )

        return PullRequestContext(
            changed_files=changed_files,
            code_files_changed=code_files,
            test_files_changed=test_files,
            workflow_files_changed=workflow_files,
            affected_modules=affected_modules,
            summary=summary,
        )

    def _detect_affected_modules(self, changed_files: list[str]) -> list[str]:
        modules = []
        file_text = " ".join(changed_files).lower()

        if "client" in file_text:
            modules.append("clients")

        if "invoice" in file_text:
            modules.append("invoice_records")

        if "exception" in file_text:
            modules.append("exceptions")

        if "verification" in file_text:
            modules.append("verification_checks")

        if "monthly" in file_text or "statement" in file_text:
            modules.append("monthly_statements")

        if ".github/workflows" in file_text:
            modules.append("ci_workflows")

        return modules

    def _build_summary(
        self,
        code_files: list[str],
        test_files: list[str],
        workflow_files: list[str],
        affected_modules: list[str],
    ) -> str:
        parts = []

        if code_files:
            parts.append(f"Code files changed: {', '.join(code_files)}.")

        if test_files:
            parts.append(f"Test files changed: {', '.join(test_files)}.")

        if workflow_files:
            parts.append(f"Workflow files changed: {', '.join(workflow_files)}.")

        if affected_modules:
            parts.append(f"Affected modules: {', '.join(affected_modules)}.")

        if not parts:
            return "No relevant backend, test, or workflow files changed."

        return " ".join(parts)
