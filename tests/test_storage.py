"""Test storage operations"""

import pytest
from datetime import datetime, timedelta

from src.core.models import Entry, EntryType, Project, Improvement, ImprovementType, ImprovementStatus


class TestStorage:
    """Test Storage operations"""
    
    def test_add_and_get_entry(self, temp_db):
        """Test adding and retrieving an entry"""
        entry = Entry(
            entry_type=EntryType.TRADE,
            notes="BTC long @ 45k",
            tags=["btc", "long"]
        )
        entry_id = temp_db.add_entry(entry)
        assert entry_id > 0
        
        entries = temp_db.get_entries(entry_type=EntryType.TRADE)
        assert len(entries) == 1
        assert entries[0].notes == "BTC long @ 45k"
        assert entries[0].id == entry_id
    
    def test_get_entries_by_date_range(self, temp_db):
        """Test filtering entries by date range"""
        # Add entries on different dates
        entry1 = Entry(
            entry_type=EntryType.CODE,
            notes="Old entry",
            timestamp=datetime.now() - timedelta(days=2)
        )
        entry2 = Entry(
            entry_type=EntryType.CODE,
            notes="New entry",
            timestamp=datetime.now()
        )
        temp_db.add_entry(entry1)
        temp_db.add_entry(entry2)
        
        # Get only today's entries
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        entries = temp_db.get_entries(
            entry_type=EntryType.CODE,
            start_date=today_start
        )
        assert len(entries) == 1
        assert entries[0].notes == "New entry"
    
    def test_add_and_get_project(self, temp_db):
        """Test adding and retrieving a project"""
        project = Project(name="Test Project", description="A test")
        project_id = temp_db.add_project(project)
        assert project_id > 0
        
        retrieved = temp_db.get_project(project_id)
        assert retrieved is not None
        assert retrieved.name == "Test Project"
        assert retrieved.id == project_id
    
    def test_get_project_by_name(self, temp_db):
        """Test retrieving project by name"""
        project = Project(name="Unique Project")
        project_id = temp_db.add_project(project)
        
        retrieved = temp_db.get_project_by_name("Unique Project")
        assert retrieved is not None
        assert retrieved.id == project_id
    
    def test_add_and_get_improvement(self, temp_db):
        """Test adding and retrieving improvements"""
        # First create a project
        project = Project(name="Test Project")
        project_id = temp_db.add_project(project)
        
        improvement = Improvement(
            project_id=project_id,
            improvement_type=ImprovementType.MONETIZATION,
            status=ImprovementStatus.PENDING,
            notes="Test improvement"
        )
        imp_id = temp_db.add_improvement(improvement)
        assert imp_id > 0
        
        improvements = temp_db.get_improvements(project_id=project_id)
        assert len(improvements) == 1
        assert improvements[0].notes == "Test improvement"
    
    def test_update_improvement(self, temp_db):
        """Test updating an improvement"""
        project = Project(name="Test Project")
        project_id = temp_db.add_project(project)
        
        improvement = Improvement(
            project_id=project_id,
            improvement_type=ImprovementType.MONETIZATION
        )
        imp_id = temp_db.add_improvement(improvement)
        
        # Update status
        updated = temp_db.update_improvement(
            imp_id,
            status=ImprovementStatus.IN_PROGRESS,
            notes="Updated note"
        )
        assert updated is True
        
        improvements = temp_db.get_improvements(project_id=project_id)
        assert improvements[0].status == ImprovementStatus.IN_PROGRESS
        assert improvements[0].notes == "Updated note"
    
    def test_update_entry_metadata(self, temp_db):
        """Test updating entry metadata"""
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Initial risk",
            metadata={"initial": "value"}
        )
        entry_id = temp_db.add_entry(entry)
        
        # Update metadata
        new_metadata = {
            "initial": "value",
            "updated": "new_value",
            "risk_data": {"type": "nft", "cost": 10.0}
        }
        updated = temp_db.update_entry_metadata(entry_id, new_metadata)
        assert updated is True
        
        entries = temp_db.get_entries()
        updated_entry = next(e for e in entries if e.id == entry_id)
        assert updated_entry.metadata["updated"] == "new_value"
        assert updated_entry.metadata["risk_data"]["cost"] == 10.0
    
    def test_add_and_get_trades(self, temp_db):
        """Test adding and retrieving trades"""
        trade_data = {
            'entry_date': datetime.now(),
            'exit_date': datetime.now(),
            'symbol': 'BTC',
            'entry_price': 45000.0,
            'exit_price': 46000.0,
            'quantity': 1.0,
            'pnl': 1000.0,
            'return_pct': 2.22,
            'strategy': 'momentum'
        }
        
        trade_id = temp_db.add_trade(trade_data)
        assert trade_id > 0
        
        trades = temp_db.get_trades()
        assert len(trades) == 1
        assert trades[0]['symbol'] == 'BTC'
        assert trades[0]['pnl'] == 1000.0
    
    def test_add_trades_batch(self, temp_db):
        """Test adding multiple trades in batch"""
        trades = [
            {
                'entry_date': datetime.now(),
                'symbol': 'BTC',
                'entry_price': 45000.0,
                'exit_price': 46000.0,
                'quantity': 1.0,
                'pnl': 1000.0
            },
            {
                'entry_date': datetime.now(),
                'symbol': 'ETH',
                'entry_price': 2500.0,
                'exit_price': 2600.0,
                'quantity': 2.0,
                'pnl': 200.0
            }
        ]
        
        count = temp_db.add_trades_batch(trades)
        assert count == 2
        
        all_trades = temp_db.get_trades()
        assert len(all_trades) == 2
    
    def test_add_and_get_skill(self, temp_db):
        """Test adding and retrieving skills"""
        from src.core.models import Skill
        
        skill = Skill(
            name="Python",
            category="programming",
            proficiency_level="advanced"
        )
        skill_id = temp_db.add_skill(skill)
        assert skill_id > 0
        
        retrieved = temp_db.get_skill("Python")
        assert retrieved is not None
        assert retrieved.name == "Python"
        assert retrieved.category == "programming"
    
    def test_list_skills(self, temp_db):
        """Test listing skills"""
        from src.core.models import Skill
        
        skill1 = Skill(name="Python", category="programming")
        skill2 = Skill(name="Solidity", category="programming")
        skill3 = Skill(name="Trading", category="finance")
        
        temp_db.add_skill(skill1)
        temp_db.add_skill(skill2)
        temp_db.add_skill(skill3)
        
        all_skills = temp_db.list_skills()
        assert len(all_skills) >= 3
        
        programming_skills = temp_db.list_skills(category="programming")
        assert len(programming_skills) >= 2

