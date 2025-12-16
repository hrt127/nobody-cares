"""Test content generation functionality"""

import pytest
from datetime import datetime

from src.core.models import Entry, EntryType
from src.core.storage import Storage
from src.outputs.content import ContentGenerator


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    import tempfile
    import os
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        storage = Storage(db_path=str(db_path))
        yield storage


class TestContentGenerator:
    """Test ContentGenerator"""
    
    def test_generate_twitter_basic(self, temp_db):
        """Test basic Twitter generation"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test bet",
            metadata={
                'risk_type': 'sports_bet',
                'entry_cost': 100.0,
                'currency': 'USD',
                'odds_or_price': 3.21,
                'my_probability': 0.45,
                'edge_pct': 12.5
            }
        )
        entry_id = temp_db.add_entry(entry)
        entries = temp_db.get_entries(limit=10000)
        entry = next((e for e in entries if e.id == entry_id), None)
        
        generator = ContentGenerator(temp_db)
        content = generator.generate_twitter(entry, brevity='medium')
        
        assert "bet" in content.lower() or "insight" in content.lower()
        assert "100" in content or "USD" in content
    
    def test_generate_twitter_high_brevity(self, temp_db):
        """Test Twitter generation with high brevity"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test",
            metadata={
                'entry_cost': 100.0,
                'currency': 'USD'
            }
        )
        entry_id = temp_db.add_entry(entry)
        entries = temp_db.get_entries(limit=10000)
        entry = next((e for e in entries if e.id == entry_id), None)
        
        generator = ContentGenerator(temp_db)
        content = generator.generate_twitter(entry, brevity='high')
        
        assert "Quick" in content or "insight" in content.lower()
    
    def test_generate_linkedin(self, temp_db):
        """Test LinkedIn post generation"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test bet with learning",
            metadata={
                'risk_type': 'sports_bet',
                'entry_cost': 100.0,
                'currency': 'USD',
                'my_probability': 0.45,
                'what_i_see': 'Market slow to react'
            }
        )
        entry_id = temp_db.add_entry(entry)
        entries = temp_db.get_entries(limit=10000)
        entry = next((e for e in entries if e.id == entry_id), None)
        
        generator = ContentGenerator(temp_db)
        content = generator.generate_linkedin(entry)
        
        assert len(content) > 0
        assert "bet" in content.lower() or "insight" in content.lower() or "learning" in content.lower()
    
    def test_generate_blog(self, temp_db):
        """Test blog post generation"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Detailed analysis of a bet",
            metadata={
                'risk_type': 'sports_bet',
                'entry_cost': 100.0,
                'currency': 'USD',
                'my_probability': 0.45,
                'what_i_see': 'Market inefficiency',
                'why_i_trust_this': 'Past experience'
            }
        )
        entry_id = temp_db.add_entry(entry)
        entries = temp_db.get_entries(limit=10000)
        entry = next((e for e in entries if e.id == entry_id), None)
        
        generator = ContentGenerator(temp_db)
        content = generator.generate_blog(entry)
        
        assert len(content) > 100  # Blog should be longer
        assert "analysis" in content.lower() or "bet" in content.lower()
    
    def test_filter_content(self, temp_db):
        """Test content filtering"""
        generator = ContentGenerator(temp_db)
        
        content = "This is about trading.\nCrypto is interesting.\nNFTs are cool."
        
        # Include filter
        filtered = generator.filter_content(content, include=['trading', 'Crypto'])
        assert "trading" in filtered or "Crypto" in filtered
        
        # Exclude filter
        filtered = generator.filter_content(content, exclude=['NFTs'])
        assert "NFTs" not in filtered
    
    def test_generate_with_missing_metadata(self, temp_db):
        """Test generation with minimal metadata"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Minimal entry",
            metadata={}
        )
        entry_id = temp_db.add_entry(entry)
        entries = temp_db.get_entries(limit=10000)
        entry = next((e for e in entries if e.id == entry_id), None)
        
        generator = ContentGenerator(temp_db)
        
        # Should not crash with missing metadata
        twitter = generator.generate_twitter(entry)
        linkedin = generator.generate_linkedin(entry)
        blog = generator.generate_blog(entry)
        
        assert len(twitter) > 0
        assert len(linkedin) > 0
        assert len(blog) > 0

