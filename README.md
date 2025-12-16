# Nobody Cares - Daily Improvement Hub

A modular system for tracking daily activities, building skills portfolios, analyzing trading performance, and generating shareable artifacts. Built for incremental value over time.

## Quick Start

```bash
# Install
pip install -e .

# Daily entry
nc log trade "BTC long @ 45k, exit @ 46.2k, +2.6%"
nc log code "Fixed authentication bug, PR #123"
nc today  # View today's entries
nc week   # Weekly summary
```

## Architecture

- **Phase 1**: Daily entry foundation
- **Phase 2**: Web3 alpha brief generator
- **Phase 3**: Automated data collection
- **Phase 4**: Trading performance analysis
- **Phase 5**: Skills & monetization tracking
- **Phase 6**: Improvement tracking & templates
- **Phase 7**: Output generation suite
- **Phase 8**: Pattern recognition & insights

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

