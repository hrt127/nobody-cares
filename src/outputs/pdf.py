"""PDF report generator"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from ..core.models import Project
from ..core.storage import Storage


class PDFReportGenerator:
    """Generate PDF reports"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
    
    def generate_pdf(self, project: Project, output_path: Path) -> Path:
        """Generate a PDF report for a project"""
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph(project.name, title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Date
        date_style = styles['Normal']
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", date_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Description
        if project.description:
            story.append(Paragraph("<b>Description:</b>", styles['Heading2']))
            story.append(Paragraph(project.description, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Performance Metrics
        story.append(Paragraph("<b>Performance Metrics</b>", styles['Heading2']))
        metrics = self._get_metrics_table(project)
        if metrics:
            story.append(metrics)
            story.append(Spacer(1, 0.3*inch))
        
        # Top Trades
        story.append(Paragraph("<b>Top Trades</b>", styles['Heading2']))
        top_trades_table = self._get_top_trades_table(project)
        if top_trades_table:
            story.append(top_trades_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Improvements Status
        story.append(Paragraph("<b>Improvements Status</b>", styles['Heading2']))
        improvements_table = self._get_improvements_table(project)
        if improvements_table:
            story.append(improvements_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _get_metrics_table(self, project: Project) -> Optional[Table]:
        """Create metrics table"""
        trades = self.storage.get_trades(project_id=project.id)
        
        if not trades:
            return None
        
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
        avg_pnl = total_pnl / len(trades) if trades else 0
        
        data = [
            ['Metric', 'Value'],
            ['Total Trades', str(len(trades))],
            ['Win Rate', f"{win_rate:.1f}%"],
            ['Total PnL', f"${total_pnl:,.2f}"],
            ['Average PnL', f"${avg_pnl:,.2f}"],
        ]
        
        if project.metadata.get('benchmark_return'):
            data.append(['vs Benchmark', f"{project.metadata['benchmark_return']:.1f}%"])
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    def _get_top_trades_table(self, project: Project, top_n: int = 10) -> Optional[Table]:
        """Create top trades table"""
        trades = self.storage.get_trades(project_id=project.id, limit=top_n)
        
        if not trades:
            return None
        
        # Sort by PnL
        trades_sorted = sorted(trades, key=lambda t: t.get('pnl', 0), reverse=True)
        
        data = [['Symbol', 'Entry Date', 'PnL', 'Return %', 'Strategy']]
        
        for trade in trades_sorted[:top_n]:
            entry_date = trade.get('entry_date')
            if isinstance(entry_date, datetime):
                entry_date = entry_date.strftime('%Y-%m-%d')
            elif entry_date:
                entry_date = str(entry_date)[:10]
            else:
                entry_date = 'N/A'
            
            data.append([
                trade.get('symbol', 'N/A'),
                entry_date,
                f"${trade.get('pnl', 0):,.2f}",
                f"{trade.get('return_pct', 0):.2f}%",
                trade.get('strategy', 'N/A')[:20]
            ])
        
        table = Table(data, colWidths=[1*inch, 1.2*inch, 1*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    def _get_improvements_table(self, project: Project) -> Optional[Table]:
        """Create improvements status table"""
        improvements = self.storage.get_improvements(project_id=project.id)
        
        if not improvements:
            return None
        
        template_names = {
            'interactive_viz': 'Interactive Visualization',
            'benchmark': 'Benchmark Comparison',
            'monetization': 'Skills Monetization',
            'video': 'Video Walkthrough',
            'open_source': 'Open Source Playbook'
        }
        
        data = [['Improvement Type', 'Status', 'Notes']]
        
        for imp in improvements:
            name = template_names.get(imp.improvement_type.value, imp.improvement_type.value)
            status = imp.status.value
            notes = (imp.notes or '')[:50] if imp.notes else ''
            
            data.append([name, status, notes])
        
        table = Table(data, colWidths=[2.5*inch, 1*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

