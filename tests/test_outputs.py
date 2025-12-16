"""Test output generators"""

import pytest
from pathlib import Path
import tempfile

from src.core.models import Project
from src.core.storage import Storage
from src.outputs import TwitterThreadGenerator, LinkedInPostGenerator, VideoScriptGenerator


@pytest.fixture
def sample_project(temp_db):
    """Create a sample project with some data"""
    project = Project(name="Test Trading Report", description="A test project")
    project_id = temp_db.add_project(project)
    project.id = project_id
    
    # Add some trades
    trade_data = {
        'entry_date': '2024-01-01',
        'exit_date': '2024-01-02',
        'symbol': 'BTC',
        'entry_price': 45000.0,
        'exit_price': 46000.0,
        'quantity': 1.0,
        'pnl': 1000.0,
        'return_pct': 2.22,
        'strategy': 'momentum'
    }
    temp_db.add_trade(trade_data, project_id=project_id)
    
    return project


class TestOutputGenerators:
    """Test output generation"""
    
    def test_twitter_thread_generator(self, temp_db, sample_project):
        """Test Twitter thread generation"""
        generator = TwitterThreadGenerator(temp_db)
        thread = generator.generate_thread(sample_project)
        
        assert len(thread) > 0
        assert "Test Trading Report" in thread or "trading" in thread.lower()
    
    def test_linkedin_post_generator(self, temp_db, sample_project):
        """Test LinkedIn post generation"""
        generator = LinkedInPostGenerator(temp_db)
        post = generator.generate_post(sample_project)
        
        assert len(post) > 0
        assert "Test Trading Report" in post or "trading" in post.lower()
    
    def test_video_script_generator(self, temp_db, sample_project):
        """Test video script generation"""
        generator = VideoScriptGenerator(temp_db)
        script = generator.generate_script(sample_project)
        
        assert len(script) > 0
        assert "90-Second" in script or "90 second" in script.lower()
        assert "Hook" in script or "hook" in script.lower()
    
    def test_pdf_generator_import(self):
        """Test PDF generator can be imported (may fail if reportlab not available)"""
        try:
            from src.outputs import PDFReportGenerator
            assert PDFReportGenerator is not None
        except ImportError:
            # reportlab might not be available, that's okay for minimum testing
            pytest.skip("reportlab not available")

