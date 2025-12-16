"""Test utility functions"""

import pytest
from datetime import datetime, timedelta

from src.core.utils import get_week_start, get_week_end


class TestUtils:
    """Test utility functions"""
    
    def test_get_week_start(self):
        """Test getting start of week (Monday)"""
        # Test with a Wednesday
        wed = datetime(2024, 1, 3)  # Wednesday
        week_start = get_week_start(wed)
        
        # Should be Monday (Jan 1, 2024)
        assert week_start.weekday() == 0  # Monday
        assert week_start.day == 1
        assert week_start.month == 1
    
    def test_get_week_end(self):
        """Test getting end of week (Sunday)"""
        # Test with a Wednesday
        wed = datetime(2024, 1, 3)  # Wednesday
        week_end = get_week_end(wed)
        
        # Should be Sunday (Jan 7, 2024)
        assert week_end.weekday() == 6  # Sunday
        assert week_end.day == 7
        assert week_end.month == 1
    
    def test_week_start_end_consistency(self):
        """Test that week start and end are consistent"""
        test_date = datetime(2024, 1, 15)  # Monday
        week_start = get_week_start(test_date)
        week_end = get_week_end(test_date)
        
        # Week should be 7 days
        delta = week_end - week_start
        assert delta.days == 6  # Monday to Sunday inclusive is 6 days difference
        assert delta.seconds == 86399  # 23:59:59

