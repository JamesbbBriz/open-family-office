#!/usr/bin/env python3
"""Idempotently seed the two canonical Open Family Office GitHub Discussions.

Requires GH_TOKEN with discussions:write. The repository must already have
GitHub Discussions enabled and the General + Announcements categories available.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com/graphql"

WELCOME_TITLE = "Welcome to Open Family Office — what should a personal family office understand?"
ANNOUNCEMENT_TITLE = "Open Family Office v0.5.1 — installable CLI, portable Agent Skills and trusted distribution"


def graphql(query: str, variables: dict) -> dict:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN is required")
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "open-family-office-discussion-seeder",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"GitHub GraphQL HTTP {exc.code}: {body}") from exc
    if data.get("errors"):
        raise RuntimeError("GitHub GraphQL errors: " + json.dumps(data["errors"]))
    return data["data"]


def repository_state(owner: str, name: str) -> tuple[str, dict[str, str], set[str]]:
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
        discussionCategories(first: 50) { nodes { id name } }
        discussions(first: 100) { nodes { title } }
      }
    }
    """
    repo = graphql(query, {"owner": owner, "name": name})["repository"]
    categories = {node["name"]: node["id"] for node in repo["discussionCategories"]["nodes"]}
    titles = {node["title"] for node in repo["discussions"]["nodes"]}
    return repo["id"], categories, titles


def create_discussion(repository_id: str, category_id: str, title: str, body: str) -> str:
    mutation = """
    mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {
        repositoryId: $repositoryId,
        categoryId: $categoryId,
        title: $title,
        body: $body
      }) {
        discussion { url }
      }
    }
    """
    data = graphql(
        mutation,
        {
            "repositoryId": repository_id,
            "categoryId": category_id,
            "title": title,
            "body": body,
        },
    )
    return data["createDiscussion"]["discussion"]["url"]


def main() -> int:
    repo = os.environ.get("GITHUB_REPOSITORY", "JamesbbBriz/open-family-office")
    if "/" not in repo:
        raise RuntimeError("GITHUB_REPOSITORY must be owner/name")
    owner, name = repo.split("/", 1)

    repository_id, categories, existing = repository_state(owner, name)
    missing = [name for name in ("General", "Announcements") if name not in categories]
    if missing:
        raise RuntimeError(
            "Missing required Discussion categories: "
            + ", ".join(missing)
            + ". Enable/create them in repository Discussions settings first."
        )

    items = [
        (
            "General",
            WELCOME_TITLE,
            ROOT / "docs/launch/discussions/welcome.md",
        ),
        (
            "Announcements",
            ANNOUNCEMENT_TITLE,
            ROOT / "docs/launch/discussions/v0.5.1.md",
        ),
    ]

    created = 0
    for category_name, title, path in items:
        if title in existing:
            print(f"Already exists: {title}")
            continue
        url = create_discussion(
            repository_id,
            categories[category_name],
            title,
            path.read_text(encoding="utf-8"),
        )
        print(f"Created: {url}")
        created += 1
    print(f"Discussion seeding complete; created {created} discussion(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, KeyError) as exc:
        print(f"Discussion seeding failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
