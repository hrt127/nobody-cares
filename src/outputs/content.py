"""Content generation for distribution - one source, many outputs"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.models import Entry, EntryType
from ..core.storage import Storage
from ..core.currency import format_cost


class ContentGenerator:
    """Generate content from entries for distribution"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def generate_twitter(self, entry: Entry, brevity: str = 'medium') -> str:
        """Generate Twitter thread from risk entry"""
        try:
            risk_data = entry.metadata or {}
            cost = risk_data.get('entry_cost', 0)
            currency = risk_data.get('currency', 'USD')
        except Exception:
            # Fallback if metadata is malformed
            risk_data = {}
            cost = 0
            currency = 'USD'
        
        tweets = []
        
        # Tweet 1: Hook
        if brevity == 'high':
            hook = f"📊 Quick insight from a recent bet:\n\n"
        else:
            hook = f"📊 Sharing a recent bet and what I learned:\n\n"
        tweets.append(hook)
        
        # Tweet 2: The bet
        bet_tweet = f"💰 The Bet:\n"
        bet_tweet += f"• Amount: {format_cost(cost, currency)}\n"
        
        if risk_data.get('odds_or_price'):
            bet_tweet += f"• Odds: {risk_data['odds_or_price']}\n"
        
        if risk_data.get('my_probability'):
            bet_tweet += f"• My probability: {risk_data['my_probability']*100:.0f}%\n"
        
        if risk_data.get('edge_pct'):
            bet_tweet += f"• Edge: {risk_data['edge_pct']:+.1f}%"
        
        tweets.append(bet_tweet)
        
        # Tweet 3: What I saw (if available)
        if risk_data.get('what_i_see') and brevity != 'high':
            insight_tweet = f"🔍 What I saw:\n{risk_data['what_i_see']}"
            tweets.append(insight_tweet)
        
        # Tweet 4: Outcome/Lesson
        outcome_tweet = f"📈 Outcome: "
        try:
            if risk_data.get('realized_value') is not None:
                realized = risk_data['realized_value']
                pnl = realized - cost
                outcome_tweet += f"{format_cost(realized, currency)} "
                if pnl > 0:
                    outcome_tweet += f"(+{format_cost(pnl, currency)})"
                else:
                    outcome_tweet += f"({format_cost(pnl, currency)})"
            else:
                outcome_tweet += "Pending"
        except (TypeError, ValueError):
            outcome_tweet += "Pending"
        
        tweets.append(outcome_tweet)
        
        # Tweet 5: Lesson (if available)
        lessons = self.extract_lessons(entry)
        if lessons and brevity != 'high':
            lesson_tweet = f"💡 Lesson:\n{lessons[0]}"  # First lesson
            tweets.append(lesson_tweet)
        
        # Join with thread separator
        return "\n\n---\n\n".join(tweets)
    
    def generate_linkedin(self, entry: Entry) -> str:
        """Generate LinkedIn post (more professional)"""
        try:
            risk_data = entry.metadata or {}
            cost = risk_data.get('entry_cost', 0)
            currency = risk_data.get('currency', 'USD')
        except Exception:
            risk_data = {}
            cost = 0
            currency = 'USD'
        
        post = f"📊 Recent Bet Analysis\n\n"
        
        post += f"I recently placed a bet that taught me something valuable about risk management and edge recognition.\n\n"
        
        post += f"💰 The Setup:\n"
        post += f"• Amount: {format_cost(cost, currency)}\n"
        if risk_data.get('odds_or_price'):
            post += f"• Odds: {risk_data['odds_or_price']}\n"
        if risk_data.get('my_probability'):
            post += f"• My assessment: {risk_data['my_probability']*100:.0f}% probability\n"
        if risk_data.get('edge_pct'):
            post += f"• Calculated edge: {risk_data['edge_pct']:+.1f}%\n"
        
        if risk_data.get('what_i_see'):
            post += f"\n🔍 Key Insight:\n{risk_data['what_i_see']}\n"
        
        if risk_data.get('why_i_trust_this'):
            post += f"\nWhy I trusted this: {risk_data['why_i_trust_this']}\n"
        
        post += f"\n📈 Outcome: "
        try:
            if risk_data.get('realized_value') is not None:
                realized = risk_data['realized_value']
                pnl = realized - cost
                post += f"{format_cost(realized, currency)} "
                if pnl != 0:
                    post += f"({format_cost(pnl, currency)})"
            else:
                post += "Pending"
        except (TypeError, ValueError):
            post += "Pending"
        
        lessons = self.extract_lessons(entry)
        if lessons:
            post += f"\n\n💡 Key Takeaway:\n{lessons[0]}\n"
        
        post += f"\n#RiskManagement #DecisionMaking #Learning"
        
        return post
    
    def generate_blog(self, entry: Entry) -> str:
        """Generate blog post (longer form)"""
        try:
            risk_data = entry.metadata or {}
        except Exception:
            risk_data = {}
        
        try:
            blog = f"# Bet Analysis: {entry.notes}\n\n"
            blog += f"*Date: {entry.timestamp.strftime('%Y-%m-%d')}*\n\n"
        except Exception:
            blog = f"# Bet Analysis\n\n"
            blog += f"*Date: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        
        blog += f"## The Setup\n\n"
        blog += f"**Amount:** {format_cost(risk_data.get('entry_cost', 0), risk_data.get('currency', 'USD'))}\n\n"
        
        if risk_data.get('odds_or_price'):
            blog += f"**Odds:** {risk_data['odds_or_price']}\n\n"
        
        if risk_data.get('my_probability'):
            blog += f"**My Probability Assessment:** {risk_data['my_probability']*100:.0f}%\n\n"
        
        if risk_data.get('market_probability'):
            blog += f"**Market Implied Probability:** {risk_data['market_probability']*100:.0f}%\n\n"
        
        if risk_data.get('edge_pct'):
            blog += f"**Calculated Edge:** {risk_data['edge_pct']:+.1f}%\n\n"
        
        if risk_data.get('what_i_see'):
            blog += f"## What I Saw\n\n{risk_data['what_i_see']}\n\n"
        
        if risk_data.get('why_i_trust_this'):
            blog += f"## Why I Trusted This\n\n{risk_data['why_i_trust_this']}\n\n"
        
        if risk_data.get('red_flags'):
            blog += f"## Red Flags\n\n{risk_data['red_flags']}\n\n"
        
        blog += f"## Outcome\n\n"
        try:
            if risk_data.get('realized_value') is not None:
                realized = risk_data['realized_value']
                cost = risk_data.get('entry_cost', 0)
                pnl = realized - cost
                currency = risk_data.get('currency', 'USD')
                blog += f"**Realized Value:** {format_cost(realized, currency)}\n\n"
                blog += f"**PnL:** {format_cost(pnl, currency)}\n\n"
            else:
                blog += f"Pending\n\n"
        except (TypeError, ValueError):
            blog += f"Pending\n\n"
        
        lessons = self.extract_lessons(entry)
        if lessons:
            blog += f"## Lessons Learned\n\n"
            for i, lesson in enumerate(lessons, 1):
                blog += f"{i}. {lesson}\n\n"
        
        return blog
    
    def extract_lessons(self, entry: Entry) -> List[str]:
        """Extract hard-won lessons from outcome"""
        try:
            risk_data = entry.metadata or {}
        except Exception:
            risk_data = {}
        
        lessons = []
        
        # Cash-out lesson
        if risk_data.get('missed_cash_out_value'):
            lessons.append(
                f"Couldn't cash out when optimal - lost {format_cost(risk_data['missed_cash_out_value'], risk_data.get('currency', 'USD'))} in value. "
                f"Next time: Check cash-out availability before betting."
            )
        
        if risk_data.get('why_stuck'):
            lessons.append(f"Got stuck: {risk_data['why_stuck']}. Platform limitation cost me value.")
        
        # Edge capture lesson
        if risk_data.get('edge_pct') and risk_data.get('realized_value'):
            edge = risk_data['edge_pct']
            if edge > 0:
                lessons.append(f"Had {edge:+.1f}% edge - need to ensure I can capture it (cash-out availability matters).")
        
        # Intuition lesson
        if risk_data.get('gut_feeling') and risk_data.get('realized_value'):
            gut = risk_data['gut_feeling']
            realized = risk_data['realized_value']
            cost = risk_data.get('entry_cost', 0)
            if (realized > cost and 'strong' in gut.lower()) or (realized < cost and 'weak' in gut.lower()):
                lessons.append(f"Gut feeling ({gut}) was accurate - trust this pattern in future.")
        
        # Pattern match lesson
        if risk_data.get('pattern_match'):
            lessons.append(f"Pattern match noted: {risk_data['pattern_match']}. Track if this pattern holds.")
        
        return lessons
    
    def filter_content(self, content: str, include: Optional[List[str]] = None, 
                      exclude: Optional[List[str]] = None) -> str:
        """Filter what to share"""
        # Simple keyword filtering - can be enhanced
        lines = content.split('\n')
        filtered = []
        
        for line in lines:
            # Check exclude
            if exclude:
                if any(keyword.lower() in line.lower() for keyword in exclude):
                    continue
            
            # Check include
            if include:
                if any(keyword.lower() in line.lower() for keyword in include):
                    filtered.append(line)
            else:
                filtered.append(line)
        
        return '\n'.join(filtered)
