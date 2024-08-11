# gh-stats-cli

A CLI tool that fetches and displays GitHub user and repository statistics using the GitHub API. Built with Click and Rich for beautiful terminal output.

## Features

- **User profiles** — view key stats (followers, repos, bio, etc.) in a formatted table
- **Repository listing** — see top repos sorted by stars
- **Language breakdown** — visualize language usage across all public repos with a bar chart

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Show a user's profile stats
ghstats user torvalds

# List top repositories by stars
ghstats repos torvalds
ghstats repos torvalds --limit 20

# Show language breakdown
ghstats languages torvalds
ghstats languages torvalds --limit 5
```

### Authentication

For higher rate limits, set a GitHub personal access token:

```bash
export GITHUB_TOKEN=ghp_xxxxx
# or pass it directly
ghstats --token ghp_xxxxx user torvalds
```

Without a token the GitHub API allows 60 requests per hour; with a token you get 5,000.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## License

MIT
