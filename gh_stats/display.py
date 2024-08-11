"""Rich formatting helpers for GitHub stats output."""

from __future__ import annotations

from typing import Any

from rich.table import Table


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
