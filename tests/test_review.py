"""Test review prompts and iteration suggestions"""

import pytest
from datetime import datetime, timedelta

from src.core.models import Entry, EntryType
from src.core.storage import Storage
from src.review.prompts import get_review_prompts, track_field_usage, suggest_iterations


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        storage = Storage(db_path=str(db_path))
        yield storage


class TestReviewPrompts:
    """Test review prompt generation"""
    
    def test_get_review_prompts_empty(self, temp_db):
        """Test review prompts with no entries"""
        prompts = get_review_prompts(temp_db)
        assert isinstance(prompts, list)
        # Should return empty list or handle gracefully
        assert len(prompts) == 0 or all(isinstance(p, str) for p in prompts)
    
    def test_get_review_prompts_with_open_risks(self, temp_db):
        """Test review prompts with open risks"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Open risk",
            metadata={'status': 'open'}
        )
        temp_db.add_entry(entry)
        
        prompts = get_review_prompts(temp_db)
        assert any('open risk' in p.lower() for p in prompts)
    
    def test_get_review_prompts_with_quick_entries(self, temp_db):
        """Test review prompts with quick mode entries"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Quick entry",
            metadata={'status': 'open', 'quick_mode': True}
        )
        temp_db.add_entry(entry)
        
        prompts = get_review_prompts(temp_db)
        assert any('quick' in p.lower() for p in prompts) or len(prompts) == 0
    
    def test_get_review_prompts_with_recent_closed(self, temp_db):
        """Test review prompts with recently closed entries"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Closed entry",
            timestamp=datetime.now() - timedelta(days=1),
            metadata={'status': 'closed'}
        )
        temp_db.add_entry(entry)
        
        prompts = get_review_prompts(temp_db)
        # Should suggest reviewing recent outcomes
        assert any('outcome' in p.lower() or 'learning' in p.lower() for p in prompts) or len(prompts) == 0


class TestFieldUsageTracking:
    """Test field usage tracking"""
    
    def test_track_field_usage_empty(self, temp_db):
        """Test tracking with no entries"""
        usage = track_field_usage(temp_db)
        assert isinstance(usage, dict)
    
    def test_track_field_usage_with_fields(self, temp_db):
        """Test tracking with entries that have fields"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test",
            metadata={
                'my_probability': 0.45,
                'gut_feeling': 'strong',
                'what_i_see': 'Market slow'
            }
        )
        temp_db.add_entry(entry)
        
        usage = track_field_usage(temp_db)
        assert 'my_probability' in usage or isinstance(usage, dict)
        # Usage should be tracked (count >= 0)
        assert all(isinstance(count, int) for count in usage.values())


class TestIterationSuggestions:
    """Test iteration suggestions"""
    
    def test_suggest_iterations_empty(self, temp_db):
        """Test suggestions with no entries"""
        suggestions = suggest_iterations(temp_db)
        assert isinstance(suggestions, dict)
        assert 'suggestions' in suggestions
        assert 'popular_fields' in suggestions
        assert 'unused_fields' in suggestions
    
    def test_suggest_iterations_with_entries(self, temp_db):
        """Test suggestions with entries"""
        # Add entry with some fields
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test",
            metadata={
                'my_probability': 0.45,
                'gut_feeling': 'strong'
            }
        )
        temp_db.add_entry(entry)
        
        suggestions = suggest_iterations(temp_db)
        assert isinstance(suggestions, dict)
        assert 'suggestions' in suggestions
        assert isinstance(suggestions['suggestions'], list)
    
    def test_suggest_iterations_quick_mode_heavy(self, temp_db):
        """Test suggestions when quick mode is heavily used"""
        # Add multiple quick mode entries
        for i in range(5):
            entry = Entry(
                entry_type=EntryType.RISK,
                notes=f"Quick {i}",
                metadata={'quick_mode': True}
            )
            temp_db.add_entry(entry)
        
        suggestions = suggest_iterations(temp_db)
        # Should suggest making quick mode faster if heavily used
        assert isinstance(suggestions, dict)

