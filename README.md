# Dependabot Policy Enforcer

A GitHub Action that enforces age-based policies on Dependabot security alerts. It helps teams maintain security by ensuring that vulnerabilities are addressed within specified timeframes based on their severity.

## Features

- Checks open Dependabot alerts against configurable age thresholds
- Supports different thresholds for Critical, High, Medium, and Low severity alerts
- Provides detailed reports in PR comments and workflow logs
- Optional report-only mode for monitoring without failing builds

## Usage

```yaml
name: Check Dependabot Alerts
on:
  schedule:
    - cron: '0 0 * * *'  # Daily check
  pull_request:
  workflow_dispatch:

permissions:
  security-events: read
  contents: read
  pull-requests: write  # Required for PR comments

jobs:
  check-alerts:
    runs-on: ubuntu-latest
    steps:
      - uses: your-username/dependabot-alert-checker@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          critical-threshold: 3
          high-threshold: 5
          medium-threshold: 14
          low-threshold: 30
          report-mode: false
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | GitHub token with security alerts read permission | Yes | N/A |
| `critical-threshold` | Maximum age in days for Critical severity alerts | No | 3 |
| `high-threshold` | Maximum age in days for High severity alerts | No | 5 |
| `medium-threshold` | Maximum age in days for Medium severity alerts | No | 14 |
| `low-threshold` | Maximum age in days for Low severity alerts | No | 30 |
| `report-mode` | Run in report-only mode without failing | No | false |

## Permissions

This action requires:
- `security-events: read` to access Dependabot alerts
- `contents: read` to access repository content
- `pull-requests: write` (optional) to post comments on PRs

## Development

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

