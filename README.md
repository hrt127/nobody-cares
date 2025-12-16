# Nobody Cares - Daily Improvement Hub

A modular system for tracking daily activities, building skills portfolios, analyzing trading performance, and generating shareable artifacts. Built for incremental value over time.

**Your Edge System**: Track your unique intuition, connect insights across domains (trading, sports, code), and learn from YOUR patterns - not generic formulas.

## Quick Start

```bash
# Install
pip install -e .

# Daily entry
nc log trade "BTC long @ 45k, exit @ 46.2k, +2.6%"
nc log code "Fixed authentication bug, PR #123"
nc today  # View today's entries
nc week   # Weekly summary

# Quick capture (when overwhelmed)
nc q 100 "houston bet"

# Full context (when you have time)
nc risk sports_bet --cost 100 --odds 3.21 --my-probability 0.45 --what-i-see "Market slow" "Value bet"
```

## Key Features

### Your Edge System

- **Intuition Tracking**: Capture your gut feeling, what you see, why you trust it
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
