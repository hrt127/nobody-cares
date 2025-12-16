"""Learning review system - periodic reviews without prompts

Focus: Principles vs preferences. Self-accountability. Staying uncomfortable.
Must answer authoritatively without resources.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..core.storage import Storage
from ..core.models import EntryType


def generate_review_questions(storage: Storage, days: int = 90) -> List[str]:
    """Generate review questions based on logged data
    
    NO prefilled answers. Must answer authoritatively.
    Questions get harder as you log more.
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        entries = storage.get_entries(entry_type=EntryType.RISK, start_date=cutoff_date, limit=1000)
        
        if not entries:
            return []
        
        questions = []
        
        # Basic questions (always asked)
        questions.append("What patterns do you see in your risk entries?")
        questions.append("What principles guide your decisions? (Not preferences - principles)")
        questions.append("When do you deviate from yourself? What triggers it?")
        
        # Pattern-based questions (if enough data)
        if len(entries) >= 10:
            questions.append("What ownership type (mine/influenced/performed) correlates with better outcomes?")
            questions.append("What voices influence you? Do they help or hurt?")
            questions.append("What's your misalignment rate? What does it mean?")
        
        if len(entries) >= 20:
            questions.append("What transferable skills have you learned from logging?")
            questions.append("What patterns repeat? What do they teach you?")
            questions.append("Where are you uncomfortable? (That's where living happens)")
        
        if len(entries) >= 50:
            questions.append("What principles have you discovered? (Not preferences)")
            questions.append("What have you learned about yourself that you didn't know?")
            questions.append("What keeps you in positive loops? What breaks them?")
        
        # Advanced questions (if extensive logging)
        if len(entries) >= 100:
            questions.append("What's your edge? How do you know?")
            questions.append("What patterns across domains (sports, trading, code) do you see?")
            questions.append("What have you learned that's transferable?")
        
        return questions[:10]  # Limit to 10 questions
        
    except Exception:
        return []


def get_review_schedule() -> Dict[str, str]:
    """Get review schedule - how often to review"""
    return {
        "Early stage (< 10 entries)": "Weekly",
        "Building (< 50 entries)": "Bi-weekly",
        "Established (50+ entries)": "Monthly",
        "Advanced (100+ entries)": "Quarterly"
    }


def check_review_due(storage: Storage) -> Dict[str, Any]:
    """Check if review is due based on last review and entry count"""
    try:
        # Get entry count
        entries = storage.get_entries(entry_type=EntryType.RISK, limit=1000)
        count = len(entries)
        
        # Determine schedule based on count
        if count < 10:
            frequency_days = 7  # Weekly
        elif count < 50:
            frequency_days = 14  # Bi-weekly
        elif count < 100:
            frequency_days = 30  # Monthly
        else:
            frequency_days = 90  # Quarterly
        
        # Check last review (stored in metadata or separate table)
        # For now, always suggest review (can enhance later)
        return {
            'due': True,
            'reason': f"Review recommended ({count} entries logged, review every {frequency_days} days)",
            'frequency_days': frequency_days,
            'entry_count': count
        }
        
    except Exception:
        return {
            'due': True,
            'reason': 'Unable to determine - suggest review',
            'frequency_days': 30,
            'entry_count': 0
        }
