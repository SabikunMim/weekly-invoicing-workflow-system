import json

import pytest

from pr_review_bot.github_pr import added_patch_lines, pull_request_number


def test_pull_request_number_reads_event_payload():
    assert pull_request_number({"pull_request": {"number": 42}}) == 42


def test_pull_request_number_rejects_non_pr_event():
    with pytest.raises(ValueError):
        pull_request_number({"issue": {"number": 42}})


def test_added_patch_lines_excludes_removed_and_header_lines():
    patch = """--- a/app/main.py
+++ b/app/main.py
@@ -1,2 +1,2 @@
-old_value = 1
+api_key = "example"
 unchanged = True
"""
    assert added_patch_lines(patch) == 'api_key = "example"'


def test_added_patch_lines_handles_missing_patch():
    assert added_patch_lines(None) == ""
