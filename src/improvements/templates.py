"""Improvement template definitions with guidance and checklists"""

from typing import Dict, List
from ..core.models import ImprovementType


class ImprovementTemplate:
    """Template definition for an improvement type"""
    
    def __init__(
        self,
        improvement_type: ImprovementType,
        name: str,
        description: str,
        checklist: List[str],
        examples: List[str],
        tools_needed: List[str]
    ):
        self.improvement_type = improvement_type
        self.name = name
        self.description = description
        self.checklist = checklist
        self.examples = examples
        self.tools_needed = tools_needed


# Template definitions
IMPROVEMENT_TEMPLATES: Dict[ImprovementType, ImprovementTemplate] = {
    ImprovementType.INTERACTIVE_VIZ: ImprovementTemplate(
        improvement_type=ImprovementType.INTERACTIVE_VIZ,
        name="Interactive Visualization",
        description="Create interactive trade replay with annotations and voiceover",
        checklist=[
            "Set up charting library (Chart.js, D3, or Plotly)",
            "Implement trade replay functionality",
            "Add annotation system (mark entry/exit points)",
            "Create voiceover script or text-to-speech",
            "Add controls (play/pause, speed adjustment)",
            "Export/share functionality",
            "Mobile-responsive design"
        ],
        examples=[
            "Interactive candlestick chart with trade markers",
            "Timeline-based replay with annotations",
            "3D visualization of trading activity"
        ],
        tools_needed=["Charting library", "Web framework", "Audio recording/processing"]
    ),
    
    ImprovementType.BENCHMARK: ImprovementTemplate(
        improvement_type=ImprovementType.BENCHMARK,
        name="Benchmark Comparison",
        description="Compare your returns against market benchmarks and peers",
        checklist=[
            "Identify relevant benchmarks (BTC, ETH, indices, peer group)",
            "Collect historical benchmark data",
            "Calculate performance metrics (Sharpe, Sortino, max drawdown)",
            "Create comparison visualizations",
            "Add time-period filters",
            "Include risk-adjusted metrics",
            "Document methodology"
        ],
        examples=[
            "Returns vs BTC/ETH over multiple timeframes",
            "Sharpe ratio comparison chart",
            "Drawdown comparison visualization"
        ],
        tools_needed=["Data source APIs", "Charting library", "Statistical libraries"]
    ),
    
    ImprovementType.MONETIZATION: ImprovementTemplate(
        improvement_type=ImprovementType.MONETIZATION,
        name="Skills Monetization",
        description="Map skills to monetization paths and calculate market value",
        checklist=[
            "List all skills demonstrated in the project",
            "Research market rates for each skill",
            "Identify monetization paths (consulting, SaaS, content, courses)",
            "Calculate potential revenue streams",
            "Create pricing structure",
            "Develop marketing strategy",
            "Set up payment/execution infrastructure"
        ],
        examples=[
            "$49/mo SaaS subscription",
            "Consulting at $150/hr",
            "Video course at $99 one-time",
            "Newsletter subscription at $10/mo"
        ],
        tools_needed=["Market research", "Payment processor", "Pricing calculator"]
    ),
    
    ImprovementType.VIDEO: ImprovementTemplate(
        improvement_type=ImprovementType.VIDEO,
        name="Video Walkthrough",
        description="90-second video script with structured format",
        checklist=[
            "Write hook (first 5 seconds)",
            "Define problem (10-15 seconds)",
            "Present solution/demo (45-60 seconds)",
            "Call-to-action (final 10 seconds)",
            "Add timestamps and talking points",
            "Prepare visuals/screen recordings",
            "Record and edit video",
            "Add captions/subtitles"
        ],
        examples=[
            "4-part structure: Hook → Problem → Solution → CTA",
            "Screen recording with voiceover",
            "Animated explainer video"
        ],
        tools_needed=["Screen recording software", "Video editing tool", "Audio equipment"]
    ),
    
    ImprovementType.OPEN_SOURCE: ImprovementTemplate(
        improvement_type=ImprovementType.OPEN_SOURCE,
        name="Open Source Playbook",
        description="Framework structure for others to fork and use",
        checklist=[
            "Document project structure",
            "Create comprehensive README",
            "Add setup/installation instructions",
            "Write code comments and docstrings",
            "Create example usage scenarios",
            "Set up GitHub repository",
            "Add license file",
            "Create contribution guidelines",
            "Add tests and CI/CD"
        ],
        examples=[
            "GitHub repo with clear structure",
            "Template repository",
            "Step-by-step guide for implementation"
        ],
        tools_needed=["GitHub", "Documentation tool (MkDocs, Sphinx)", "CI/CD platform"]
    )
}


def get_template(improvement_type: ImprovementType) -> ImprovementTemplate:
    """Get template for an improvement type"""
    return IMPROVEMENT_TEMPLATES.get(improvement_type)


def get_all_templates() -> Dict[ImprovementType, ImprovementTemplate]:
    """Get all improvement templates"""
    return IMPROVEMENT_TEMPLATES.copy()

