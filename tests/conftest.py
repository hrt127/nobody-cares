"""Pytest configuration and fixtures"""

import pytest
import tempfile
from pathlib import Path

from src.core.storage import Storage


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)
    
    storage = Storage(db_path=db_path)
    yield storage
    
    # Cleanup
    if db_path.exists():
        db_path.unlink()

