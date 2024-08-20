"""Command-line interface for ghstats."""

from __future__ import annotations

import sys

import click
from rich.console import Console

from gh_stats.display import language_chart, repos_table, user_table
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


@main.command()
@click.argument("username")
@click.option("--limit", "-n", default=10, show_default=True, help="Number of repos to display.")
@click.pass_context
def repos(ctx: click.Context, username: str, limit: int) -> None:
    """List public repositories sorted by stars."""
    client: GitHubClient = ctx.obj["client"]
    try:
        data = client.get_repos(username)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    console.print(repos_table(data, limit=limit))


@main.command()
@click.argument("username")
@click.option("--limit", "-n", default=10, show_default=True, help="Number of languages to display.")
@click.pass_context
def languages(ctx: click.Context, username: str, limit: int) -> None:
    """Show language breakdown across all public repos."""
    client: GitHubClient = ctx.obj["client"]
    try:
        with console.status("Fetching language data..."):
            data = client.get_languages(username)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)
    console.print(language_chart(data, limit=limit))
