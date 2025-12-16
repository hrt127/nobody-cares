"""Pattern detection - repeated deviations, corrections, cost of drift"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..core.storage import Storage
from ..core.models import EntryType


def detect_misalignment_patterns(storage: Storage, days: int = 90) -> Dict[str, Any]:
    """Detect repeated deviations from self (misalignment patterns)
    
    Returns patterns where aligned_with_self=False over time.
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        entries = storage.get_entries(entry_type=EntryType.RISK, start_date=cutoff_date, limit=1000)
        
        misaligned = []
        aligned = []
        
        for entry in entries:
            risk_data = entry.metadata or {}
            aligned_flag = risk_data.get('aligned_with_self')
            
            if aligned_flag is False:
                misaligned.append({
                    'id': entry.id,
                    'date': entry.timestamp,
                    'ownership': risk_data.get('ownership'),
                    'voluntary': risk_data.get('voluntary'),
                    'voices_present': risk_data.get('voices_present', []),
                    'motivation_type': risk_data.get('motivation_type'),
                    'cost': risk_data.get('entry_cost', 0),
                    'currency': risk_data.get('currency', 'USD')
                })
            elif aligned_flag is True:
                aligned.append({
                    'id': entry.id,
                    'date': entry.timestamp
                })
        
        return {
            'misaligned_count': len(misaligned),
            'aligned_count': len(aligned),
            'misalignment_rate': len(misaligned) / len(entries) if entries else 0,
            'misaligned_entries': misaligned[:10],  # Top 10
            'pattern': _analyze_misalignment_pattern(misaligned)
        }
    except Exception:
        return {'error': 'Failed to detect patterns'}


def detect_drift_patterns(storage: Storage, days: int = 90) -> Dict[str, Any]:
    """Detect repeated corrections back to self (drift patterns)
    
    Shows when you corrected course after misalignment.
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        entries = storage.get_entries(entry_type=EntryType.RISK, start_date=cutoff_date, limit=1000)
        
        # Sort by date
        entries_sorted = sorted(entries, key=lambda e: e.timestamp)
        
        corrections = []
        drift_sequences = []
        
        prev_aligned = None
        current_sequence = []
        
        for entry in entries_sorted:
            risk_data = entry.metadata or {}
            aligned = risk_data.get('aligned_with_self')
            
            if prev_aligned is False and aligned is True:
                # Correction: was misaligned, now aligned
                corrections.append({
                    'id': entry.id,
                    'date': entry.timestamp,
                    'days_since_misalignment': (entry.timestamp - current_sequence[0]['date']).days if current_sequence else 0
                })
                if current_sequence:
                    drift_sequences.append(current_sequence)
                current_sequence = []
            elif aligned is False:
                # Drift: misaligned
                if not current_sequence:
                    current_sequence = []
                current_sequence.append({
                    'id': entry.id,
                    'date': entry.timestamp
                })
            
            prev_aligned = aligned
        
        return {
            'corrections_count': len(corrections),
            'drift_sequences_count': len(drift_sequences),
            'corrections': corrections[:10],
            'longest_drift': max([len(s) for s in drift_sequences], default=0)
        }
    except Exception:
        return {'error': 'Failed to detect drift patterns'}


def analyze_ownership_correlation(storage: Storage, days: int = 90) -> Dict[str, Any]:
    """Analyze correlation between ownership type and outcomes
    
    Does "mine" correlate with better outcomes than "influenced" or "performed"?
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        entries = storage.get_entries(entry_type=EntryType.RISK, start_date=cutoff_date, limit=1000)
        
        by_ownership = {
            'mine': [],
            'influenced': [],
            'performed': []
        }
        
        for entry in entries:
            risk_data = entry.metadata or {}
            ownership = risk_data.get('ownership')
            realized = risk_data.get('realized_value')
            cost = risk_data.get('entry_cost', 0)
            
            if ownership and realized is not None and cost > 0:
                pnl = realized - cost
                roi = (pnl / cost) * 100 if cost > 0 else 0
                
                if ownership in by_ownership:
                    by_ownership[ownership].append({
                        'pnl': pnl,
                        'roi': roi,
                        'id': entry.id
                    })
        
        # Calculate averages
        results = {}
        for ownership_type, outcomes in by_ownership.items():
            if outcomes:
                avg_pnl = sum(o['pnl'] for o in outcomes) / len(outcomes)
                avg_roi = sum(o['roi'] for o in outcomes) / len(outcomes)
                results[ownership_type] = {
                    'count': len(outcomes),
                    'avg_pnl': avg_pnl,
                    'avg_roi': avg_roi
                }
        
        return results
    except Exception:
        return {'error': 'Failed to analyze ownership correlation'}


def _analyze_misalignment_pattern(misaligned: List[Dict]) -> Dict[str, Any]:
    """Analyze common patterns in misaligned entries"""
    if not misaligned:
        return {}
    
    # Count by ownership type
    ownership_counts = {}
    for entry in misaligned:
        ownership = entry.get('ownership', 'unknown')
        ownership_counts[ownership] = ownership_counts.get(ownership, 0) + 1
    
    # Count by voices present
    voice_counts = {}
    for entry in misaligned:
        voices = entry.get('voices_present', [])
        for voice in voices:
            voice_counts[voice] = voice_counts.get(voice, 0) + 1
    
    # Count by motivation type
    motivation_counts = {}
    for entry in misaligned:
        motivation = entry.get('motivation_type', 'unknown')
        motivation_counts[motivation] = motivation_counts.get(motivation, 0) + 1
    
    return {
        'ownership_distribution': ownership_counts,
        'voices_distribution': voice_counts,
        'motivation_distribution': motivation_counts
    }
