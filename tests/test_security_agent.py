from pr_review_bot.explore_agent import ExploreSubagent
from pr_review_bot.review_agents.security_agent import SecurityReviewAgent


def test_security_agent_flags_hardcoded_secret_pattern():
    explorer = ExploreSubagent()
    context = explorer.explore([
        "app/main.py",
    ])

    file_contents = {
        "app/main.py": 'api_key = "fake-secret-value"'
    }

    agent = SecurityReviewAgent()
    findings = agent.review(context, file_contents)

    assert len(findings) == 1
    assert findings[0].severity == "high"
    assert findings[0].title == "Potential security risk"


def test_security_agent_flags_eval_usage():
    explorer = ExploreSubagent()
    context = explorer.explore([
        "app/main.py",
    ])

    file_contents = {
        "app/main.py": "result = eval(user_input)"
    }

    agent = SecurityReviewAgent()
    findings = agent.review(context, file_contents)

    assert len(findings) == 1
    assert findings[0].file == "app/main.py"


def test_security_agent_returns_no_findings_for_safe_content():
    explorer = ExploreSubagent()
    context = explorer.explore([
        "app/main.py",
    ])

    file_contents = {
        "app/main.py": "def root():\n    return {'status': 'running'}"
    }

    agent = SecurityReviewAgent()
    findings = agent.review(context, file_contents)

    assert findings == []
