"""Test currency utilities"""

from src.core.currency import format_cost, get_last_used_currency, format_gas_fee, calculate_total_cost
from src.core.models import Entry, EntryType


class TestCurrencyFormatting:
    """Test currency formatting functions"""
    
    def test_format_cost_usd(self):
        """Test USD formatting"""
        result = format_cost(100.50, "USD")
        assert result == "$100.50 USD"
    
    def test_format_cost_eth(self):
        """Test ETH formatting (6 decimals)"""
        result = format_cost(0.123456, "ETH")
        assert result == "0.123456 ETH"
    
    def test_format_cost_btc(self):
        """Test BTC formatting (6 decimals)"""
        result = format_cost(0.001234, "BTC")
        assert result == "0.001234 BTC"
    
    def test_format_cost_sol(self):
        """Test SOL formatting (4 decimals)"""
        result = format_cost(1.2345, "SOL")
        assert result == "1.2345 SOL"
    
    def test_format_cost_unknown(self):
        """Test unknown currency formatting"""
        result = format_cost(100, "XYZ")
        assert "100 XYZ" in result or result == "100 XYZ"
    
    def test_format_cost_zero(self):
        """Test zero value formatting"""
        result = format_cost(0, "USD")
        assert "$0.00 USD" in result or "0.00 USD" in result
    
    def test_format_gas_fee(self):
        """Test gas fee formatting"""
        result = format_gas_fee(0.001, "ETH")
        assert "0.001000 ETH" in result or "0.001 ETH" in result
    
    def test_calculate_total_cost_same_currency(self):
        """Test calculating total cost with same currency gas fee"""
        total, currency = calculate_total_cost(100.0, "USD", gas_fee=5.0, gas_currency="USD")
        assert total == 105.0
        assert currency == "USD"
    
    def test_calculate_total_cost_no_gas(self):
        """Test calculating total cost without gas fee"""
        total, currency = calculate_total_cost(100.0, "USD")
        assert total == 100.0
        assert currency == "USD"
    
    def test_calculate_total_cost_different_currency(self):
        """Test calculating total cost with different currency gas (should not add)"""
        total, currency = calculate_total_cost(100.0, "USD", gas_fee=0.001, gas_currency="ETH")
        assert total == 100.0  # Should not add different currencies
        assert currency == "USD"


class TestGetLastUsedCurrency:
    """Test getting last used currency"""
    
    def test_get_last_used_currency_from_entry(self, temp_db):
        """Test getting currency from recent entry"""
        # Create entry with currency
        entry = Entry(
            entry_type=EntryType.RISK,
            notes="Test",
            metadata={"currency": "ETH"}
        )
        temp_db.add_entry(entry)
        
        currency = get_last_used_currency(temp_db)
        assert currency == "ETH"
    
    def test_get_last_used_currency_default(self, temp_db):
        """Test default currency when no entries exist"""
        currency = get_last_used_currency(temp_db)
        assert currency == "USD"

