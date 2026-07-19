from pr_review_bot.explore_agent import ExploreSubagent
from pr_review_bot.plan_agent import PlanSubagent


def test_plan_selects_code_checks_for_backend_change():
    context = ExploreSubagent().explore(["app/main.py"])
    plan = PlanSubagent().plan(context)

    assert plan.run_test_coverage is True
    assert plan.run_security is True


def test_plan_skips_code_checks_for_docs_only_change():
    context = ExploreSubagent().explore(["docs/review-logic.md"])
    plan = PlanSubagent().plan(context)

    assert plan.run_test_coverage is False
    assert plan.run_security is False
