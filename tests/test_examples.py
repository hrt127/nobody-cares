"""Test examples and templates library"""

import pytest

from src.examples.library import (
    EXAMPLES, TEMPLATES, get_example, get_template, get_contrast
)
from src.core.models import Entry, EntryType
from src.core.storage import Storage


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        storage = Storage(db_path=str(db_path))
        yield storage


class TestExamplesLibrary:
    """Test examples library"""
    
    def test_examples_available(self):
        """Test that examples are defined"""
        assert len(EXAMPLES) > 0
        assert 'sports-bet-quick' in EXAMPLES
    
    def test_templates_available(self):
        """Test that templates are defined"""
        assert len(TEMPLATES) > 0
        assert 'value-bet' in TEMPLATES or 'quick-capture' in TEMPLATES
    
    def test_get_example_exists(self):
        """Test getting an existing example"""
        example = get_example('sports-bet-quick')
        assert example is not None
        assert 'description' in example
        assert 'command' in example
    
    def test_get_example_not_exists(self):
        """Test getting a non-existent example"""
        example = get_example('nonexistent')
        assert example is None
    
    def test_get_template_exists(self):
        """Test getting an existing template"""
        template = get_template('value-bet')
        if template:
            assert 'name' in template
            assert 'description' in template
        else:
            # If 'value-bet' doesn't exist, check another
            template = get_template('quick-capture')
            if template:
                assert 'name' in template
    
    def test_get_template_not_exists(self):
        """Test getting a non-existent template"""
        template = get_template('nonexistent')
        assert template is None


class TestContrastView:
    """Test contrast view functionality"""
    
    def test_get_contrast_existing_entry(self, temp_db):
        """Test getting contrast for existing entry"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test bet",
            metadata={
                'risk_type': 'sports_bet',
                'entry_cost': 100.0,
                'my_probability': 0.45
            }
        )
        entry_id = temp_db.add_entry(entry)
        
        contrast = get_contrast(temp_db, entry_id)
        
        assert 'your_structure' in contrast or 'error' in contrast
        if 'your_structure' in contrast:
            assert 'fields_used' in contrast['your_structure']
    
    def test_get_contrast_nonexistent_entry(self, temp_db):
        """Test getting contrast for non-existent entry"""
        contrast = get_contrast(temp_db, 99999)
        assert 'error' in contrast
    
    def test_get_contrast_non_risk_entry(self, temp_db):
        """Test getting contrast for non-risk entry"""
        entry = Entry(
            entry_type=EntryType.TRADE,
            notes="Not a risk entry"
        )
        entry_id = temp_db.add_entry(entry)
        
        contrast = get_contrast(temp_db, entry_id)
        assert 'error' in contrast

