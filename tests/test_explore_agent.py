from pr_review_bot.explore_agent import ExploreSubagent


def test_explore_agent_identifies_code_and_test_files():
    explorer = ExploreSubagent()

    context = explorer.explore([
        "app/main.py",
        "tests/test_invoice_records.py",
    ])

    assert "app/main.py" in context.code_files_changed
    assert "tests/test_invoice_records.py" in context.test_files_changed
    assert "invoice_records" in context.affected_modules


def test_explore_agent_identifies_workflow_files():
    explorer = ExploreSubagent()

    context = explorer.explore([
        ".github/workflows/test.yml",
    ])

    assert ".github/workflows/test.yml" in context.workflow_files_changed
    assert "ci_workflows" in context.affected_modules


def test_explore_agent_returns_summary():
    explorer = ExploreSubagent()

    context = explorer.explore([
        "app/main.py",
        "tests/test_clients.py",
    ])

    assert "Code files changed" in context.summary
    assert "Test files changed" in context.summary
