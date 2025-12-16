# Nobody Cares - Daily Improvement Hub

A modular system for tracking daily activities, building skills portfolios, analyzing trading performance, and generating shareable artifacts. Built for incremental value over time.

**Your Edge System**: Track your unique intuition, connect insights across domains (trading, sports, code), and learn from YOUR patterns - not generic formulas.

## Quick Start

**New to this?** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute getting started guide.  
**Not sure when to log?** See [WHEN_TO_LOG.md](WHEN_TO_LOG.md) for practical examples and a checklist.  
**Understanding the codebase?** See [INDEX.md](INDEX.md) for repository structure and extension points.  
**Extended documentation?** See [docs/](docs/) folder for additional technical docs.  
**Extended documentation?** See [docs/](docs/) folder for additional technical docs.

**Basic commands:**

```bash
# Quick capture (when overwhelmed)
nc q 100 "houston bet"

# Full context (when you have time)
nc risk sports_bet --cost 100 --odds 3.21 --my-probability 0.45 --what-i-saw "Market slow" "Value bet"

# List your risks
nc risks

# See today's activity
nc today
```

## Key Features

### Your Edge System

- **Agency & Ownership Tracking**: Binary data (mine/influenced/performed, aligned/not aligned, voluntary/pressure)
- **Influence Surface**: Track who gets access to influence you (voices_present array)
- **Motivation Integrity**: Classification (internal/external, alignment/expectation/avoidance/pruning)
- **Structured Intuition**: Observable patterns (what_i_saw, why_it_mattered) - not feelings
- **Pattern Detection**: Longitudinal patterns (misalignment, drift, ownership correlation)
- **Cross-Domain Connections**: Link sports betting to trading, alpha, code
- **Multi-Currency Support**: Track any currency (USD, ETH, BTC, SOL, etc.) with gas fee tracking
- **Cash-Out Tracking**: Track when you can't cash out - where value gets lost
- **Quick Capture Mode**: Ultra-fast entry when overwhelmed (`nc q <cost> <notes>`)

### Content Generation

- **One Source, Many Outputs**: Generate Twitter, LinkedIn, blog from same entry
- **Brevity Control**: High/medium/low - system helps you be concise
- **Lesson Extraction**: Automatically extract hard-won lessons from outcomes
- **Distribution**: Prepare content for multiple platforms

### Review & Iterate

- **Pattern Detection**: Detect misalignment patterns, drift patterns, ownership correlation
- **Learning Reviews**: Periodic reviews without prompts - must answer authoritatively (`nc learn`)
- **Pattern Export**: Export pattern data to CSV for external analysis (`nc patterns export`)
- **Not Daily Habits**: Frequent review cycles, adapt system to YOUR process
- **Usage Analytics**: See what you use vs skip
- **System Adaptation**: Remove unused complexity, add what you need
- **Examples Library**: See what others do, stay grounded

## Architecture

- **Phase 1**: Daily entry foundation ✅
- **Phase 2**: Web3 alpha brief generator ✅
- **Phase 3**: Automated data collection ✅
- **Phase 4**: Trading performance analysis ✅
- **Phase 5**: Skills & monetization tracking ✅
- **Phase 6**: Improvement tracking & templates ✅
- **Phase 7**: Output generation suite ✅
- **Phase 8**: Pattern recognition & insights ✅
- **Phase 9**: Your Edge System (sports betting, intuition tracking, multi-currency) ✅

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src/

# Type check
mypy src/
```

## Testing

The project includes comprehensive tests covering:

- **Core Models** (`tests/test_models.py`): Entry, Project, Improvement, RiskEntry models
- **Storage Layer** (`tests/test_storage.py`): Database operations, CRUD for all entities
- **CLI Commands** (`tests/test_cli.py`): All CLI commands including risk tracking
- **Risk Tracking** (`tests/test_risk_tracking.py`): Risk entry logging, reward updates, opportunity cost tracking
- **Data Importers** (`tests/test_importers.py`): CSV parsing and trading performance analysis
- **Output Generators** (`tests/test_outputs.py`): Twitter, LinkedIn, video script generation
- **Alpha Brief** (`tests/test_alpha.py`): Alpha brief generation and formatting
- **Utilities** (`tests/test_utils.py`): Helper functions

Run all tests:

```bash
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_storage.py -v
```

Run with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

## Error Handling & Fallbacks

The system includes comprehensive error handling:

- **Input Validation**: Probabilities (0-1), costs (>0), odds (>0) with helpful error messages
- **Graceful Degradation**: Missing metadata handled, defaults provided
- **Storage Errors**: Try/catch blocks, helpful error messages
- **Multi-Currency**: Handles any currency, doesn't break on unknown formats
- **Review Prompts**: Won't break if database issues occur
- **Content Generation**: Handles missing data gracefully

All error messages include hints (e.g., "Use 0.45 for 45%, not 45").

## Privacy & Security

**What you're logging:** Risk entries, observations, patterns (structured data)  
**Where it's stored:** Local SQLite database on your machine only (`data/nobody_cares.db`)  
**Security:** No cloud, no network, no external services - completely local  
**Public repo, private data:** Code is public, your database is ignored by `.gitignore`  
**Minimum specs:** Python 3.10+, ~1MB per 1000 entries, no special permissions needed

See [PRIVACY_SECURITY.md](PRIVACY_SECURITY.md) for details.

---

## Major Shifts

See [docs/MAJOR_SHIFTS.md](docs/MAJOR_SHIFTS.md) for details on:

- Agency & Ownership tracking (binary data, not narrative)
- Structured intuition fields (observable patterns, not feelings)
- Influence surface tracking (access control, not emotion)
- Pattern detection queries (longitudinal patterns, not mood)

**Key Principle**: This is a **personal signal extraction engine**, not a feelings database.
