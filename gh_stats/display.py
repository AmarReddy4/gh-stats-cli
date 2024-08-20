"""Rich formatting helpers for GitHub stats output."""

from __future__ import annotations

from typing import Any

from rich.bar import Bar
from rich.table import Table
from rich.text import Text


def user_table(data: dict[str, Any]) -> Table:
    """Build a Rich table showing key profile statistics."""
    table = Table(title=f"GitHub Profile: {data['login']}", show_header=False, padding=(0, 2))
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("Name", data.get("name") or "—")
    table.add_row("Bio", data.get("bio") or "—")
    table.add_row("Location", data.get("location") or "—")
    table.add_row("Company", data.get("company") or "—")
    table.add_row("Public repos", str(data.get("public_repos", 0)))
    table.add_row("Public gists", str(data.get("public_gists", 0)))
    table.add_row("Followers", str(data.get("followers", 0)))
    table.add_row("Following", str(data.get("following", 0)))
    table.add_row("Created", data.get("created_at", "—")[:10])
    table.add_row("URL", data.get("html_url", "—"))

    return table


def repos_table(repos: list[dict[str, Any]], *, limit: int = 10) -> Table:
    """Build a Rich table of repositories sorted by star count."""
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:limit]

    table = Table(title=f"Top {limit} Repositories by Stars")
    table.add_column("#", style="dim", width=4)
    table.add_column("Repository", style="bold")
    table.add_column("Stars", justify="right", style="yellow")
    table.add_column("Forks", justify="right", style="green")
    table.add_column("Language", style="cyan")
    table.add_column("Description", max_width=48, no_wrap=True)

    for idx, repo in enumerate(sorted_repos, 1):
        table.add_row(
            str(idx),
            repo["name"],
            str(repo.get("stargazers_count", 0)),
            str(repo.get("forks_count", 0)),
            repo.get("language") or "—",
            (repo.get("description") or "—")[:48],
        )

    return table


def language_chart(languages: dict[str, int], *, limit: int = 10) -> Table:
    """Build a Rich bar-chart table showing language breakdown."""
    items = list(languages.items())[:limit]
    if not items:
        table = Table(title="Languages")
        table.add_column("Info")
        table.add_row("No language data available.")
        return table

    total = sum(v for _, v in items)

    table = Table(title="Language Breakdown", padding=(0, 1))
    table.add_column("Language", style="bold cyan", min_width=14)
    table.add_column("Bytes", justify="right", style="dim")
    table.add_column("%", justify="right", width=7)
    table.add_column("", width=30)

    colors = [
        "bright_blue", "bright_green", "bright_yellow", "bright_magenta",
        "bright_cyan", "bright_red", "blue", "green", "yellow", "magenta",
    ]

    for idx, (lang, byte_count) in enumerate(items):
        pct = (byte_count / total) * 100 if total else 0
        color = colors[idx % len(colors)]
        bar = Bar(size=pct, begin=0, end=100, color=color)
        table.add_row(lang, f"{byte_count:,}", f"{pct:.1f}%", bar)

    return table
