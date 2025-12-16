"""Alpha brief generator - processes emails and on-chain data to generate daily briefs"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path

from ..core.models import AlphaSignal, ActionItem, AlphaBrief
from ..core.storage import Storage


class AlphaBriefGenerator:
    """Generates structured alpha briefs from emails and on-chain data"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def generate_brief(self, email_source: Optional[str] = None) -> AlphaBrief:
        """Generate a daily alpha brief"""
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Extract signals from emails
        early_signals = []
        conflicting_views = []
        blind_spots = []
        action_items = []
        sources_used = []
        
        # TODO: Integrate Gmail API when credentials are configured
        if email_source:
            email_signals, email_actions, email_sources = self._parse_emails(email_source)
            early_signals.extend(email_signals.get('early_signal', []))
            conflicting_views.extend(email_signals.get('conflicting_view', []))
            blind_spots.extend(email_signals.get('blind_spot', []))
            action_items.extend(email_actions)
            sources_used.extend(email_sources)
        
        # TODO: Integrate on-chain APIs (ElfAPI, Zapper, Dune)
        # For now, placeholder for structure
        
        # Create brief
        brief = AlphaBrief(
            date=date,
            early_signals=[AlphaSignal(
                signal_type='early_signal',
                content=s.content,
                source=s.source,
                confidence=s.confidence,
                narrative=s.narrative,
                metadata=s.metadata
            ) for s in early_signals],
            conflicting_views=[AlphaSignal(
                signal_type='conflicting_view',
                content=s.content,
                source=s.source,
                confidence=s.confidence,
                narrative=s.narrative,
                metadata=s.metadata
            ) for s in conflicting_views],
            action_items=action_items,
            blind_spots=[AlphaSignal(
                signal_type='blind_spot',
                content=s.content,
                source=s.source,
                confidence=s.confidence,
                narrative=s.narrative,
                metadata=s.metadata
            ) for s in blind_spots],
            sources_used=sources_used
        )
        
        # Save to database
        signal_ids = []
        for signal_list in [early_signals, conflicting_views, blind_spots]:
            for sig in signal_list:
                sig_model = AlphaSignal(
                    signal_type=sig.signal_type if hasattr(sig, 'signal_type') else 'early_signal',
                    content=sig.content if hasattr(sig, 'content') else str(sig),
                    source=sig.source if hasattr(sig, 'source') else 'email',
                    confidence=sig.confidence if hasattr(sig, 'confidence') else None,
                    narrative=sig.narrative if hasattr(sig, 'narrative') else None,
                    metadata=sig.metadata if hasattr(sig, 'metadata') else {}
                )
                signal_ids.append(self.storage.add_alpha_signal(sig_model))
        
        action_item_ids = []
        for action in action_items:
            action_id = self.storage.add_action_item(action)
            action_item_ids.append(action_id)
        
        brief_id = self.storage.add_alpha_brief(brief, signal_ids, action_item_ids)
        brief.id = brief_id
        
        return brief
    
    def _parse_emails(self, email_source: str) -> Tuple[Dict[str, List[AlphaSignal]], List[ActionItem], List[str]]:
        """Parse emails and extract signals and action items
        
        Returns: (signals_dict, action_items, sources_used)
        """
        signals = {
            'early_signal': [],
            'conflicting_view': [],
            'blind_spot': []
        }
        action_items = []
        sources_used = []
        
        # TODO: Implement Gmail API integration
        # For now, this is a placeholder that shows the structure
        
        # When implemented, this would:
        # 1. Connect to Gmail API
        # 2. Search for emails with label (e.g., "📊")
        # 3. Extract content, URLs, tickers, narratives
        # 4. Categorize into early signals, conflicting views, blind spots
        # 5. Extract action items using NLP/pattern matching
        
        return signals, action_items, sources_used
    
    def extract_action_items(self, text: str) -> List[ActionItem]:
        """Extract action items from text using pattern matching"""
        action_items = []
        
        # Pattern: Look for task-like sentences
        # Examples: "Research X protocol", "Map Y on DefiLlama", "Check Z unlock"
        task_patterns = [
            r'(?:Research|Map|Check|Scan|Review|Investigate|Analyze)\s+([^\.]+)',
            r'([A-Z][^\.]*\?)\s+(?:Category|Time|Urgency|Tools)',
        ]
        
        lines = text.split('\n')
        current_task = None
        task_metadata = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_task:
                    action_items.append(self._create_action_item(current_task, task_metadata))
                    current_task = None
                    task_metadata = {}
                continue
            
            # Check for task table format
            if '\t' in line or '|' in line:
                parts = [p.strip() for p in re.split(r'\t|\|', line) if p.strip()]
                if len(parts) >= 2:
                    task = parts[0]
                    # Try to extract metadata
                    if len(parts) > 1:
                        task_metadata['category'] = parts[1] if parts[1] else None
                    if len(parts) > 2:
                        task_metadata['time_estimate'] = parts[2] if parts[2] else None
                    if len(parts) > 3:
                        task_metadata['urgency'] = parts[3].lower() if parts[3] else None
                    if len(parts) > 4:
                        task_metadata['tools_needed'] = parts[4] if parts[4] else None
                    
                    if task and task.lower() != 'task':
                        action_items.append(self._create_action_item(task, task_metadata))
                        task_metadata = {}
            
            # Check for simple task patterns
            for pattern in task_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    task_text = match.group(1).strip()
                    if task_text and len(task_text) > 10:  # Filter out too short matches
                        action_items.append(ActionItem(
                            task=task_text,
                            urgency=self._infer_urgency(line),
                            time_estimate=self._infer_time_estimate(line)
                        ))
        
        return action_items
    
    def _create_action_item(self, task: str, metadata: Dict[str, Any]) -> ActionItem:
        """Create an action item from task and metadata"""
        return ActionItem(
            task=task,
            category=metadata.get('category'),
            time_estimate=metadata.get('time_estimate'),
            urgency=metadata.get('urgency'),
            tools_needed=metadata.get('tools_needed'),
            status='pending'
        )
    
    def _infer_urgency(self, text: str) -> Optional[str]:
        """Infer urgency from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['urgent', 'asap', 'immediately', 'high']):
            return 'high'
        elif any(word in text_lower for word in ['soon', 'medium', 'moderate']):
            return 'medium'
        elif any(word in text_lower for word in ['low', 'later', 'eventually']):
            return 'low'
        return None
    
    def _infer_time_estimate(self, text: str) -> Optional[str]:
        """Infer time estimate from text (e.g., "30m", "1h", "2 hours")"""
        # Look for time patterns
        time_pattern = r'(\d+)\s*(?:m|min|minute|h|hour|hr)'
        match = re.search(time_pattern, text.lower())
        if match:
            return match.group(0)
        return None

