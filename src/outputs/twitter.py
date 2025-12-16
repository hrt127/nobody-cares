"""Twitter thread generator"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core.models import Project
from ..core.storage import Storage


class TwitterThreadGenerator:
    """Generate Twitter threads from project data"""
    
    MAX_TWEET_LENGTH = 280
    THREAD_SEPARATOR = "\n\n---\n\n"
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def generate_thread(self, project: Project, include_benchmarks: bool = True,
                       include_monetization: bool = True) -> str:
        """Generate a Twitter thread for a project"""
        tweets = []
        
        # Tweet 1: Hook
        hook = self._generate_hook(project)
        tweets.append(hook)
        
        # Tweet 2: Key metrics/performance
        metrics = self._get_metrics_tweet(project, include_benchmarks)
        if metrics:
            tweets.append(metrics)
        
        # Tweet 3: Edge demonstration
        edge = self._generate_edge_tweet(project)
        if edge:
            tweets.append(edge)
        
        # Tweet 4: Top trades/achievements
        achievements = self._generate_achievements_tweet(project)
        if achievements:
            tweets.append(achievements)
        
        # Tweet 5: Monetization (if enabled)
        if include_monetization:
            monetization = self._generate_monetization_tweet(project)
            if monetization:
                tweets.append(monetization)
        
        # Tweet 6: CTA
        cta = self._generate_cta(project)
        tweets.append(cta)
        
        return self.THREAD_SEPARATOR.join(tweets)
    
    def _generate_hook(self, project: Project) -> str:
        """Generate opening hook tweet"""
        # Try to extract interesting metric or achievement
        trades = self.storage.get_trades(project_id=project.id, limit=1)
        
        if trades and 'pnl' in trades[0]:
            pnl = trades[0].get('pnl', 0)
            if pnl > 0:
                return f"📊 Just completed analysis of my trading performance for {project.name}\n\n" \
                       f"Here's what I learned and how I beat the market 🧵👇"
        
        return f"📊 Sharing my {project.name} analysis\n\n" \
               f"Key insights, performance metrics, and what I learned 🧵👇"
    
    def _get_metrics_tweet(self, project: Project, include_benchmarks: bool) -> str:
        """Generate metrics tweet"""
        trades = self.storage.get_trades(project_id=project.id)
        
        if not trades:
            return ""
        
        # Calculate metrics
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
        
        tweet = f"📈 Performance Metrics:\n\n"
        tweet += f"• Total trades: {len(trades)}\n"
        tweet += f"• Win rate: {win_rate:.1f}%\n"
        tweet += f"• Total PnL: ${total_pnl:,.2f}"
        
        if include_benchmarks and project.metadata.get('benchmark_return'):
            benchmark = project.metadata['benchmark_return']
            tweet += f"\n• vs Benchmark: {benchmark:.1f}%"
        
        return tweet
    
    def _generate_edge_tweet(self, project: Project) -> str:
        """Generate tweet showing edge/differentiation"""
        improvements = self.storage.get_improvements(project_id=project.id)
        completed = [i for i in improvements if i.status.value == 'completed']
        
        if completed:
            improvement_names = {
                'interactive_viz': 'Interactive visualizations',
                'benchmark': 'Benchmark comparisons',
                'monetization': 'Monetization paths',
                'video': 'Video walkthroughs',
                'open_source': 'Open-source playbooks'
            }
            
            edges = [improvement_names.get(i.improvement_type.value, i.improvement_type.value) 
                    for i in completed[:2]]
            
            if edges:
                return f"🎯 My Edge:\n\n" + "\n".join(f"• {edge}" for edge in edges)
        
        return ""
    
    def _generate_achievements_tweet(self, project: Project) -> str:
        """Generate achievements/top trades tweet"""
        trades = self.storage.get_trades(project_id=project.id, limit=5)
        
        if not trades:
            return ""
        
        # Get top trade
        top_trade = max(trades, key=lambda t: t.get('pnl', 0), default=None)
        
        if top_trade and top_trade.get('pnl', 0) > 0:
            symbol = top_trade.get('symbol', 'N/A')
            pnl = top_trade.get('pnl', 0)
            return_pct = top_trade.get('return_pct', 0)
            
            tweet = f"🏆 Best Trade:\n\n"
            tweet += f"{symbol}: +{return_pct:.2f}% (${pnl:,.2f})\n\n"
            
            if top_trade.get('strategy'):
                tweet += f"Strategy: {top_trade['strategy']}"
            
            return tweet
        
        return ""
    
    def _generate_monetization_tweet(self, project: Project) -> str:
        """Generate monetization path tweet"""
        monetization_improvements = [
            i for i in self.storage.get_improvements(project_id=project.id)
            if i.improvement_type.value == 'monetization'
        ]
        
        if monetization_improvements and project.metadata.get('monetization_path'):
            path = project.metadata['monetization_path']
            value = project.metadata.get('monetization_value', '')
            
            tweet = f"💰 Monetization Path:\n\n"
            tweet += f"{path}"
            if value:
                tweet += f"\n\nTarget: {value}"
            
            return tweet
        
        return ""
    
    def _generate_cta(self, project: Project) -> str:
        """Generate call-to-action tweet"""
        return f"📚 Full analysis available in my portfolio\n\n" \
               f"Link in bio 👆\n\n" \
               f"#TradingAnalysis #Crypto #Web3"

