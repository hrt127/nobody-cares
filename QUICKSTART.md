# Quick Start Guide

Get up and running in 5 minutes.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run your first command
nc --help
```

## Your First Log

**Quick capture (when overwhelmed):**

```bash
nc q 100 "test bet"
```

**Full entry (when you have time):**

```bash
nc risk sports_bet --cost 100 --odds 2.5 "My first bet"
```

## Common Commands

```bash
# Quick capture
nc q <cost> "<notes>"

# List your risks
nc risks

# See today's activity
nc today

# Update a risk
nc update-risk <id> --status closed --realized-value 150

# See examples
nc examples list
```

## Privacy & Security

**Quick summary:**

- Data stored locally only (`data/nobody_cares.db`)
- No cloud, no network, no external services
- Python 3.10+, ~1MB per 1000 entries
- See [PRIVACY_SECURITY.md](PRIVACY_SECURITY.md) for details

## What Next?

- **New to this?** → See [WHEN_TO_LOG.md](WHEN_TO_LOG.md) for practical examples
- **Want deeper workflows?** → See [DAILY_GUIDE.md](DAILY_GUIDE.md)
- **Understanding the system?** → See [README.md](README.md)
- **Understanding the codebase?** → See [INDEX.md](INDEX.md) for repository structure

---

**Key Principle:** Log as you go, not after. If it takes more than 60 seconds, it's not signal.
