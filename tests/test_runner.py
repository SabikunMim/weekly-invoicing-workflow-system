from pr_review_bot.runner import PRReviewRunner, format_findings


def test_runner_combines_test_coverage_and_security_findings():
    runner = PRReviewRunner()

    findings = runner.review(
        changed_files=["app/main.py"],
        file_contents={
            "app/main.py": 'api_key = "fake-secret-value"',
        },
    )

    titles = [finding.title for finding in findings]

    assert "Missing test coverage" in titles
    assert "Potential security risk" in titles


def test_runner_returns_no_findings_for_safe_docs_change():
    runner = PRReviewRunner()

    findings = runner.review(
        changed_files=["docs/review-logic.md"],
        file_contents={
            "docs/review-logic.md": "Updated documentation only.",
        },
    )

    assert findings == []


def test_format_findings_returns_markdown_success_message_when_no_findings():
    output = format_findings([])

    assert "<!-- pr-review-bot -->" in output
    assert "No focused review findings were detected" in output


def test_format_findings_includes_finding_details():
    runner = PRReviewRunner()

    findings = runner.review(
        changed_files=["app/main.py"],
        file_contents={
            "app/main.py": "def root():\n    return {'status': 'running'}",
        },
    )

    output = format_findings(findings)

    assert "## PR Review Bot" in output
    assert "Missing test coverage" in output
