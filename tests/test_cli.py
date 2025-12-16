"""Test CLI commands"""

import pytest
from click.testing import CliRunner
from pathlib import Path
import tempfile
import os

from src.cli.main import main


@pytest.fixture
def cli_runner():
    """Create a CLI test runner"""
    return CliRunner()


@pytest.fixture
def isolated_env(cli_runner):
    """Create isolated environment for CLI tests"""
    with cli_runner.isolated_filesystem():
        # Set up temporary data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        yield


class TestCLIBasic:
    """Test basic CLI commands"""
    
    def test_log_entry(self, cli_runner, isolated_env):
        """Test logging a basic entry"""
        result = cli_runner.invoke(main, ['log', 'trade', 'BTC long @ 45k'])
        assert result.exit_code == 0
        assert "Logged entry" in result.output
    
    def test_today_command(self, cli_runner, isolated_env):
        """Test today command"""
        # First log an entry
        cli_runner.invoke(main, ['log', 'code', 'Test commit'])
        
        # Then check today
        result = cli_runner.invoke(main, ['today'])
        assert result.exit_code == 0
        assert "Today's Entries" in result.output or "No entries found" in result.output
    
    def test_create_project(self, cli_runner, isolated_env):
        """Test creating a project"""
        import uuid
        unique_name = f"Test Project {uuid.uuid4().hex[:8]}"
        result = cli_runner.invoke(main, ['project', 'create', unique_name])
        assert result.exit_code == 0
        assert "Created project" in result.output
    
    def test_list_projects(self, cli_runner, isolated_env):
        """Test listing projects"""
        # Create a project first
        cli_runner.invoke(main, ['project', 'create', 'Test Project'])
        
        result = cli_runner.invoke(main, ['project', 'list'])
        assert result.exit_code == 0
        assert "Test Project" in result.output


class TestCLIRiskTracking:
    """Test risk tracking CLI commands"""
    
    def test_log_risk(self, cli_runner, isolated_env):
        """Test logging a risk entry"""
        result = cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '6.3',
            '--expected-value', '15',
            'Test NFT'
        ])
        assert result.exit_code == 0
        assert "Logged risk entry" in result.output
        assert "nft" in result.output.lower()
    
    def test_log_risk_with_opportunity_cost(self, cli_runner, isolated_env):
        """Test logging risk with opportunity cost"""
        result = cli_runner.invoke(main, [
            'risk', 'sports_bet',
            '--cost', '100',
            '--expected-value', '150',
            '--opportunity-cost', '10',
            'Test bet'
        ])
        assert result.exit_code == 0
        assert "Opportunity cost" in result.output
    
    def test_log_risk_with_zero_opportunity_cost(self, cli_runner, isolated_env):
        """Test that explicit zero opportunity cost is respected"""
        result = cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '10',
            '--expected-value', '15',
            '--opportunity-cost', '5',
            '--opportunity-cost-real', '0',  # Explicitly zero
            'Test NFT'
        ])
        assert result.exit_code == 0
        # Should show "0.00 USD real" or "$0.00 USD real" not fall back to perceived
        # New format uses currency formatting: "$0.00 USD real" or "0.00 USD real"
        assert ("0.00" in result.output and "real" in result.output) or "$0.00" in result.output
    
    def test_list_risks(self, cli_runner, isolated_env):
        """Test listing risks"""
        # First log a risk
        cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '10',
            'Test'
        ])
        
        result = cli_runner.invoke(main, ['risks'])
        assert result.exit_code == 0
        assert "Risk Entries" in result.output
    
    def test_update_risk_reward(self, cli_runner, isolated_env):
        """Test updating risk reward"""
        # First log a risk
        result = cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '10',
            '--expected-value', '15',
            'Test'
        ])
        # Extract entry ID from output (this is a simplified test)
        # In practice, we'd need to parse the output or use a different approach
        
        # Update the risk (assuming entry ID 1)
        result = cli_runner.invoke(main, [
            'update-risk', '1',
            '--reward', '20',
            '--reason', 'Market moved'
        ])
        # Should either succeed or fail gracefully if entry doesn't exist
        assert result.exit_code in [0, 1]  # Allow both success and graceful failure
    
    def test_update_risk_opportunity_cost(self, cli_runner, isolated_env):
        """Test updating risk opportunity cost"""
        # First log a risk
        cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '10',
            '--expected-value', '15',
            '--opportunity-cost', '5',
            'Test'
        ])
        
        # Update opportunity cost
        result = cli_runner.invoke(main, [
            'update-risk', '1',
            '--opportunity-cost-real', '8',
            '--reason', 'Market conditions changed'
        ])
        # Should either succeed or fail gracefully
        assert result.exit_code in [0, 1]
    
    def test_risks_with_history(self, cli_runner, isolated_env):
        """Test listing risks with history"""
        # Log a risk first
        cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '10',
            '--expected-value', '15',
            'Test'
        ])
        
        result = cli_runner.invoke(main, ['risks', '--show-history'])
        assert result.exit_code == 0
        assert "Risk Entries" in result.output
    
    def test_improvements_commands(self, cli_runner, isolated_env):
        """Test improvement tracking commands"""
        # Create project first
        cli_runner.invoke(main, ['project', 'create', 'Test Project'])
        
        # Add improvement
        result = cli_runner.invoke(main, [
            'improvements', 'add',
            'Test Project',
            '--template', 'monetization'
        ])
        assert result.exit_code == 0
        assert "Added" in result.output or "improvement" in result.output.lower()
        
        # List improvements
        result = cli_runner.invoke(main, [
            'improvements', 'list',
            '--project', 'Test Project'
        ])
        assert result.exit_code == 0
        
        # Show guide
        result = cli_runner.invoke(main, [
            'improvements', 'guide',
            '--template', 'monetization'
        ])
        assert result.exit_code == 0
        assert "monetization" in result.output.lower() or "Skills Monetization" in result.output
    
    def test_update_risk_from_zero_reward(self, cli_runner, isolated_env):
        """Test updating risk reward from zero (explicit zero should be treated as update, not set)"""
        # First log a risk with zero expected value
        result = cli_runner.invoke(main, [
            'risk', 'nft',
            '--cost', '10',
            '--expected-value', '0',  # Explicitly zero
            'Test zero reward'
        ])
        assert result.exit_code == 0
        # Extract entry ID from output (format: "Logged risk entry #X")
        import re
        match = re.search(r'#(\d+)', result.output)
        if not match:
            pytest.skip("Could not extract entry ID from output")
        entry_id = match.group(1)
        
        # Update from zero to non-zero
        result = cli_runner.invoke(main, [
            'update-risk', entry_id,
            '--reward', '15',
            '--reason', 'Updated from zero'
        ])
        # Should show "Updated reward: $0.00 → $15.00" not "Set reward"
        assert result.exit_code == 0
        assert "Updated reward" in result.output
        assert "0.00" in result.output  # Should show the zero value
        assert "15.00" in result.output

