"""Core data models using Pydantic for validation"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class EntryType(str, Enum):
    """Types of entries that can be logged"""
    TRADE = "trade"
    CODE = "code"
    ALPHA = "alpha"
    LEARNING = "learning"
    ACTION = "action"
    NOTE = "note"
    OPPORTUNITY = "opportunity"
    RISK = "risk"  # Any risk-taking activity


class Entry(BaseModel):
    """Daily entry model"""
    id: Optional[int] = None
    entry_type: EntryType
    timestamp: datetime = Field(default_factory=datetime.now)
    notes: str
    tags: list[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    source: str = "manual"  # manual, auto, sync


class Project(BaseModel):
    """Project model for aggregated work"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ImprovementStatus(str, Enum):
    """Improvement status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ImprovementType(str, Enum):
    """Types of improvements"""
    INTERACTIVE_VIZ = "interactive_viz"
    BENCHMARK = "benchmark"
    MONETIZATION = "monetization"
    VIDEO = "video"
    OPEN_SOURCE = "open_source"


class Improvement(BaseModel):
    """Improvement tracking model"""
    id: Optional[int] = None
    project_id: int
    improvement_type: ImprovementType
    status: ImprovementStatus = ImprovementStatus.PENDING
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlphaSignal(BaseModel):
    """Alpha signal extracted from sources"""
    id: Optional[int] = None
    signal_type: str  # early_signal, conflicting_view, action_item, blind_spot
    content: str
    source: str  # email, telegram, onchain, etc.
    confidence: Optional[str] = None
    narrative: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ActionItem(BaseModel):
    """Action item extracted from alpha briefs"""
    id: Optional[int] = None
    task: str
    category: Optional[str] = None
    time_estimate: Optional[str] = None
    urgency: Optional[str] = None  # high, medium, low
    tools_needed: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlphaBrief(BaseModel):
    """Generated alpha brief"""
    id: Optional[int] = None
    date: datetime = Field(default_factory=datetime.now)
    early_signals: list[AlphaSignal] = Field(default_factory=list)
    conflicting_views: list[AlphaSignal] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    blind_spots: list[AlphaSignal] = Field(default_factory=list)
    sources_used: list[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Skill(BaseModel):
    """Skill model"""
    id: Optional[int] = None
    name: str
    category: Optional[str] = None  # e.g., 'programming', 'trading', 'research'
    first_seen: datetime = Field(default_factory=datetime.now)
    last_used: datetime = Field(default_factory=datetime.now)
    proficiency_level: Optional[str] = None  # beginner, intermediate, advanced, expert
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Opportunity(BaseModel):
    """Monetization opportunity"""
    id: Optional[int] = None
    title: str
    opportunity_type: str  # job, consulting, content, product, other
    description: Optional[str] = None
    value: Optional[float] = None  # Estimated value/revenue
    currency: str = "USD"
    required_skills: list[str] = Field(default_factory=list)
    status: str = "open"  # open, applied, in_progress, completed, closed
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MonetizationPath(BaseModel):
    """Path to monetize a skill"""
    id: Optional[int] = None
    skill_name: str
    path_type: str  # consulting, saas, content, course, etc.
    description: str
    target_revenue: Optional[float] = None
    revenue_model: Optional[str] = None  # e.g., "$49/mo", "$150/hr"
    status: str = "pending"  # pending, in_progress, active, completed
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RiskEntry(BaseModel):
    """Structured risk-taking activity with comprehensive tracking"""
    risk_type: str  # nft, sports_bet, prediction_market, trade, crypto, other
    entry_cost: float  # Amount at risk
    currency: str = "USD"
    
    # Reward/value tracking
    initial_expected_value: Optional[float] = None  # Initial expected upside/outcome value
    current_expected_value: Optional[float] = None  # Current expected value (may change over time)
    expected_timeframe: Optional[str] = None  # e.g., "2 weeks", "end of game", "30 days"
    confidence_level: Optional[float] = None  # 0.0-1.0 probability/confidence in expected value
    
    # Opportunity cost
    opportunity_cost_perceived: Optional[float] = None  # What you think you're giving up
    opportunity_cost_real: Optional[float] = None  # Actual opportunity cost (can update over time)
    opportunity_cost_notes: Optional[str] = None  # What opportunities are being passed up
    
    # Risk metrics
    odds_or_price: Optional[float] = None  # Current odds (e.g., 3.21) or entry price
    fair_value: Optional[float] = None  # Your assessment of fair value (e.g., 2.0 for "evens")
    max_loss: Optional[float] = None  # Worst case scenario loss
    max_gain: Optional[float] = None  # Best case scenario gain
    risk_factors: list[str] = Field(default_factory=list)  # e.g., ["no_cash_out", "illiquidity", "timing_risk"]
    
    # Liquidity and exit
    exit_strategy: Optional[str] = None
    liquidity_rating: Optional[str] = None  # high, medium, low, locked
    time_to_exit: Optional[str] = None  # How long to exit if needed
    
    # Diversification and correlation
    portfolio_allocation_pct: Optional[float] = None  # % of total risk capital
    correlated_risks: list[str] = Field(default_factory=list)  # Related risk entry IDs or descriptions
    
    # Information and edge
    information_edge: Optional[str] = None  # public, private, research, insider
    time_invested_hours: Optional[float] = None  # Time spent researching/monitoring
    
    # Status and outcomes
    status: str = "open"  # open, closed, realized, written_off
    realized_value: Optional[float] = None  # Actual outcome when closed
    reward_history: list[Dict[str, Any]] = Field(default_factory=list)  # Track reward changes over time
    opportunity_cost_history: list[Dict[str, Any]] = Field(default_factory=list)  # Track opportunity cost changes
    
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RewardUpdate(BaseModel):
    """Single reward/value update for a risk entry"""
    timestamp: datetime = Field(default_factory=datetime.now)
    expected_value: float
    notes: Optional[str] = None
    reason: Optional[str] = None  # Why the reward changed
    confidence_level: Optional[float] = None  # Updated confidence if available
    metadata: Dict[str, Any] = Field(default_factory=dict)
