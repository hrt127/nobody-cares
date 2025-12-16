"""Test risk tracking functionality"""

import pytest
from datetime import datetime

from src.core.models import Entry, EntryType


class TestRiskTracking:
    """Test risk tracking operations"""
    
    def test_log_risk_entry(self, temp_db):
        """Test logging a risk entry with metadata"""
        risk_metadata = {
            "risk_type": "nft",
            "entry_cost": 6.3,
            "currency": "USD",
            "initial_expected_value": 15.0,
            "current_expected_value": 15.0,
            "confidence_level": 0.65,
            "opportunity_cost_perceived": 5.0,
            "opportunity_cost_real": None,
            "max_loss": 6.3,
            "max_gain": 25.0,
            "status": "open",
            "reward_history": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "expected_value": 15.0,
                    "reason": "initial"
                }
            ],
            "opportunity_cost_history": []
        }
        
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="NFT purchase",
            tags=["nft", "risk"],
            metadata=risk_metadata
        )
        entry_id = temp_db.add_entry(entry)
        
        # Retrieve and verify
        entries = temp_db.get_entries(entry_type=EntryType.RISK)
        assert len(entries) == 1
        assert entries[0].metadata["risk_type"] == "nft"
        assert entries[0].metadata["entry_cost"] == 6.3
        assert entries[0].metadata["current_expected_value"] == 15.0
    
    def test_update_risk_reward(self, temp_db):
        """Test updating risk reward over time"""
        risk_metadata = {
            "risk_type": "sports_bet",
            "entry_cost": 100.0,
            "current_expected_value": 150.0,
            "reward_history": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "expected_value": 150.0,
                    "reason": "initial"
                }
            ],
            "status": "open"
        }
        
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Sports bet",
            metadata=risk_metadata
        )
        entry_id = temp_db.add_entry(entry)
        
        # Update reward
        updated_metadata = risk_metadata.copy()
        updated_metadata["current_expected_value"] = 180.0
        updated_metadata["reward_history"].append({
            "timestamp": datetime.now().isoformat(),
            "expected_value": 180.0,
            "reason": "odds moved favorably"
        })
        
        temp_db.update_entry_metadata(entry_id, updated_metadata)
        
        # Verify update
        entries = temp_db.get_entries()
        updated_entry = next(e for e in entries if e.id == entry_id)
        assert updated_entry.metadata["current_expected_value"] == 180.0
        assert len(updated_entry.metadata["reward_history"]) == 2
    
    def test_opportunity_cost_tracking(self, temp_db):
        """Test opportunity cost tracking"""
        risk_metadata = {
            "risk_type": "prediction_market",
            "entry_cost": 50.0,
            "opportunity_cost_perceived": 5.0,
            "opportunity_cost_real": None,
            "opportunity_cost_history": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "opportunity_cost": 5.0,
                    "type": "perceived",
                    "notes": "Initial assessment"
                }
            ],
            "status": "open"
        }
        
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Prediction market",
            metadata=risk_metadata
        )
        entry_id = temp_db.add_entry(entry)
        
        # Update real opportunity cost
        updated_metadata = risk_metadata.copy()
        updated_metadata["opportunity_cost_real"] = 8.0
        updated_metadata["opportunity_cost_history"].append({
            "timestamp": datetime.now().isoformat(),
            "opportunity_cost": 8.0,
            "type": "real",
            "notes": "Market conditions changed"
        })
        
        temp_db.update_entry_metadata(entry_id, updated_metadata)
        
        # Verify
        entries = temp_db.get_entries()
        updated_entry = next(e for e in entries if e.id == entry_id)
        assert updated_entry.metadata["opportunity_cost_real"] == 8.0
        assert len(updated_entry.metadata["opportunity_cost_history"]) == 2

