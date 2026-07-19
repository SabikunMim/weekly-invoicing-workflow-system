import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from pr_review_bot.runner import PRReviewRunner, format_findings


def github_api_json(url: str, token: str) -> object:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "weekly-invoicing-pr-review-bot",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed ({error.code}): {detail}") from error


def pull_request_number(event: dict) -> int:
    try:
        return int(event["pull_request"]["number"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("The event payload does not contain a pull request number.") from error


def added_patch_lines(patch: str | None) -> str:
    if not patch:
        return ""
    return "\n".join(
        line[1:]
        for line in patch.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def fetch_changed_files(repository: str, number: int, token: str) -> list[dict]:
    results: list[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{repository}/pulls/{number}/files"
            f"?per_page=100&page={page}"
        )
        batch = github_api_json(url, token)
        if not isinstance(batch, list):
            raise RuntimeError("GitHub returned an unexpected changed-files response.")
        results.extend(batch)
        if len(batch) < 100:
            return results
        page += 1


def review_pull_request(event: dict, repository: str, token: str) -> tuple[str, list[str]]:
    number = pull_request_number(event)
    changed = fetch_changed_files(repository, number, token)
    changed_files = [item["filename"] for item in changed]
    changed_lines = {
        item["filename"]: added_patch_lines(item.get("patch"))
        for item in changed
    }
    findings = PRReviewRunner().review(changed_files, changed_lines)
    return format_findings(findings), changed_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Review the pull request from a GitHub event.")
    parser.add_argument("--event-path", required=True)
    parser.add_argument("--output", default="pr-review.md")
    parser.add_argument("--changed-files-output", default="changed-files.txt")
    args = parser.parse_args()

    event = json.loads(Path(args.event_path).read_text(encoding="utf-8"))
    repository = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]

    review, changed_files = review_pull_request(event, repository, token)
    Path(args.output).write_text(review + "\n", encoding="utf-8")
    Path(args.changed_files_output).write_text(
        "".join(f"{path}\n" for path in changed_files),
        encoding="utf-8",
    )
    print(review)


if __name__ == "__main__":
    main()
