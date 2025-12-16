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
