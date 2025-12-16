"""Examples and templates library"""

from typing import Dict, List, Optional
from ..core.storage import Storage
from ..core.models import EntryType


EXAMPLES = {
    'sports-bet-quick': {
        'description': 'Quick capture (minimal) - when overwhelmed',
        'command': 'nc q 100 "houston bet"',
        'when': 'When overwhelmed, need fast capture',
        'fields_used': ['cost', 'notes']
    },
    'sports-bet-full': {
        'description': 'Full context (structured) - when you have time',
        'command': 'nc risk sports_bet --cost 100 --odds 3.21 --my-probability 0.45 --what-i-see "Market slow" --why-i-trust-this "Similar pattern in trading" "Value bet"',
        'when': 'When you have time, want full context',
        'fields_used': ['cost', 'odds', 'my_probability', 'what_i_see', 'why_i_trust_this']
    },
    'sports-bet-multi-currency': {
        'description': 'Multi-currency with gas fees',
        'command': 'nc risk sports_bet --cost 0.1 --currency ETH --gas-fee 0.001 --gas-currency ETH "ETH bet"',
        'when': 'Betting in crypto, gas fees matter',
        'fields_used': ['cost', 'currency', 'gas_fee', 'gas_currency']
    },
    'sports-bet-intuition': {
        'description': 'With intuition/feels captured',
        'command': 'nc risk sports_bet --cost 100 --odds 3.21 --my-probability 0.45 --gut-feeling "strong" --what-i-see "Market slow to react" --why-i-trust-this "Caught similar pattern 3/4 times" --red-flags "No cash-out available" "Value bet"',
        'when': 'When you want to capture your intuition',
        'fields_used': ['cost', 'odds', 'my_probability', 'gut_feeling', 'what_i_see', 'why_i_trust_this', 'red_flags']
    },
    'sports-bet-connected': {
        'description': 'Connected to other domains',
        'command': 'nc risk sports_bet --cost 100 --odds 3.21 --my-probability 0.45 --related-trades 123 --pattern-match "Similar to BTC breakout last week" --domain-knowledge "Applied momentum pattern from trading" "Cross-domain insight"',
        'when': 'When you see patterns across domains',
        'fields_used': ['cost', 'odds', 'my_probability', 'related_trades', 'pattern_match', 'domain_knowledge_applied']
    }
}


TEMPLATES = {
    'value-bet': {
        'name': 'Value Bet',
        'description': 'Template for value betting with edge calculation',
        'fields': ['cost', 'odds', 'my-probability', 'what-i-see', 'why-i-trust-this'],
        'command_template': 'nc risk sports_bet --cost <amount> --odds <odds> --my-probability <your_prob> --what-i-see "Market slow to react" --why-i-trust-this "Similar pattern in trading" "<notes>"'
    },
    'quick-capture': {
        'name': 'Quick Capture',
        'description': 'Ultra-fast entry when overwhelmed',
        'fields': ['cost', 'notes'],
        'command_template': 'nc q <cost> "<notes>"'
    },
    'multi-currency': {
        'name': 'Multi-Currency',
        'description': 'Betting in crypto with gas fees',
        'fields': ['cost', 'currency', 'gas-fee', 'gas-currency'],
        'command_template': 'nc risk sports_bet --cost <amount> --currency <currency> --gas-fee <gas> --gas-currency <gas_currency> "<notes>"'
    },
    'intuition-capture': {
        'name': 'Intuition Capture',
        'description': 'Capture your gut feeling and reasoning',
        'fields': ['cost', 'gut-feeling', 'what-i-see', 'why-i-trust-this', 'red-flags'],
        'command_template': 'nc risk sports_bet --cost <amount> --gut-feeling "<feeling>" --what-i-see "<what>" --why-i-trust-this "<why>" --red-flags "<flags>" "<notes>"'
    }
}


def get_example(example_id: str) -> Optional[Dict]:
    """Get an example by ID"""
    return EXAMPLES.get(example_id)


def get_template(template_id: str) -> Optional[Dict]:
    """Get a template by ID"""
    return TEMPLATES.get(template_id)


def get_contrast(storage: Storage, entry_id: int) -> Dict:
    """Get contrast view - how others structure similar bets"""
    try:
        # Get the entry
        entries = storage.get_entries(limit=10000)
        entry = next((e for e in entries if e.id == entry_id), None)
        
        if not entry or entry.entry_type != EntryType.RISK:
            return {'error': 'Entry not found or not a risk entry'}
        
        risk_data = entry.metadata or {}
        risk_type = risk_data.get('risk_type', 'sports_bet')
        
        # Find similar examples
        similar_examples = []
        for example_id, example in EXAMPLES.items():
            if risk_type in example_id or 'sports-bet' in example_id:
                similar_examples.append(example)
        
        return {
            'your_structure': {
                'fields_used': [k for k, v in risk_data.items() if v is not None and k not in ['status', 'reward_history', 'opportunity_cost_history']],
                'quick_mode': risk_data.get('quick_mode', False)
            },
            'similar_examples': similar_examples[:3],  # Top 3 similar
            'suggestions': []
        }
    except Exception:
        return {'error': 'Failed to get contrast view'}
