from pr_review_bot.runner import PRReviewRunner


def test_bot_flags_known_bad_pr_with_code_change_no_tests_and_secret():
    """
    Assignment TDD case:

    This simulates a bad pull request where backend code changes,
    no tests are updated, and a hardcoded API key is introduced.

    Correct bot behavior:
    - Flag missing test coverage
    - Flag potential security risk
    """

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
