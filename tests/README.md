# Test Suite Overview

## Test Coverage

The test suite provides minimum viable testing for all core functionality:

### Core Components (44 tests total)

1. **Models** (`test_models.py`) - 6 tests
   - Entry creation and metadata
   - RiskEntry with reward history
   - Project and Improvement models

2. **Storage** (`test_storage.py`) - 11 tests
   - Entry CRUD operations
   - Project management
   - Improvement tracking
   - Trade storage (single and batch)
   - Skill management
   - Metadata updates

3. **CLI** (`test_cli.py`) - 8 tests
   - Basic logging commands
   - Project management
   - Risk tracking commands
   - Improvement commands

4. **Risk Tracking** (`test_risk_tracking.py`) - 3 tests
   - Risk entry logging
   - Reward updates over time
   - Opportunity cost tracking

5. **Importers** (`test_importers.py`) - 3 tests
   - CSV validation
   - Trading data parsing
   - Metrics calculation

6. **Output Generators** (`test_outputs.py`) - 4 tests
   - Twitter thread generation
   - LinkedIn post generation
   - Video script generation
   - PDF generator import

7. **Alpha Brief** (`test_alpha.py`) - 3 tests
   - Brief generation
   - Action item extraction
   - Brief formatting

8. **Utils** (`test_utils.py`) - 3 tests
   - Week start/end calculations
   - Date consistency

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_storage.py

# Run specific test
pytest tests/test_storage.py::TestStorage::test_add_and_get_entry

# Run with coverage
pytest --cov=src --cov-report=html
```

## Test Fixtures

- `temp_db`: Creates a temporary SQLite database for each test
- `cli_runner`: Click CLI test runner
- `isolated_env`: Isolated filesystem for CLI tests
- `sample_project`: Sample project with trades for output tests

## Adding New Tests

When adding new functionality:

1. Add model tests in `test_models.py`
2. Add storage tests in `test_storage.py`
3. Add CLI tests in `test_cli.py`
4. Add feature-specific tests in dedicated files

Follow the existing patterns:
- Use fixtures for database setup
- Test both success and edge cases
- Keep tests isolated and independent
- Use descriptive test names

