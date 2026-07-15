from pr_review_bot.explore_agent import ExploreSubagent
from pr_review_bot.review_agents.test_coverage_agent import TestCoverageReviewAgent


def test_test_coverage_agent_flags_code_change_without_tests():
    explorer = ExploreSubagent()
    context = explorer.explore([
        "app/main.py",
    ])

    agent = TestCoverageReviewAgent()
    findings = agent.review(context)

    assert len(findings) == 1
    assert findings[0].severity == "medium"
    assert findings[0].title == "Missing test coverage"


def test_test_coverage_agent_does_not_flag_when_tests_changed():
    explorer = ExploreSubagent()
    context = explorer.explore([
        "app/main.py",
        "tests/test_clients.py",
    ])

    agent = TestCoverageReviewAgent()
    findings = agent.review(context)

    assert findings == []


def test_test_coverage_agent_does_not_flag_docs_only_change():
    explorer = ExploreSubagent()
    context = explorer.explore([
        "docs/review-logic.md",
    ])

    agent = TestCoverageReviewAgent()
    findings = agent.review(context)

    assert findings == []
