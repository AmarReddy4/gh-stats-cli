"""GitHub API client using httpx."""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = "https://api.github.com"


class GitHubClient:
    """Lightweight wrapper around the GitHub REST API."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self._client = httpx.Client(base_url=BASE_URL, headers=headers, timeout=15.0)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get_user(self, username: str) -> dict[str, Any]:
        """Return profile data for *username*."""
        resp = self._client.get(f"/users/{username}")
        resp.raise_for_status()
        return resp.json()

    def get_repos(self, username: str, *, per_page: int = 100) -> list[dict[str, Any]]:
        """Return public repositories for *username* (paginated)."""
        repos: list[dict[str, Any]] = []
        page = 1
        while True:
            resp = self._client.get(
                f"/users/{username}/repos",
                params={"per_page": per_page, "page": page, "type": "owner", "sort": "updated"},
            )
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            repos.extend(batch)
            if len(batch) < per_page:
                break
            page += 1
        return repos

    def get_languages(self, username: str) -> dict[str, int]:
        """Aggregate language byte-counts across all public repos."""
        repos = self.get_repos(username)
        totals: dict[str, int] = {}
        for repo in repos:
            resp = self._client.get(f"/repos/{username}/{repo['name']}/languages")
            if resp.status_code != 200:
                continue
            for lang, byte_count in resp.json().items():
                totals[lang] = totals.get(lang, 0) + byte_count
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
