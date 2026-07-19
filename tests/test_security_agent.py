from pr_review_bot.explore_agent import ExploreSubagent
from pr_review_bot.review_agents.security_agent import SecurityReviewAgent


def review(files, contents):
    context = ExploreSubagent().explore(files)
    return SecurityReviewAgent().review(context, contents)


def test_security_agent_flags_hardcoded_secret_pattern():
    findings = review(
        ["app/main.py"],
        {"app/main.py": 'api_key = "fake-secret-value"'},
    )

    assert len(findings) == 1
    assert findings[0].severity == "high"
    assert findings[0].title == "Potential security risk"


def test_security_agent_flags_eval_usage():
    findings = review(
        ["app/main.py"],
        {"app/main.py": "result = eval(user_input)"},
    )

    assert len(findings) == 1
    assert findings[0].file == "app/main.py"


def test_security_agent_returns_no_findings_for_safe_content():
    findings = review(
        ["app/main.py"],
        {"app/main.py": "def root():\n    return {'status': 'running'}"},
    )

    assert findings == []


def test_security_agent_allows_environment_sourced_token():
    findings = review(
        ["pr_review_bot/github_pr.py"],
        {"pr_review_bot/github_pr.py": 'token = os.environ["GITHUB_TOKEN"]'},
    )

    assert findings == []


def test_security_agent_ignores_test_fixtures():
    findings = review(
        ["tests/test_security_agent.py"],
        {"tests/test_security_agent.py": 'api_key = "example-fixture"'},
    )

    assert findings == []
