"""Test data importers"""

import pytest
import tempfile
import pandas as pd
from pathlib import Path

from src.importers import TradingPerformanceImporter


class TestTradingPerformanceImporter:
    """Test trading performance CSV importer"""
    
    def test_validate_valid_csv(self):
        """Test validation of valid trading CSV"""
        # Create a temporary CSV with valid structure
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("entry_date,exit_date,symbol,entry_price,exit_price,quantity,pnl,return_pct\n")
            f.write("2024-01-01,2024-01-02,BTC,45000,46000,1,1000,2.22\n")
            csv_path = Path(f.name)
        
        try:
            importer = TradingPerformanceImporter(csv_path)
            assert importer.validate() is True
        finally:
            csv_path.unlink()
    
    def test_parse_trading_csv(self):
        """Test parsing a trading CSV"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("entry_date,exit_date,symbol,entry_price,exit_price,quantity,pnl,return_pct\n")
            f.write("2024-01-01,2024-01-02,BTC,45000,46000,1,1000,2.22\n")
            f.write("2024-01-03,2024-01-04,ETH,2500,2600,2,200,4.00\n")
            csv_path = Path(f.name)
        
        try:
            importer = TradingPerformanceImporter(csv_path)
            data = importer.parse()
            
            assert len(data['trades']) == 2
            assert data['total_trades'] == 2
            assert 'metrics' in data
            assert data['metrics']['total_pnl'] == 1200.0
        finally:
            csv_path.unlink()
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("entry_date,exit_date,symbol,entry_price,exit_price,quantity,pnl,return_pct\n")
            f.write("2024-01-01,2024-01-02,BTC,45000,46000,1,1000,2.22\n")
            f.write("2024-01-03,2024-01-04,ETH,2500,2400,2,-200,-4.00\n")
            csv_path = Path(f.name)
        
        try:
            importer = TradingPerformanceImporter(csv_path)
            data = importer.parse()
            metrics = data['metrics']
            
            assert metrics['total_pnl'] == 800.0
            assert metrics['win_rate'] == 50.0  # 1 win, 1 loss
            assert metrics['avg_pnl'] == 400.0
        finally:
            csv_path.unlink()

