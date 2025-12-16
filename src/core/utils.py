"""Utility functions"""

from datetime import datetime, timedelta
from typing import List, Optional
import re


def parse_tags(text: str) -> List[str]:
    """Extract tags from text (format: --tags tag1,tag2 or #tag1 #tag2)"""
    tags = []
    
    # Extract from --tags flag format
    tags_match = re.search(r'--tags\s+([^\s]+)', text)
    if tags_match:
        tags.extend([t.strip() for t in tags_match.group(1).split(',')])
    
    # Extract hashtags
    hashtags = re.findall(r'#(\w+)', text)
    tags.extend(hashtags)
    
    return list(set(tags))  # Remove duplicates


def parse_entry_type(text: str) -> Optional[str]:
    """Try to infer entry type from text"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['trade', 'long', 'short', 'exit', 'entry', 'pnl']):
        return 'trade'
    elif any(word in text_lower for word in ['commit', 'pr', 'bug', 'fix', 'code', 'repo']):
        return 'code'
    elif any(word in text_lower for word in ['alpha', 'signal', 'narrative', 'protocol']):
        return 'alpha'
    elif any(word in text_lower for word in ['learn', 'course', 'tutorial', 'module']):
        return 'learning'
    elif any(word in text_lower for word in ['action', 'task', 'todo', 'research']):
        return 'action'
    elif any(word in text_lower for word in ['job', 'opportunity', 'consulting', 'offer']):
        return 'opportunity'
    else:
        return 'note'


def get_week_start(date: datetime) -> datetime:
    """Get start of week (Monday) for a given date"""
    days_since_monday = date.weekday()
    return (date - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)


def get_week_end(date: datetime) -> datetime:
    """Get end of week (Sunday) for a given date"""
    week_start = get_week_start(date)
    return week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

