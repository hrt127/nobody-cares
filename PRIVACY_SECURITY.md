# Privacy & Security

## What You're Logging

**Data Types:**

- Risk entries (bets, trades, decisions)
- Financial amounts (costs, outcomes, currencies)
- Your intuition & observations (structured patterns, not feelings)
- Agency & ownership tracking (mine/influenced/performed)
- Cross-domain connections (linking entries)
- Pattern detection data (misalignment, drift, correlations)

**What's NOT Logged:**

- Personal identifying information (names, addresses, etc.)
- Sensitive credentials (API keys, passwords)
- External account details (bank accounts, exchange accounts)
- Third-party data (only your observations about it)

---

## Where It's Stored

**Storage Location:**

- **Local SQLite database:** `data/nobody_cares.db`
- **Location:** On your machine only (project root `data/` directory)
- **Format:** SQLite (standard database file)
- **Backup:** You control backups (it's just a file)

**Security:**

- ✅ **Local only** - No cloud, no external servers
- ✅ **No network** - Database never leaves your machine
- ✅ **No telemetry** - No tracking, no analytics
- ✅ **Your data** - You own it completely

**Privacy:**

- All data stored locally on your machine
- No data sent anywhere (no API calls for storage)
- No third-party services involved in storage
- You can delete the database file anytime

---

## How to Log

**Methods:**

1. **CLI commands** - `nc risk`, `nc q`, etc.
2. **Direct file access** - Edit database directly (advanced)
3. **Python API** - Import and use `Storage` class programmatically

**Typical Usage:**

```bash
# Quick capture (minimal data)
nc q 100 "bet"

# Full entry (detailed data)
nc risk sports_bet --cost 100 --odds 2.5 "full context"
```

**Minimum Data Required:**

- Cost/amount (can be 0 for non-financial entries)
- Notes (brief description)

**Everything else is optional** - add details later if needed.

---

## Minimum Specs

**Requirements:**

- **Python:** 3.10 or higher
- **Storage:** ~1MB per 1000 entries (SQLite is lightweight)
- **Dependencies:** Standard Python packages (see `pyproject.toml`)
- **OS:** Linux, macOS, Windows (WSL2 tested)

**Typical Setup:**

```bash
# Install
pip install -e .

# First use creates database automatically
nc today
```

**No special permissions needed:**

- No network access required
- No admin/root privileges
- No external services
- Just file system access (to create `data/` directory)

---

## Data Safety

**Backup:**

- Database is a single file: `data/nobody_cares.db`
- Copy it anywhere (USB, cloud, etc.)
- Restore by placing file back in `data/` directory

**Deletion:**

- Delete `data/nobody_cares.db` to remove all data
- No traces left (it's just a file)

**Migration:**

- SQLite format is portable
- Works across platforms
- Can be opened with any SQLite tool

---

## What's Safe to Log

**✅ Safe:**

- Financial amounts (costs, outcomes)
- Your observations & patterns
- Decision-making data
- Risk assessments
- Pattern matches
- Cross-domain connections

**⚠️ Be Careful:**

- Don't log actual API keys or passwords
- Don't log sensitive account numbers
- Don't log personal information about others
- Don't log anything you wouldn't want in a local file

**❌ Don't Log:**

- Passwords or secrets
- API keys or tokens
- Bank account numbers
- Social security numbers
- Other people's personal information

---

## Best Practices

1. **Keep it local** - Database stays on your machine
2. **Backup regularly** - Copy `data/nobody_cares.db` somewhere safe
3. **Don't commit database** - Already in `.gitignore`
4. **Log patterns, not secrets** - Focus on observations, not credentials
5. **Review periodically** - Use `nc review` to see what you've logged

---

## Summary

- **What:** Your risk entries, observations, patterns (structured data)
- **Where:** Local SQLite database on your machine only
- **Security:** No cloud, no network, no external services
- **Privacy:** Your data, your control, completely local
- **Minimum:** Python 3.10+, ~1MB storage per 1000 entries
- **Safe:** Log patterns and observations, not secrets or credentials

**Bottom line:** Everything stays on your machine. You own it. You control it.

---

## Public Repository, Private Data

**Code is public, data stays private.** Your database (`data/nobody_cares.db`) is ignored by `.gitignore`, so it never gets committed to Git. Anyone can clone the code, but they create their own database when they first run it. Your personal data never leaves your machine.
