"""Format alpha briefs as markdown"""

from datetime import datetime
from typing import List

from ..core.models import AlphaBrief, AlphaSignal, ActionItem


class BriefFormatter:
    """Formats alpha briefs as markdown"""
    
    @staticmethod
    def format_brief(brief: AlphaBrief) -> str:
        """Format a brief as markdown"""
        lines = []
        
        # Header
        date_str = brief.date.strftime("%Y-%m-%d")
        lines.append(f"# DAILY WEB3 ALPHA BRIEF - {date_str}\n")
        lines.append("---\n\n")
        
        # Early Signals
        if brief.early_signals:
            lines.append("## 1. Early Signals\n\n")
            lines.append("*New protocols/narratives before they trend, on-chain activity, sentiment shifts*\n\n")
            
            for i, signal in enumerate(brief.early_signals, 1):
                lines.append(f"{i}. {signal.content}")
                if signal.source:
                    lines.append(f"   *Source: {signal.source}*")
                if signal.confidence:
                    lines.append(f"   *Confidence: {signal.confidence}*")
                if signal.narrative:
                    lines.append(f"   *Narrative: {signal.narrative}*")
                lines.append("")
        else:
            lines.append("## 1. Early Signals\n\n")
            lines.append("*No early signals identified today.*\n\n")
        
        # Conflicting Views
        if brief.conflicting_views:
            lines.append("## 2. Conflicting Views\n\n")
            lines.append("*Where sources disagree, contrarian cases, red flags being ignored*\n\n")
            
            for i, signal in enumerate(brief.conflicting_views, 1):
                lines.append(f"{i}. {signal.content}")
                if signal.source:
                    lines.append(f"   *Source: {signal.source}*")
                lines.append("")
        else:
            lines.append("## 2. Conflicting Views\n\n")
            lines.append("*No conflicting views identified today.*\n\n")
        
        # Action Items
        if brief.action_items:
            lines.append("## 3. Action Items\n\n")
            lines.append("| Task | Category | Time | Urgency | Tools Needed |\n")
            lines.append("|------|----------|------|---------|-------------|\n")
            
            for action in brief.action_items:
                task = action.task.replace('|', '\\|')  # Escape pipes
                category = action.category or ""
                time_est = action.time_estimate or ""
                urgency = action.urgency or ""
                tools = action.tools_needed or ""
                
                lines.append(f"| {task} | {category} | {time_est} | {urgency} | {tools} |\n")
            
            lines.append("")
        else:
            lines.append("## 3. Action Items\n\n")
            lines.append("*No action items extracted.*\n\n")
        
        # Blind Spots
        if brief.blind_spots:
            lines.append("## 4. Blind Spots Today\n\n")
            lines.append("*What sources are NOT covering, where to look manually*\n\n")
            
            for i, signal in enumerate(brief.blind_spots, 1):
                lines.append(f"- {signal.content}")
                if signal.source:
                    lines.append(f"  *Source: {signal.source}*")
                lines.append("")
        else:
            lines.append("## 4. Blind Spots Today\n\n")
            lines.append("*No blind spots identified.*\n\n")
        
        # Sources
        if brief.sources_used:
            lines.append("---\n\n")
            lines.append(f"**Sources used:** {', '.join(brief.sources_used)}\n")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_action_items_table(action_items: List[ActionItem]) -> str:
        """Format action items as a table"""
        if not action_items:
            return "No action items.\n"
        
        lines = []
        lines.append("| Task | Category | Time | Urgency | Status | Tools Needed |\n")
        lines.append("|------|----------|------|---------|--------|-------------|\n")
        
        for action in action_items:
            task = action.task.replace('|', '\\|')
            category = action.category or ""
            time_est = action.time_estimate or ""
            urgency = action.urgency or ""
            status = action.status or "pending"
            tools = action.tools_needed or ""
            
            lines.append(f"| {task} | {category} | {time_est} | {urgency} | {status} | {tools} |\n")
        
        return "".join(lines)

