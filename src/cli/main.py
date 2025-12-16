"""Main CLI entry point"""

import click
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..core.storage import Storage
from ..core.models import Entry, EntryType, Project
from ..core.utils import get_week_start, get_week_end
from ..alpha import AlphaBriefGenerator, BriefFormatter
from ..improvements import get_template
from ..importers import TradingPerformanceImporter
from ..outputs import (
    TwitterThreadGenerator, LinkedInPostGenerator,
    VideoScriptGenerator, PDFReportGenerator
)


# Global storage instance
_storage = None


def get_storage() -> Storage:
    """Get or create storage instance"""
    global _storage
    if _storage is None:
        _storage = Storage()
    return _storage


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Nobody Cares - Daily Improvement Hub
    
    Track daily activities, build skills portfolios, analyze performance, and generate insights.
    """
    pass


@main.command()
@click.argument('entry_type', type=click.Choice(['trade', 'code', 'alpha', 'learning', 'action', 'note', 'opportunity', 'risk'], case_sensitive=False))
@click.argument('notes', nargs=-1, required=True)
@click.option('--tags', '-t', help='Comma-separated tags')
@click.option('--source', '-s', default='manual', help='Entry source (manual/auto/sync)')
def log(entry_type: str, notes: tuple, tags: str, source: str):
    """Log a daily entry
    
    Examples:
        nc log trade "BTC long @ 45k, exit @ 46.2k, +2.6%"
        nc log code "Fixed authentication bug, PR #123" --tags bugfix,security
        nc log alpha "Saw restaking narrative in Telegram" --tags restaking,degen
    """
    storage = get_storage()
    
    # Combine notes tuple into single string
    notes_text = ' '.join(notes)
    
    # Parse tags
    tag_list = []
    if tags:
        tag_list.extend([t.strip() for t in tags.split(',')])
    
    # Also extract hashtags from notes
    import re
    hashtags = re.findall(r'#(\w+)', notes_text)
    tag_list.extend(hashtags)
    tag_list = list(set(tag_list))  # Remove duplicates
    
    # Create entry
    try:
        entry_type_enum = EntryType(entry_type.lower())
    except ValueError:
        click.echo(f"Error: Invalid entry type '{entry_type}'", err=True)
        return
    
    entry = Entry(
        entry_type=entry_type_enum,
        notes=notes_text,
        tags=tag_list,
        source=source,
        timestamp=datetime.now()
    )
    
    entry_id = storage.add_entry(entry)
    click.echo(f"✓ Logged entry #{entry_id}: {entry_type} - {notes_text[:50]}...")
    if tag_list:
        click.echo(f"  Tags: {', '.join(tag_list)}")


@main.command('risk')
@click.argument('risk_type', type=click.Choice(['nft', 'sports_bet', 'prediction_market', 'trade', 'crypto', 'other']))
@click.option('--cost', '-c', type=float, required=True, help='Entry cost / amount at risk')
@click.option('--expected-value', '-ev', type=float, help='Initial expected upside/outcome value')
@click.option('--timeframe', '-t', help='Expected timeframe (e.g., "2 weeks", "end of game")')
@click.option('--odds', '-o', type=float, help='Current odds or entry price')
@click.option('--fair-value', '-fv', type=float, help='Your assessment of fair value')
@click.option('--confidence', type=float, help='Confidence level (0.0-1.0) in expected value')
@click.option('--opportunity-cost', '-oc', type=float, help='Perceived opportunity cost')
@click.option('--opportunity-cost-real', '-ocr', type=float, help='Real/actual opportunity cost')
@click.option('--opportunity-cost-notes', help='What opportunities are being passed up')
@click.option('--max-loss', type=float, help='Worst case scenario loss')
@click.option('--max-gain', type=float, help='Best case scenario gain')
@click.option('--risk-factors', '-rf', help='Comma-separated risk factors')
@click.option('--exit-strategy', '-e', help='Exit strategy/plan')
@click.option('--liquidity', type=click.Choice(['high', 'medium', 'low', 'locked']), help='Liquidity rating')
@click.option('--time-to-exit', help='Time needed to exit (e.g., "instant", "24 hours")')
@click.option('--allocation', type=float, help='Portfolio allocation % (of total risk capital)')
@click.option('--correlated', help='Comma-separated list of correlated risk IDs or descriptions')
@click.option('--edge', type=click.Choice(['public', 'private', 'research', 'insider']), help='Information edge type')
@click.option('--time-invested', type=float, help='Time invested researching/monitoring (hours)')
@click.option('--currency', default='USD', help='Currency (default: USD)')
@click.argument('notes', nargs=-1)
def log_risk(risk_type: str, cost: float, expected_value: Optional[float], timeframe: Optional[str],
             odds: Optional[float], fair_value: Optional[float], confidence: Optional[float],
             opportunity_cost: Optional[float], opportunity_cost_real: Optional[float],
             opportunity_cost_notes: Optional[str], max_loss: Optional[float], max_gain: Optional[float],
             risk_factors: Optional[str], exit_strategy: Optional[str], liquidity: Optional[str],
             time_to_exit: Optional[str], allocation: Optional[float], correlated: Optional[str],
             edge: Optional[str], time_invested: Optional[float], currency: str, notes: tuple):
    """Log a risk-taking activity with comprehensive structured data
    
    Examples:
        nc risk nft --cost 6.3 --expected-value 15 --timeframe "4 weeks" --opportunity-cost 5 "Cool Punks #1234"
        nc risk sports_bet --cost 100 --odds 3.21 --fair-value 2.0 --risk-factors "no_cash_out" "Game X vs Y"
        nc risk prediction_market --cost 50 --expected-value 150 --confidence 0.75 --max-loss 50 "Event outcome"
    """
    storage = get_storage()
    
    notes_text = ' '.join(notes) if notes else ""
    
    # Parse risk factors and correlated risks
    risk_factors_list = []
    if risk_factors:
        risk_factors_list = [rf.strip() for rf in risk_factors.split(',')]
    
    correlated_list = []
    if correlated:
        correlated_list = [c.strip() for c in correlated.split(',')]
    
    # Create risk entry metadata
    risk_entry_data = {
        'risk_type': risk_type,
        'entry_cost': cost,
        'currency': currency,
        'initial_expected_value': expected_value,
        'current_expected_value': expected_value,
        'expected_timeframe': timeframe,
        'confidence_level': confidence,
        'opportunity_cost_perceived': opportunity_cost,
        'opportunity_cost_real': opportunity_cost_real,
        'opportunity_cost_notes': opportunity_cost_notes,
        'odds_or_price': odds,
        'fair_value': fair_value,
        'max_loss': max_loss,
        'max_gain': max_gain,
        'risk_factors': risk_factors_list,
        'exit_strategy': exit_strategy,
        'liquidity_rating': liquidity,
        'time_to_exit': time_to_exit,
        'portfolio_allocation_pct': allocation,
        'correlated_risks': correlated_list,
        'information_edge': edge,
        'time_invested_hours': time_invested,
        'status': 'open',
        'reward_history': [],
        'opportunity_cost_history': []
    }
    
    # Add initial reward to history if provided
    if expected_value is not None:
        risk_entry_data['reward_history'].append({
            'timestamp': datetime.now().isoformat(),
            'expected_value': expected_value,
            'notes': 'Initial expected value',
            'reason': 'initial',
            'confidence_level': confidence
        })
    
    # Add initial opportunity cost to history if provided
    if opportunity_cost is not None:
        risk_entry_data['opportunity_cost_history'].append({
            'timestamp': datetime.now().isoformat(),
            'opportunity_cost': opportunity_cost,
            'type': 'perceived',
            'notes': opportunity_cost_notes or 'Initial perceived opportunity cost'
        })
    
    if opportunity_cost_real is not None:
        risk_entry_data['opportunity_cost_history'].append({
            'timestamp': datetime.now().isoformat(),
            'opportunity_cost': opportunity_cost_real,
            'type': 'real',
            'notes': opportunity_cost_notes or 'Initial real opportunity cost'
        })
    
    # Create main entry
    entry = Entry(
        entry_type=EntryType.RISK,
        notes=notes_text or f"{risk_type}: ${cost} {currency}",
        tags=[risk_type, "risk"],
        source="manual",
        timestamp=datetime.now(),
        metadata=risk_entry_data
    )
    
    entry_id = storage.add_entry(entry)
    
    # Show comprehensive stats
    click.echo(f"✓ Logged risk entry #{entry_id}: {risk_type}")
    click.echo(f"  Cost: ${cost:.2f} {currency}")
    
    if expected_value:
        potential_return = expected_value - cost
        roi = (potential_return / cost) * 100 if cost > 0 else 0
        conf_str = f" ({confidence*100:.0f}% confidence)" if confidence else ""
        click.echo(f"  Expected reward: ${expected_value:.2f} {currency} (potential +${potential_return:.2f}, {roi:.1f}% ROI){conf_str}")
    
    if odds and fair_value:
        edge_pct = ((odds / fair_value) - 1) * 100 if fair_value > 0 else 0
        click.echo(f"  Edge: {edge_pct:.1f}% (odds {odds} vs fair {fair_value})")
    
    if opportunity_cost is not None or opportunity_cost_real is not None:
        oc_perceived = opportunity_cost if opportunity_cost is not None else 0
        oc_real = opportunity_cost_real if opportunity_cost_real is not None else (opportunity_cost if opportunity_cost is not None else 0)
        if opportunity_cost_real is not None:
            click.echo(f"  Opportunity cost: ${oc_perceived:.2f} perceived → ${oc_real:.2f} real")
        else:
            click.echo(f"  Opportunity cost: ${oc_perceived:.2f} (perceived)")
    
    if max_loss and max_gain:
        click.echo(f"  Risk range: -${max_loss:.2f} to +${max_gain:.2f}")
    
    if risk_factors_list:
        click.echo(f"  Risk factors: {', '.join(risk_factors_list)}")
    
    if liquidity:
        click.echo(f"  Liquidity: {liquidity}")
    
    if allocation:
        click.echo(f"  Portfolio allocation: {allocation:.1f}%")


@main.command('update-risk')
@click.argument('entry_id', type=int)
@click.option('--reward', '-r', type=float, help='New expected reward/value')
@click.option('--confidence', type=float, help='Updated confidence level (0.0-1.0)')
@click.option('--opportunity-cost', '-oc', type=float, help='Update perceived opportunity cost')
@click.option('--opportunity-cost-real', '-ocr', type=float, help='Update real opportunity cost')
@click.option('--reason', help='Reason for the change')
@click.option('--status', type=click.Choice(['open', 'closed', 'realized', 'written_off']), help='Update status')
@click.option('--realized-value', type=float, help='Actual realized value (when closing)')
@click.argument('notes', nargs=-1)
def update_risk(entry_id: int, reward: Optional[float], confidence: Optional[float],
                opportunity_cost: Optional[float], opportunity_cost_real: Optional[float],
                reason: Optional[str], status: Optional[str], realized_value: Optional[float], notes: tuple):
    """Update a risk entry with new reward/value, opportunity cost, or status
    
    Examples:
        nc update-risk 1 --reward 20 --reason "market moved favorably"
        nc update-risk 1 --opportunity-cost-real 8 --reason "missed better opportunity"
        nc update-risk 1 --status closed --realized-value 12.5
    """
    storage = get_storage()
    
    # Get the entry
    entries = storage.get_entries(limit=10000)
    entry = next((e for e in entries if e.id == entry_id), None)
    
    if not entry or entry.entry_type != EntryType.RISK:
        click.echo(f"Error: Risk entry #{entry_id} not found", err=True)
        return
    
    notes_text = ' '.join(notes) if notes else ""
    risk_data = entry.metadata.copy()
    
    # Update reward if provided
    if reward is not None:
        old_reward = risk_data.get('current_expected_value')
        risk_data['current_expected_value'] = reward
        
        if 'reward_history' not in risk_data:
            risk_data['reward_history'] = []
        
        reward_update = {
            'timestamp': datetime.now().isoformat(),
            'expected_value': reward,
            'notes': notes_text or None,
            'reason': reason or 'updated',
            'confidence_level': confidence or risk_data.get('confidence_level')
        }
        risk_data['reward_history'].append(reward_update)
        
        # Use explicit None check to handle zero values correctly
        if old_reward is not None:
            change = reward - old_reward
            change_pct = ((reward / old_reward) - 1) * 100 if old_reward > 0 else 0
            click.echo(f"✓ Updated reward: ${old_reward:.2f} → ${reward:.2f} ({change:+.2f}, {change_pct:+.1f}%)")
        else:
            click.echo(f"✓ Set reward: ${reward:.2f}")
        
        if confidence is not None:
            risk_data['confidence_level'] = confidence
    
    # Update opportunity cost
    if opportunity_cost is not None:
        old_oc = risk_data.get('opportunity_cost_perceived')
        risk_data['opportunity_cost_perceived'] = opportunity_cost
        
        if 'opportunity_cost_history' not in risk_data:
            risk_data['opportunity_cost_history'] = []
        
        risk_data['opportunity_cost_history'].append({
            'timestamp': datetime.now().isoformat(),
            'opportunity_cost': opportunity_cost,
            'type': 'perceived',
            'notes': notes_text or reason or 'Updated perceived opportunity cost'
        })
        
        if old_oc is not None:
            click.echo(f"✓ Updated perceived opportunity cost: ${old_oc:.2f} → ${opportunity_cost:.2f}")
        else:
            click.echo(f"✓ Set perceived opportunity cost: ${opportunity_cost:.2f}")
    
    if opportunity_cost_real is not None:
        old_oc_real = risk_data.get('opportunity_cost_real')
        risk_data['opportunity_cost_real'] = opportunity_cost_real
        
        if 'opportunity_cost_history' not in risk_data:
            risk_data['opportunity_cost_history'] = []
        
        risk_data['opportunity_cost_history'].append({
            'timestamp': datetime.now().isoformat(),
            'opportunity_cost': opportunity_cost_real,
            'type': 'real',
            'notes': notes_text or reason or 'Updated real opportunity cost'
        })
        
        if old_oc_real is not None:
            click.echo(f"✓ Updated real opportunity cost: ${old_oc_real:.2f} → ${opportunity_cost_real:.2f}")
        else:
            click.echo(f"✓ Set real opportunity cost: ${opportunity_cost_real:.2f}")
    
    # Update status
    if status:
        risk_data['status'] = status
        click.echo(f"✓ Status: {status}")
    
    # Update realized value
    if realized_value is not None:
        risk_data['realized_value'] = realized_value
        if 'reward_history' not in risk_data:
            risk_data['reward_history'] = []
        risk_data['reward_history'].append({
            'timestamp': datetime.now().isoformat(),
            'expected_value': realized_value,
            'notes': notes_text or 'Realized value',
            'reason': 'realized'
        })
        cost = risk_data.get('entry_cost', 0)
        pnl = realized_value - cost
        roi = (pnl / cost) * 100 if cost > 0 else 0
        click.echo(f"✓ Realized value: ${realized_value:.2f} (PnL: ${pnl:+.2f}, ROI: {roi:+.1f}%)")
    
    # Update entry metadata in database
    storage.update_entry_metadata(entry_id, risk_data)


@main.command('risks')
@click.option('--type', '-t', help='Filter by risk type')
@click.option('--status', '-s', help='Filter by status (open/closed/realized/written_off)')
@click.option('--show-history', is_flag=True, help='Show reward and opportunity cost history')
@click.option('--show-all', is_flag=True, help='Show all fields including opportunity cost, max loss/gain, etc.')
def list_risks(type: str, status: str, show_history: bool, show_all: bool):
    """List all risk entries with comprehensive stats"""
    storage = get_storage()
    
    entries = storage.get_entries(entry_type=EntryType.RISK)
    
    # Filter by type and status if provided
    if type:
        entries = [e for e in entries if e.metadata.get('risk_type') == type]
    if status:
        entries = [e for e in entries if e.metadata.get('status') == status]
    
    if not entries:
        click.echo("No risk entries found.")
        return
    
    click.echo(f"\n⚠️  Risk Entries ({len(entries)} total)\n")
    click.echo("=" * 80)
    
    total_at_risk = 0
    total_current_expected = 0
    total_realized = 0
    total_opportunity_cost = 0
    
    for entry in entries:
        risk_data = entry.metadata
        risk_type = risk_data.get('risk_type', 'unknown')
        cost = risk_data.get('entry_cost', 0)
        current_ev = risk_data.get('current_expected_value')
        initial_ev = risk_data.get('initial_expected_value')
        realized = risk_data.get('realized_value')
        risk_status = risk_data.get('status', 'open')
        oc_perceived = risk_data.get('opportunity_cost_perceived')
        oc_real = risk_data.get('opportunity_cost_real')
        
        total_at_risk += cost
        if current_ev:
            total_current_expected += current_ev
        if realized:
            total_realized += realized
        # Use explicit None checks to handle zero values correctly
        if oc_real is not None:
            total_opportunity_cost += oc_real
        elif oc_perceived is not None:
            total_opportunity_cost += oc_perceived
        
        status_icon = {
            'open': '🟢',
            'closed': '🔴',
            'realized': '✅',
            'written_off': '❌'
        }.get(risk_status, '⚪')
        
        click.echo(f"\n{status_icon} [{entry.id}] {risk_type.upper()} - {risk_status}")
        click.echo(f"  Cost: ${cost:.2f} {risk_data.get('currency', 'USD')}")
        
        if initial_ev and current_ev:
            if current_ev != initial_ev:
                change = current_ev - initial_ev
                change_pct = ((current_ev / initial_ev) - 1) * 100
                conf_str = f" ({risk_data.get('confidence_level', 0)*100:.0f}% confidence)" if risk_data.get('confidence_level') else ""
                click.echo(f"  Expected: ${initial_ev:.2f} → ${current_ev:.2f} ({change:+.2f}, {change_pct:+.1f}%){conf_str}")
            else:
                conf_str = f" ({risk_data.get('confidence_level', 0)*100:.0f}% confidence)" if risk_data.get('confidence_level') else ""
                click.echo(f"  Expected: ${current_ev:.2f}{conf_str}")
        elif current_ev:
            conf_str = f" ({risk_data.get('confidence_level', 0)*100:.0f}% confidence)" if risk_data.get('confidence_level') else ""
            click.echo(f"  Expected: ${current_ev:.2f}{conf_str}")
        
        if realized is not None:
            pnl = realized - cost
            roi = (pnl / cost) * 100 if cost > 0 else 0
            click.echo(f"  Realized: ${realized:.2f} (PnL: ${pnl:+.2f}, ROI: {roi:+.1f}%)")
        
        if show_all:
            if oc_perceived is not None or oc_real is not None:
                if oc_real is not None and oc_perceived is not None:
                    click.echo(f"  Opportunity cost: ${oc_perceived:.2f} perceived → ${oc_real:.2f} real")
                elif oc_real is not None:
                    click.echo(f"  Opportunity cost: ${oc_real:.2f} (real)")
                elif oc_perceived is not None:
                    click.echo(f"  Opportunity cost: ${oc_perceived:.2f} (perceived)")
                if risk_data.get('opportunity_cost_notes'):
                    click.echo(f"    Notes: {risk_data['opportunity_cost_notes']}")
            
            if risk_data.get('max_loss') and risk_data.get('max_gain'):
                click.echo(f"  Risk range: -${risk_data['max_loss']:.2f} to +${risk_data['max_gain']:.2f}")
            
            if risk_data.get('liquidity_rating'):
                click.echo(f"  Liquidity: {risk_data['liquidity_rating']}")
            
            if risk_data.get('portfolio_allocation_pct'):
                click.echo(f"  Portfolio allocation: {risk_data['portfolio_allocation_pct']:.1f}%")
            
            if risk_data.get('information_edge'):
                click.echo(f"  Information edge: {risk_data['information_edge']}")
            
            if risk_data.get('time_invested_hours'):
                click.echo(f"  Time invested: {risk_data['time_invested_hours']:.1f} hours")
        
        if entry.notes:
            click.echo(f"  Notes: {entry.notes}")
        click.echo(f"  Date: {entry.timestamp.strftime('%Y-%m-%d %H:%M')}")
        
        # Show reward history if requested
        if show_history and risk_data.get('reward_history'):
            click.echo(f"  📈 Reward History:")
            for update in risk_data['reward_history']:
                update_time = datetime.fromisoformat(update['timestamp']) if isinstance(update['timestamp'], str) else update['timestamp']
                conf_str = f" ({update.get('confidence_level', 0)*100:.0f}% conf)" if update.get('confidence_level') else ""
                click.echo(f"     {update_time.strftime('%Y-%m-%d %H:%M')}: ${update['expected_value']:.2f}{conf_str}")
                if update.get('reason'):
                    click.echo(f"       Reason: {update['reason']}")
                if update.get('notes'):
                    click.echo(f"       Notes: {update['notes']}")
        
        # Show opportunity cost history if requested
        if show_history and risk_data.get('opportunity_cost_history'):
            click.echo(f"  💰 Opportunity Cost History:")
            for update in risk_data['opportunity_cost_history']:
                update_time = datetime.fromisoformat(update['timestamp']) if isinstance(update['timestamp'], str) else update['timestamp']
                oc_type = update.get('type', 'unknown')
                click.echo(f"     {update_time.strftime('%Y-%m-%d %H:%M')}: ${update['opportunity_cost']:.2f} ({oc_type})")
                if update.get('notes'):
                    click.echo(f"       Notes: {update['notes']}")
    
    click.echo(f"\n📊 Summary:")
    click.echo(f"  Total at risk: ${total_at_risk:.2f}")
    if total_current_expected > 0:
        click.echo(f"  Total current expected: ${total_current_expected:.2f}")
        click.echo(f"  Total potential profit: ${total_current_expected - total_at_risk:.2f}")
    if total_opportunity_cost > 0:
        click.echo(f"  Total opportunity cost: ${total_opportunity_cost:.2f}")
        click.echo(f"  Net expected (after OC): ${total_current_expected - total_at_risk - total_opportunity_cost:.2f}")
    if total_realized > 0:
        click.echo(f"  Total realized: ${total_realized:.2f}")
        click.echo(f"  Total realized PnL: ${total_realized - total_at_risk:.2f}")


@main.command()
@click.option('--type', '-t', help='Filter by entry type')
@click.option('--tags', help='Filter by tags (comma-separated)')
def today(type: str, tags: str):
    """Show all entries for today"""
    storage = get_storage()
    
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.now()
    
    entry_type = None
    if type:
        try:
            entry_type = EntryType(type.lower())
        except ValueError:
            click.echo(f"Error: Invalid entry type '{type}'", err=True)
            return
    
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
    
    entries = storage.get_entries(
        entry_type=entry_type,
        start_date=start_date,
        end_date=end_date,
        tags=tag_list
    )
    
    if not entries:
        click.echo("No entries found for today.")
        return
    
    click.echo(f"\n📅 Today's Entries ({len(entries)} total)\n")
    click.echo("=" * 80)
    
    for entry in entries:
        time_str = entry.timestamp.strftime("%H:%M")
        type_icon = {
            'trade': '💰',
            'code': '💻',
            'alpha': '📊',
            'learning': '📚',
            'action': '✅',
            'note': '📝',
            'opportunity': '🎯'
        }.get(entry.entry_type.value, '•')
        
        click.echo(f"\n{type_icon} [{time_str}] {entry.entry_type.value.upper()}")
        click.echo(f"   {entry.notes}")
        
        if entry.tags:
            click.echo(f"   Tags: {', '.join(entry.tags)}")
        
        if entry.source != 'manual':
            click.echo(f"   Source: {entry.source}")


@main.command()
@click.option('--type', '-t', help='Filter by entry type')
@click.option('--tags', help='Filter by tags (comma-separated)')
def week(type: str, tags: str):
    """Show weekly summary"""
    storage = get_storage()
    
    today = datetime.now()
    start_date = get_week_start(today)
    end_date = get_week_end(today)
    
    entry_type = None
    if type:
        try:
            entry_type = EntryType(type.lower())
        except ValueError:
            click.echo(f"Error: Invalid entry type '{type}'", err=True)
            return
    
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
    
    entries = storage.get_entries(
        entry_type=entry_type,
        start_date=start_date,
        end_date=end_date,
        tags=tag_list
    )
    
    if not entries:
        click.echo(f"No entries found for this week ({start_date.date()} - {end_date.date()}).")
        return
    
    # Group by type
    by_type = {}
    for entry in entries:
        entry_type_val = entry.entry_type.value
        if entry_type_val not in by_type:
            by_type[entry_type_val] = []
        by_type[entry_type_val].append(entry)
    
    click.echo(f"\n📊 Weekly Summary ({start_date.date()} - {end_date.date()})")
    click.echo(f"Total entries: {len(entries)}\n")
    click.echo("=" * 80)
    
    type_icons = {
        'trade': '💰',
        'code': '💻',
        'alpha': '📊',
        'learning': '📚',
        'action': '✅',
        'note': '📝',
        'opportunity': '🎯'
    }
    
    for entry_type_val, type_entries in sorted(by_type.items()):
        icon = type_icons.get(entry_type_val, '•')
        click.echo(f"\n{icon} {entry_type_val.upper()} ({len(type_entries)} entries)")
        
        for entry in type_entries[:5]:  # Show first 5 of each type
            time_str = entry.timestamp.strftime("%a %H:%M")
            click.echo(f"   [{time_str}] {entry.notes[:70]}...")
        
        if len(type_entries) > 5:
            click.echo(f"   ... and {len(type_entries) - 5} more")


@main.command()
@click.option('--type', '-t', help='Filter by entry type')
@click.option('--limit', '-n', default=20, help='Number of entries to show')
def recent(type: str, limit: int):
    """Show recent entries"""
    storage = get_storage()
    
    entry_type = None
    if type:
        try:
            entry_type = EntryType(type.lower())
        except ValueError:
            click.echo(f"Error: Invalid entry type '{type}'", err=True)
            return
    
    entries = storage.get_entries(entry_type=entry_type, limit=limit)
    
    if not entries:
        click.echo("No entries found.")
        return
    
    click.echo(f"\n📝 Recent Entries (last {len(entries)})\n")
    click.echo("=" * 80)
    
    type_icons = {
        'trade': '💰',
        'code': '💻',
        'alpha': '📊',
        'learning': '📚',
        'action': '✅',
        'note': '📝',
        'opportunity': '🎯'
    }
    
    for entry in entries:
        date_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
        icon = type_icons.get(entry.entry_type.value, '•')
        
        click.echo(f"\n{icon} [{date_str}] {entry.entry_type.value.upper()}")
        click.echo(f"   {entry.notes}")
        
        if entry.tags:
            click.echo(f"   Tags: {', '.join(entry.tags)}")


@main.group()
def project():
    """Manage projects"""
    pass


@project.command('create')
@click.argument('name')
@click.option('--description', '-d', help='Project description')
def create_project(name: str, description: str):
    """Create a new project"""
    storage = get_storage()
    
    # Check if project already exists
    existing = storage.get_project_by_name(name)
    if existing:
        click.echo(f"Error: Project '{name}' already exists (ID: {existing.id})", err=True)
        return
    
    project = Project(name=name, description=description)
    project_id = storage.add_project(project)
    click.echo(f"✓ Created project '{name}' (ID: {project_id})")


@project.command('list')
def list_projects():
    """List all projects"""
    storage = get_storage()
    projects = storage.list_projects()
    
    if not projects:
        click.echo("No projects found.")
        return
    
    click.echo(f"\n📁 Projects ({len(projects)} total)\n")
    click.echo("=" * 80)
    
    for proj in projects:
        click.echo(f"\n[{proj.id}] {proj.name}")
        if proj.description:
            click.echo(f"    {proj.description}")
        click.echo(f"    Created: {proj.created_at.strftime('%Y-%m-%d')}")


@main.group()
def alpha():
    """Web3 alpha brief commands"""
    pass


@alpha.command('brief')
@click.option('--output', '-o', help='Output file path (default: stdout)')
@click.option('--email-label', default='📊', help='Gmail label to search for (default: 📊)')
def generate_alpha_brief(output: str, email_label: str):
    """Generate daily alpha brief from emails and on-chain data"""
    storage = get_storage()
    generator = AlphaBriefGenerator(storage)
    formatter = BriefFormatter()
    
    # Generate brief
    click.echo("Generating alpha brief...", err=True)
    brief = generator.generate_brief(email_source=email_label)
    
    # Format and output
    markdown = formatter.format_brief(brief)
    
    if output:
        output_path = Path(output)
        output_path.write_text(markdown, encoding='utf-8')
        click.echo(f"✓ Brief saved to {output}")
    else:
        click.echo(markdown)
    
    click.echo(f"\n✓ Brief generated with {len(brief.early_signals)} early signals, "
               f"{len(brief.conflicting_views)} conflicting views, "
               f"{len(brief.action_items)} action items, "
               f"{len(brief.blind_spots)} blind spots", err=True)


@alpha.command('actions')
@click.option('--status', help='Filter by status (pending/in_progress/completed)')
@click.option('--urgency', help='Filter by urgency (high/medium/low)')
def list_action_items(status: str, urgency: str):
    """List action items from alpha briefs"""
    storage = get_storage()
    formatter = BriefFormatter()
    
    action_items = storage.get_action_items(status=status, urgency=urgency)
    
    if not action_items:
        click.echo("No action items found.")
        return
    
    click.echo(f"\n✅ Action Items ({len(action_items)} total)\n")
    click.echo("=" * 80)
    click.echo(formatter.format_action_items_table(action_items))


@main.group()
def import_data():
    """Import data from files"""
    pass


@import_data.command('trading-performance')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--project', '-p', help='Associate with project name')
def import_trading_performance(file_path: str, project: str):
    """Import trading performance CSV"""
    storage = get_storage()
    
    try:
        importer = TradingPerformanceImporter(file_path)
        
        if not importer.validate():
            click.echo("Error: Invalid file format", err=True)
            return
        
        click.echo("Parsing trading data...", err=True)
        data = importer.parse()
        
        # Get or create project
        project_id = None
        if project:
            proj = storage.get_project_by_name(project)
            if not proj:
                click.echo(f"Creating project '{project}'...", err=True)
                proj_model = Project(name=project)
                project_id = storage.add_project(proj_model)
            else:
                project_id = proj.id
        
        # Store trades
        click.echo(f"Storing {len(data['trades'])} trades...", err=True)
        count = storage.add_trades_batch(data['trades'], project_id=project_id)
        
        click.echo(f"\n✓ Imported {count} trades")
        click.echo(f"\n📊 Metrics:")
        metrics = data['metrics']
        if metrics:
            click.echo(f"   Total PnL: ${metrics.get('total_pnl', 0):.2f}")
            click.echo(f"   Win Rate: {metrics.get('win_rate', 0):.1f}%")
            click.echo(f"   Avg Return: {metrics.get('avg_return_pct', 0):.2f}%")
            if 'sharpe_ratio' in metrics:
                click.echo(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        import traceback
        traceback.print_exc()


@main.group()
def improvements():
    """Improvement tracking commands"""
    pass


@improvements.command('add')
@click.argument('project_name')
@click.option('--template', '-t', required=True,
              type=click.Choice(['interactive_viz', 'benchmark', 'monetization', 'video', 'open_source']),
              help='Improvement template type')
@click.option('--notes', '-n', help='Notes about this improvement')
def add_improvement(project_name: str, template: str, notes: str):
    """Add an improvement to a project"""
    storage = get_storage()
    
    # Find project
    project = storage.get_project_by_name(project_name)
    if not project:
        click.echo(f"Error: Project '{project_name}' not found", err=True)
        click.echo("Create it first with: nc project create <name>", err=True)
        return
    
    from ..core.models import Improvement, ImprovementType
    
    improvement = Improvement(
        project_id=project.id,
        improvement_type=ImprovementType(template),
        notes=notes
    )
    
    improvement_id = storage.add_improvement(improvement)
    click.echo(f"✓ Added {template} improvement to '{project_name}' (ID: {improvement_id})")


@improvements.command('list')
@click.option('--project', '-p', help='Filter by project name')
def list_improvements(project: str):
    """List improvements"""
    storage = get_storage()
    
    if project:
        proj = storage.get_project_by_name(project)
        if not proj:
            click.echo(f"Error: Project '{project}' not found", err=True)
            return
        improvements = storage.get_improvements(project_id=proj.id)
    else:
        improvements = storage.get_improvements()
    
    if not improvements:
        click.echo("No improvements found.")
        return
    
    click.echo(f"\n🔧 Improvements ({len(improvements)} total)\n")
    click.echo("=" * 80)
    
    template_names = {
        'interactive_viz': 'Interactive Visualization',
        'benchmark': 'Benchmark Comparison',
        'monetization': 'Skills Monetization',
        'video': 'Video Walkthrough',
        'open_source': 'Open Source Playbook'
    }
    
    status_icons = {
        'pending': '⏳',
        'in_progress': '🔄',
        'completed': '✅'
    }
    
    for imp in improvements:
        project = storage.get_project(imp.project_id)
        proj_name = project.name if project else f"Project {imp.project_id}"
        
        template_name = template_names.get(imp.improvement_type.value, imp.improvement_type.value)
        status_icon = status_icons.get(imp.status.value, '•')
        
        click.echo(f"\n{status_icon} [{imp.id}] {template_name}")
        click.echo(f"   Project: {proj_name}")
        click.echo(f"   Status: {imp.status.value}")
        if imp.notes:
            click.echo(f"   Notes: {imp.notes}")
        click.echo(f"   Created: {imp.created_at.strftime('%Y-%m-%d')}")


@improvements.command('update')
@click.argument('improvement_id', type=int)
@click.option('--status', '-s', type=click.Choice(['pending', 'in_progress', 'completed']),
              help='Update status')
@click.option('--notes', '-n', help='Update notes')
def update_improvement(improvement_id: int, status: str, notes: str):
    """Update an improvement"""
    storage = get_storage()
    
    from ..core.models import ImprovementStatus
    
    status_enum = None
    if status:
        status_enum = ImprovementStatus(status)
    
    updated = storage.update_improvement(
        improvement_id=improvement_id,
        status=status_enum,
        notes=notes
    )
    
    if updated:
        click.echo(f"✓ Updated improvement {improvement_id}")
    else:
        click.echo(f"Error: Improvement {improvement_id} not found or no changes made", err=True)


@improvements.command('guide')
@click.option('--template', '-t', required=True,
              type=click.Choice(['interactive_viz', 'benchmark', 'monetization', 'video', 'open_source']),
              help='Improvement template type')
def show_improvement_guide(template: str):
    """Show guidance for an improvement template"""
    from ..core.models import ImprovementType
    
    template_type = ImprovementType(template)
    template_def = get_template(template_type)
    
    if not template_def:
        click.echo(f"Error: Template '{template}' not found", err=True)
        return
    
    click.echo(f"\n📋 {template_def.name}\n")
    click.echo("=" * 80)
    click.echo(f"\n{template_def.description}\n")
    
    click.echo("✅ Checklist:")
    for i, item in enumerate(template_def.checklist, 1):
        click.echo(f"   {i}. {item}")
    
    click.echo("\n💡 Examples:")
    for example in template_def.examples:
        click.echo(f"   • {example}")
    
    click.echo("\n🛠️  Tools Needed:")
    for tool in template_def.tools_needed:
        click.echo(f"   • {tool}")
    click.echo("")


@main.group()
def generate():
    """Generate outputs (PDF, Twitter, LinkedIn, etc.)"""
    pass


@generate.command('pdf')
@click.argument('project_name')
@click.option('--output', '-o', required=True, help='Output PDF file path')
def generate_pdf(project_name: str, output: str):
    """Generate PDF report for a project"""
    storage = get_storage()
    
    project = storage.get_project_by_name(project_name)
    if not project:
        click.echo(f"Error: Project '{project_name}' not found", err=True)
        return
    
    try:
        generator = PDFReportGenerator(storage)
        output_path = Path(output)
        generator.generate_pdf(project, output_path)
        click.echo(f"✓ PDF generated: {output_path}")
    except ImportError as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("Install reportlab with: pip install reportlab", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@generate.command('twitter')
@click.argument('project_name')
@click.option('--output', '-o', help='Output file path (default: stdout)')
@click.option('--benchmarks/--no-benchmarks', default=True, help='Include benchmarks')
@click.option('--monetization/--no-monetization', default=True, help='Include monetization')
def generate_twitter(project_name: str, output: str, benchmarks: bool, monetization: bool):
    """Generate Twitter thread for a project"""
    storage = get_storage()
    
    project = storage.get_project_by_name(project_name)
    if not project:
        click.echo(f"Error: Project '{project_name}' not found", err=True)
        return
    
    generator = TwitterThreadGenerator(storage)
    thread = generator.generate_thread(project, include_benchmarks=benchmarks, include_monetization=monetization)
    
    if output:
        output_path = Path(output)
        output_path.write_text(thread, encoding='utf-8')
        click.echo(f"✓ Twitter thread saved to {output_path}")
    else:
        click.echo(thread)


@generate.command('linkedin')
@click.argument('project_name')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def generate_linkedin(project_name: str, output: str):
    """Generate LinkedIn post for a project"""
    storage = get_storage()
    
    project = storage.get_project_by_name(project_name)
    if not project:
        click.echo(f"Error: Project '{project_name}' not found", err=True)
        return
    
    generator = LinkedInPostGenerator(storage)
    post = generator.generate_post(project)
    
    if output:
        output_path = Path(output)
        output_path.write_text(post, encoding='utf-8')
        click.echo(f"✓ LinkedIn post saved to {output_path}")
    else:
        click.echo(post)


@generate.command('video-script')
@click.argument('project_name')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def generate_video_script(project_name: str, output: str):
    """Generate 90-second video script for a project"""
    storage = get_storage()
    
    project = storage.get_project_by_name(project_name)
    if not project:
        click.echo(f"Error: Project '{project_name}' not found", err=True)
        return
    
    generator = VideoScriptGenerator(storage)
    script = generator.generate_script(project)
    
    if output:
        output_path = Path(output)
        output_path.write_text(script, encoding='utf-8')
        click.echo(f"✓ Video script saved to {output_path}")
    else:
        click.echo(script)


if __name__ == '__main__':
    main()

