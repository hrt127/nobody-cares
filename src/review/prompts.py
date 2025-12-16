"""Review prompts and iteration suggestions"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..core.storage import Storage
from ..core.models import EntryType


def get_review_prompts(storage: Storage) -> List[str]:
    """Get review prompts based on current state"""
    prompts = []
    
    try:
        # Get open risks
        all_entries = storage.get_entries(entry_type=EntryType.RISK, limit=1000)
        open_risks = [e for e in all_entries if e.metadata.get('status') == 'open']
        
        if open_risks:
            prompts.append(f"{len(open_risks)} open risk(s) - update outcomes?")
        
        # Missing context (quick mode entries)
        quick_entries = [e for e in open_risks if e.metadata.get('quick_mode')]
        if quick_entries:
            prompts.append(f"{len(quick_entries)} quick entry/ies - add context?")
        
        # Recent outcomes without learning review
        recent_closed = [
            e for e in all_entries 
            if e.metadata.get('status') in ['closed', 'realized'] 
            and (datetime.now() - e.timestamp).days < 7
        ]
        if recent_closed:
            prompts.append(f"{len(recent_closed)} recent outcome(s) - review learnings?")
    except Exception:
        # If anything goes wrong, return empty prompts (don't break the flow)
        pass
    
    return prompts


def track_field_usage(storage: Storage) -> Dict[str, int]:
    """Track which fields are actually used"""
    field_usage = {}
    
    try:
        entries = storage.get_entries(entry_type=EntryType.RISK, limit=1000)
        
        # Fields to track
        fields_to_track = [
            'my_probability', 'market_probability', 'gut_feeling', 'trust_level',
            'what_i_see', 'why_i_trust_this', 'red_flags', 'pattern_match',
            'related_trades', 'related_alpha', 'related_code', 'domain_knowledge_applied',
            'cash_out_available', 'sportsbook', 'game_id', 'bet_type',
            'gas_fee', 'how_i_calculated', 'what_market_missing'
        ]
        
        for field in fields_to_track:
            count = sum(1 for e in entries if e.metadata.get(field) is not None)
            field_usage[field] = count
    except Exception:
        # Return empty dict if tracking fails
        pass
    
    return field_usage


def suggest_iterations(storage: Storage) -> Dict[str, Any]:
    """Suggest system improvements based on usage"""
    field_usage = track_field_usage(storage)
    
    # Find unused fields (used less than 10% of entries)
    total_entries = len(storage.get_entries(entry_type=EntryType.RISK, limit=1000))
    threshold = max(1, total_entries * 0.1)  # At least 10% usage
    
    unused_fields = [f for f, count in field_usage.items() if count < threshold]
    popular_fields = [f for f, count in field_usage.items() if count >= threshold * 2]
    
    suggestions = {
        'unused_fields': unused_fields,
        'popular_fields': popular_fields,
        'suggestions': []
    }
    
    if unused_fields:
        suggestions['suggestions'].append(
            f"Consider removing or simplifying: {', '.join(unused_fields[:5])}"
        )
    
    if popular_fields:
        suggestions['suggestions'].append(
            f"These fields work well for you: {', '.join(popular_fields[:5])}"
        )
    
    # Check for patterns
    entries = storage.get_entries(entry_type=EntryType.RISK, limit=100)
    quick_mode_count = sum(1 for e in entries if e.metadata.get('quick_mode'))
    
    if quick_mode_count > len(entries) * 0.5:
        suggestions['suggestions'].append(
            "You use quick mode often - consider making it even faster or adding defaults"
        )
    
    return suggestions
