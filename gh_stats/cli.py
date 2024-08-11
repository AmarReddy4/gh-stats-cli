"""Command-line interface for ghstats."""

from __future__ import annotations

import sys

import click
from rich.console import Console

from gh_stats.display import user_table
from gh_stats.github import GitHubClient

console = Console()


@click.group()
@click.option("--token", envvar="GITHUB_TOKEN", default=None, help="GitHub personal access token.")
@click.pass_context
def main(ctx: click.Context, token: str | None) -> None:
    """Fetch and display GitHub user & repository statistics."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = GitHubClient(token=token)


@main.command()
@click.argument("username")
@click.pass_context
def user(ctx: click.Context, username: str) -> None:
    """Show profile statistics for a GitHub user."""
    client: GitHubClient = ctx.obj["client"]
    try:
        data = client.get_user(username)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    console.print(user_table(data))
