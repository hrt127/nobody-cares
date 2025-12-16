"""Video walkthrough script generator"""

from typing import Dict, Any, List
from datetime import datetime

from ..core.models import Project
from ..core.storage import Storage


class VideoScriptGenerator:
    """Generate 90-second video scripts"""
    
    TOTAL_DURATION = 90  # seconds
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def generate_script(self, project: Project) -> str:
        """Generate a 90-second video script"""
        script = []
        
        # Header
        script.append(f"# {project.name} - 90-Second Video Script")
        script.append(f"Total Duration: {self.TOTAL_DURATION} seconds\n")
        script.append("=" * 80)
        script.append("")
        
        # Part 1: Hook (5 seconds)
        script.append("## Part 1: Hook (0:00 - 0:05)")
        script.append(self._generate_hook(project))
        script.append("")
        
        # Part 2: Problem (10-15 seconds)
        script.append("## Part 2: Problem (0:05 - 0:20)")
        script.append(self._generate_problem(project))
        script.append("")
        
        # Part 3: Solution/Demo (45-60 seconds)
        script.append("## Part 3: Solution & Demo (0:20 - 1:15)")
        script.append(self._generate_solution(project))
        script.append("")
        
        # Part 4: CTA (10 seconds)
        script.append("## Part 4: Call to Action (1:15 - 1:25)")
        script.append(self._generate_cta(project))
        script.append("")
        
        # Talking points
        script.append("---")
        script.append("## Talking Points & Visuals")
        script.append(self._generate_talking_points(project))
        
        return "\n".join(script)
    
    def _generate_hook(self, project: Project) -> str:
        """Generate 5-second hook"""
        trades = self.storage.get_trades(project_id=project.id, limit=1)
        
        if trades and trades[0].get('pnl', 0) > 0:
            pnl = trades[0]['pnl']
            return f"[Show chart/graphic]\n" \
                   f"'I just analyzed {len(self.storage.get_trades(project_id=project.id))} trades and discovered something surprising...'"
        
        return f"[Show project title]\n" \
               f"'What if I told you there's a better way to track and analyze your trading performance?'"
    
    def _generate_problem(self, project: Project) -> str:
        """Generate problem statement (10-15 seconds)"""
        return f"[Show problem visuals]\n" \
               f"'Most traders struggle with:\n" \
               f"- Scattered data across multiple platforms\n" \
               f"- No clear view of what's actually working\n" \
               f"- Missing the patterns that lead to profitable trades\n\n" \
               f"That's exactly the problem I faced.'"
    
    def _generate_solution(self, project: Project) -> str:
        """Generate solution/demo section (45-60 seconds)"""
        trades = self.storage.get_trades(project_id=project.id)
        improvements = self.storage.get_improvements(project_id=project.id)
        
        script = f"[Show dashboard/screenshots]\n"
        script += f"'So I built {project.name}.\n\n"
        
        if trades:
            total_pnl = sum(t.get('pnl', 0) for t in trades)
            win_rate = len([t for t in trades if t.get('pnl', 0) > 0]) / len(trades) * 100 if trades else 0
            script += f"I analyzed {len(trades)} trades, achieved a {win_rate:.1f}% win rate, "
            script += f"and generated ${total_pnl:,.2f} in profits.\n\n"
        
        script += "[Show key features]\n"
        script += "Here's what makes it powerful:\n"
        
        # List top 3 improvements or features
        for imp in improvements[:3]:
            imp_names = {
                'interactive_viz': 'Interactive visualizations',
                'benchmark': 'Benchmark comparisons',
                'monetization': 'Monetization tracking',
                'video': 'Video documentation',
                'open_source': 'Open-source framework'
            }
            name = imp_names.get(imp.improvement_type.value, imp.improvement_type.value)
            script += f"- {name}\n"
        
        script += "\n[Show demo/replay]"
        script += "\nThe system automatically tracks patterns, identifies your edge, "
        script += "and shows exactly where your alpha comes from.'"
        
        return script
    
    def _generate_cta(self, project: Project) -> str:
        """Generate call-to-action (10 seconds)"""
        return f"[Show contact info/links]\n" \
               f"'Want to see the full analysis or build something similar?\n" \
               f"Check the link in the description. Let's connect!'"
    
    def _generate_talking_points(self, project: Project) -> str:
        """Generate talking points and visual notes"""
        points = []
        points.append("Visual Notes:")
        points.append("• Use screen recordings for dashboard demos")
        points.append("• Include charts/graphs showing key metrics")
        points.append("• Show before/after comparison if applicable")
        points.append("")
        points.append("Key Points to Emphasize:")
        
        trades = self.storage.get_trades(project_id=project.id)
        if trades:
            points.append(f"• Analyzed {len(trades)} real trades")
            total_pnl = sum(t.get('pnl', 0) for t in trades)
            points.append(f"• Generated ${total_pnl:,.2f} in realized profits")
        
        improvements = self.storage.get_improvements(project_id=project.id)
        if improvements:
            completed = [i for i in improvements if i.status.value == 'completed']
            points.append(f"• Implemented {len(completed)} key improvements")
        
        return "\n".join(points)

