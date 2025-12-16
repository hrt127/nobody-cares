"""Test alpha brief generator"""

import pytest
from datetime import datetime

from src.core.storage import Storage
from src.alpha import AlphaBriefGenerator, BriefFormatter
from src.core.models import AlphaSignal, ActionItem, AlphaBrief


class TestAlphaBriefGenerator:
    """Test alpha brief generation"""
    
    def test_generate_brief(self, temp_db):
        """Test generating an alpha brief"""
        generator = AlphaBriefGenerator(temp_db)
        brief = generator.generate_brief()
        
        assert brief is not None
        assert brief.date is not None
        assert isinstance(brief.early_signals, list)
        assert isinstance(brief.conflicting_views, list)
        assert isinstance(brief.action_items, list)
        assert isinstance(brief.blind_spots, list)
    
    def test_extract_action_items(self, temp_db):
        """Test action item extraction from text"""
        generator = AlphaBriefGenerator(temp_db)
        
        text = """
        Task | Category | Time | Urgency | Tools Needed
        Research X protocol | Research | 30m | High | DefiLlama
        Map restaking protocols | Analysis | 45m | Medium | L2Beat
        """
        
        action_items = generator.extract_action_items(text)
        assert len(action_items) > 0
    
    def test_brief_formatter(self, temp_db):
        """Test brief formatting"""
        formatter = BriefFormatter()
        
        brief = AlphaBrief(
            date=datetime.now(),
            early_signals=[
                AlphaSignal(
                    signal_type='early_signal',
                    content="New protocol launching",
                    source="email"
                )
            ],
            action_items=[
                ActionItem(
                    task="Research protocol",
                    category="Research",
                    time_estimate="30m",
                    urgency="high"
                )
            ]
        )
        
        markdown = formatter.format_brief(brief)
        assert len(markdown) > 0
        assert "Early Signals" in markdown or "early signals" in markdown.lower()
        assert "Action Items" in markdown or "action items" in markdown.lower()

