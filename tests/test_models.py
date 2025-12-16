"""Test data models"""

import pytest
from datetime import datetime

from src.core.models import (
    Entry, EntryType, Project, Improvement, ImprovementType, ImprovementStatus,
    RiskEntry, RewardUpdate
)


class TestEntry:
    """Test Entry model"""
    
    def test_create_entry(self):
        """Test creating a basic entry"""
        entry = Entry(
            entry_type=EntryType.TRADE,
            notes="Test trade",
            tags=["btc", "long"]
        )
        assert entry.entry_type == EntryType.TRADE
        assert entry.notes == "Test trade"
        assert entry.tags == ["btc", "long"]
        assert entry.source == "manual"
        assert isinstance(entry.timestamp, datetime)
    
    def test_entry_with_metadata(self):
        """Test entry with custom metadata"""
        entry = Entry(
            entry_type=EntryType.CODE,
            notes="Test code",
            metadata={"pr_number": 123, "branch": "feature/test"}
        )
        assert entry.metadata["pr_number"] == 123
        assert entry.metadata["branch"] == "feature/test"


class TestRiskEntry:
    """Test RiskEntry model"""
    
    def test_create_risk_entry(self):
        """Test creating a risk entry"""
        risk = RiskEntry(
            risk_type="nft",
            entry_cost=6.3,
            initial_expected_value=15.0,
            current_expected_value=15.0,
            confidence_level=0.65,
            opportunity_cost_perceived=5.0
        )
        assert risk.risk_type == "nft"
        assert risk.entry_cost == 6.3
        assert risk.initial_expected_value == 15.0
        assert risk.current_expected_value == 15.0
        assert risk.confidence_level == 0.65
        assert risk.opportunity_cost_perceived == 5.0
        assert risk.status == "open"
    
    def test_risk_entry_reward_history(self):
        """Test reward history tracking"""
        risk = RiskEntry(
            risk_type="sports_bet",
            entry_cost=100.0,
            initial_expected_value=150.0,
            current_expected_value=150.0,
            reward_history=[
                {
                    "timestamp": datetime.now().isoformat(),
                    "expected_value": 150.0,
                    "reason": "initial"
                }
            ]
        )
        assert len(risk.reward_history) == 1
        assert risk.reward_history[0]["expected_value"] == 150.0


class TestProject:
    """Test Project model"""
    
    def test_create_project(self):
        """Test creating a project"""
        project = Project(
            name="Test Project",
            description="A test project"
        )
        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert isinstance(project.created_at, datetime)


class TestImprovement:
    """Test Improvement model"""
    
    def test_create_improvement(self):
        """Test creating an improvement"""
        improvement = Improvement(
            project_id=1,
            improvement_type=ImprovementType.MONETIZATION,
            status=ImprovementStatus.PENDING,
            notes="Test improvement"
        )
        assert improvement.project_id == 1
        assert improvement.improvement_type == ImprovementType.MONETIZATION
        assert improvement.status == ImprovementStatus.PENDING

