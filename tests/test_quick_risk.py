"""Test quick risk entry command"""

import pytest
from click.testing import CliRunner
from pathlib import Path

from src.cli.main import main


@pytest.fixture
def cli_runner():
    """Create a CLI test runner"""
    return CliRunner()


@pytest.fixture
def isolated_env(cli_runner):
    """Create isolated environment for CLI tests"""
    with cli_runner.isolated_filesystem():
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        yield


class TestQuickRisk:
    """Test quick risk entry command"""
    
    def test_quick_risk_basic(self, cli_runner, isolated_env):
        """Test basic quick risk entry"""
        result = cli_runner.invoke(main, ['q', '100', 'Test bet'])
        assert result.exit_code == 0
        assert "Quick entry" in result.output
        assert "100" in result.output
    
    def test_quick_risk_with_currency(self, cli_runner, isolated_env):
        """Test quick risk with currency"""
        result = cli_runner.invoke(main, ['q', '0.1', '--currency', 'ETH', 'ETH bet'])
        assert result.exit_code == 0
        assert "ETH" in result.output
    
    def test_quick_risk_negative_cost(self, cli_runner, isolated_env):
        """Test quick risk rejects negative cost"""
        result = cli_runner.invoke(main, ['q', '-10', 'Test'])
        assert result.exit_code != 0
        assert "must be greater than 0" in result.output or "Error" in result.output

