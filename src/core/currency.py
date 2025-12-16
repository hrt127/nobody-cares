"""Currency utilities for multi-currency support"""

from typing import Optional
from .storage import Storage
from .models import EntryType


def format_cost(cost: float, currency: str) -> str:
    """Format cost with currency - smart formatting based on currency type"""
    if currency in ["USD", "USDC", "USDT"]:
        return f"${cost:.2f} {currency}"
    elif currency in ["ETH", "BTC"]:
        return f"{cost:.6f} {currency}"
    elif currency in ["SOL", "MATIC", "AVAX"]:
        return f"{cost:.4f} {currency}"
    else:
        # Generic formatting for unknown currencies
        return f"{cost} {currency}"


def get_last_used_currency(storage: Storage) -> str:
    """Get last used currency (smart default)"""
    # Get from recent risk entries
    recent = storage.get_entries(limit=10, entry_type=EntryType.RISK)
    if recent:
        for entry in recent:
            risk_data = entry.metadata
            currency = risk_data.get('currency')
            if currency:
                return currency
    return 'USD'


def format_gas_fee(gas_fee: float, currency: str) -> str:
    """Format gas fee with currency"""
    return format_cost(gas_fee, currency)


def calculate_total_cost(entry_cost: float, currency: str, 
                         gas_fee: Optional[float] = None, 
                         gas_currency: Optional[str] = None) -> tuple[float, str]:
    """Calculate total cost, handling different currencies"""
    if gas_fee and gas_currency == currency:
        return entry_cost + gas_fee, currency
    return entry_cost, currency
