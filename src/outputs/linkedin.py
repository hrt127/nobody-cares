"""LinkedIn post generator"""

from typing import Dict, Any, Optional
from datetime import datetime

from ..core.models import Project
from ..core.storage import Storage


class LinkedInPostGenerator:
    """Generate LinkedIn posts from project data"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def generate_post(self, project: Project) -> str:
        """Generate a LinkedIn post for a project"""
        lines = []
        
        # Opening hook
        lines.append(self._generate_opening(project))
        lines.append("")
        
        # Key achievements
        achievements = self._generate_achievements(project)
        if achievements:
            lines.append(achievements)
            lines.append("")
        
        # What I learned
        learnings = self._generate_learnings(project)
        if learnings:
            lines.append(learnings)
            lines.append("")
        
        # Skills/value
        skills = self._generate_skills_value(project)
        if skills:
            lines.append(skills)
            lines.append("")
        
        # CTA
        lines.append(self._generate_cta(project))
        
        return "\n".join(lines)
    
    def _generate_opening(self, project: Project) -> str:
        """Generate professional opening"""
        trades = self.storage.get_trades(project_id=project.id, limit=1)
        
        if trades:
            return f"I recently completed a comprehensive analysis of my trading performance for {project.name}. Here's what I discovered:"
        
        return f"I'm excited to share insights from my recent work on {project.name}."
    
    def _generate_achievements(self, project: Project) -> str:
        """Generate achievements section"""
        trades = self.storage.get_trades(project_id=project.id)
        
        if not trades:
            return ""
        
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
        
        lines = ["Key Achievements:"]
        lines.append(f"• Executed {len(trades)} trades with a {win_rate:.1f}% win rate")
        lines.append(f"• Generated ${total_pnl:,.2f} in realized PnL")
        
        if project.metadata.get('benchmark_return'):
            benchmark = project.metadata['benchmark_return']
            lines.append(f"• Outperformed benchmark by {benchmark:.1f}%")
        
        return "\n".join(lines)
    
    def _generate_learnings(self, project: Project) -> str:
        """Generate learnings section"""
        improvements = self.storage.get_improvements(project_id=project.id)
        
        if improvements:
            lines = ["Key Learnings:"]
            for imp in improvements[:3]:
                if imp.notes:
                    lines.append(f"• {imp.notes[:100]}")
            return "\n".join(lines)
        
        return ""
    
    def _generate_skills_value(self, project: Project) -> str:
        """Generate skills and value section"""
        lines = ["This project demonstrates proficiency in:"]
        
        # Extract from metadata or improvements
        if project.metadata.get('skills'):
            skills = project.metadata['skills']
            if isinstance(skills, list):
                for skill in skills[:5]:
                    lines.append(f"• {skill}")
            else:
                lines.append(f"• {skills}")
        
        if project.metadata.get('monetization_path'):
            lines.append("")
            lines.append(f"Monetization Opportunity: {project.metadata['monetization_path']}")
        
        return "\n".join(lines)
    
    def _generate_cta(self, project: Project) -> str:
        """Generate call-to-action"""
        return "I'm always open to connecting with fellow traders and developers. Feel free to reach out if you'd like to discuss trading strategies, portfolio analysis, or collaboration opportunities.\n\n#Trading #Web3 #Crypto #PortfolioAnalysis"

