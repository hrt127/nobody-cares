"""SQLite database storage layer"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import (
    Entry, EntryType, Project, Improvement, ImprovementType, ImprovementStatus,
    AlphaSignal, ActionItem, AlphaBrief, Skill, Opportunity, MonetizationPath
)


class Storage:
    """SQLite storage manager"""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            # Default to data/ directory in project root
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / "nobody_cares.db"
        
        self.db_path = Path(db_path)
        self._init_db()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_type TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    notes TEXT NOT NULL,
                    tags TEXT,  -- JSON array
                    metadata TEXT,  -- JSON object
                    source TEXT DEFAULT 'manual',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    metadata TEXT,  -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Improvements table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS improvements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    improvement_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    notes TEXT,
                    metadata TEXT,  -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            """)
            
            # Alpha signals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alpha_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    confidence TEXT,
                    narrative TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Action items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    category TEXT,
                    time_estimate TEXT,
                    urgency TEXT,
                    tools_needed TEXT,
                    status TEXT DEFAULT 'pending',
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Alpha briefs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alpha_briefs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP NOT NULL,
                    sources_used TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Brief signals link table (many-to-many)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS brief_signals (
                    brief_id INTEGER NOT NULL,
                    signal_id INTEGER NOT NULL,
                    FOREIGN KEY (brief_id) REFERENCES alpha_briefs (id),
                    FOREIGN KEY (signal_id) REFERENCES alpha_signals (id),
                    PRIMARY KEY (brief_id, signal_id)
                )
            """)
            
            # Brief action items link table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS brief_action_items (
                    brief_id INTEGER NOT NULL,
                    action_item_id INTEGER NOT NULL,
                    FOREIGN KEY (brief_id) REFERENCES alpha_briefs (id),
                    FOREIGN KEY (action_item_id) REFERENCES action_items (id),
                    PRIMARY KEY (brief_id, action_item_id)
                )
            """)
            
            # Trades table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    entry_date TIMESTAMP NOT NULL,
                    exit_date TIMESTAMP,
                    symbol TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    quantity REAL NOT NULL,
                    pnl REAL,
                    return_pct REAL,
                    strategy TEXT,
                    setup_type TEXT,
                    notes TEXT,
                    fees REAL,
                    duration_days INTEGER,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_entries_timestamp ON entries(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_entries_type ON entries(entry_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_improvements_project ON improvements(project_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alpha_signals_type ON alpha_signals(signal_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alpha_signals_source ON alpha_signals(source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_action_items_status ON action_items(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_action_items_urgency ON action_items(urgency)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_project ON trades(project_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_entry_date ON trades(entry_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_strategy ON trades(strategy)")
            
            # Skills table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    proficiency_level TEXT,
                    metadata TEXT
                )
            """)
            
            # Opportunities table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    opportunity_type TEXT NOT NULL,
                    description TEXT,
                    value REAL,
                    currency TEXT DEFAULT 'USD',
                    required_skills TEXT,
                    status TEXT DEFAULT 'open',
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Monetization paths table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monetization_paths (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    path_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    target_revenue REAL,
                    revenue_model TEXT,
                    status TEXT DEFAULT 'pending',
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Skill entry links (many-to-many)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_entries (
                    skill_id INTEGER NOT NULL,
                    entry_id INTEGER NOT NULL,
                    FOREIGN KEY (skill_id) REFERENCES skills (id),
                    FOREIGN KEY (entry_id) REFERENCES entries (id),
                    PRIMARY KEY (skill_id, entry_id)
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_opportunities_type ON opportunities(opportunity_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_monetization_skill ON monetization_paths(skill_name)")
    
    def add_entry(self, entry: Entry) -> int:
        """Add a new entry and return its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO entries (entry_type, timestamp, notes, tags, metadata, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry.entry_type.value,
                entry.timestamp,
                entry.notes,
                json.dumps(entry.tags),
                json.dumps(entry.metadata),
                entry.source
            ))
            return cursor.lastrowid
    
    def get_entries(
        self,
        entry_type: Optional[EntryType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> List[Entry]:
        """Query entries with filters"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM entries WHERE 1=1"
            params = []
            
            if entry_type:
                query += " AND entry_type = ?"
                params.append(entry_type.value)
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)
            
            if tags:
                # SQLite JSON filtering is limited, so we'll filter in Python
                # This is a simple approach - could be optimized
                pass
            
            query += " ORDER BY timestamp DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            entries = []
            for row in rows:
                entry_dict = dict(row)
                # Filter by tags in Python if specified
                if tags:
                    entry_tags = json.loads(entry_dict.get('tags', '[]'))
                    if not any(tag in entry_tags for tag in tags):
                        continue
                
                entries.append(Entry(
                    id=entry_dict['id'],
                    entry_type=EntryType(entry_dict['entry_type']),
                    timestamp=datetime.fromisoformat(entry_dict['timestamp']) if isinstance(entry_dict['timestamp'], str) else entry_dict['timestamp'],
                    notes=entry_dict['notes'],
                    tags=json.loads(entry_dict.get('tags', '[]')),
                    metadata=json.loads(entry_dict.get('metadata', '{}')),
                    source=entry_dict.get('source', 'manual')
                ))
            
            return entries
    
    def add_project(self, project: Project) -> int:
        """Add a new project and return its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (name, description, metadata)
                VALUES (?, ?, ?)
            """, (
                project.name,
                project.description,
                json.dumps(project.metadata)
            ))
            return cursor.lastrowid
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            
            if row:
                row_dict = dict(row)
                return Project(
                    id=row_dict['id'],
                    name=row_dict['name'],
                    description=row_dict['description'],
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    updated_at=datetime.fromisoformat(row_dict['updated_at']) if isinstance(row_dict['updated_at'], str) else row_dict['updated_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                )
            return None
    
    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE name = ?", (name,))
            row = cursor.fetchone()
            
            if row:
                row_dict = dict(row)
                return Project(
                    id=row_dict['id'],
                    name=row_dict['name'],
                    description=row_dict['description'],
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    updated_at=datetime.fromisoformat(row_dict['updated_at']) if isinstance(row_dict['updated_at'], str) else row_dict['updated_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                )
            return None
    
    def list_projects(self) -> List[Project]:
        """List all projects"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                row_dict = dict(row)
                projects.append(Project(
                    id=row_dict['id'],
                    name=row_dict['name'],
                    description=row_dict['description'],
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    updated_at=datetime.fromisoformat(row_dict['updated_at']) if isinstance(row_dict['updated_at'], str) else row_dict['updated_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                ))
            return projects
    
    def add_improvement(self, improvement: Improvement) -> int:
        """Add a new improvement and return its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO improvements (project_id, improvement_type, status, notes, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                improvement.project_id,
                improvement.improvement_type.value,
                improvement.status.value,
                improvement.notes,
                json.dumps(improvement.metadata)
            ))
            return cursor.lastrowid
    
    def get_improvements(self, project_id: Optional[int] = None) -> List[Improvement]:
        """Get improvements, optionally filtered by project"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if project_id:
                cursor.execute("SELECT * FROM improvements WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
            else:
                cursor.execute("SELECT * FROM improvements ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            
            improvements = []
            for row in rows:
                row_dict = dict(row)
                improvements.append(Improvement(
                    id=row_dict['id'],
                    project_id=row_dict['project_id'],
                    improvement_type=ImprovementType(row_dict['improvement_type']),
                    status=ImprovementStatus(row_dict['status']),
                    notes=row_dict['notes'],
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    updated_at=datetime.fromisoformat(row_dict['updated_at']) if isinstance(row_dict['updated_at'], str) else row_dict['updated_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                ))
            return improvements
    
    def update_improvement(
        self,
        improvement_id: int,
        status: Optional[ImprovementStatus] = None,
        notes: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update an improvement"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if status is not None:
                updates.append("status = ?")
                params.append(status.value)
            
            if notes is not None:
                updates.append("notes = ?")
                params.append(notes)
            
            if metadata is not None:
                updates.append("metadata = ?")
                params.append(json.dumps(metadata))
            
            if not updates:
                return False
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(improvement_id)
            
            query = f"UPDATE improvements SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            return cursor.rowcount > 0
    
    def add_alpha_signal(self, signal: AlphaSignal) -> int:
        """Add an alpha signal and return its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alpha_signals (signal_type, content, source, confidence, narrative, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                signal.signal_type,
                signal.content,
                signal.source,
                signal.confidence,
                signal.narrative,
                json.dumps(signal.metadata)
            ))
            return cursor.lastrowid
    
    def add_action_item(self, action_item: ActionItem) -> int:
        """Add an action item and return its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO action_items (task, category, time_estimate, urgency, tools_needed, status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                action_item.task,
                action_item.category,
                action_item.time_estimate,
                action_item.urgency,
                action_item.tools_needed,
                action_item.status,
                json.dumps(action_item.metadata)
            ))
            return cursor.lastrowid
    
    def add_alpha_brief(
        self,
        brief: AlphaBrief,
        signal_ids: List[int],
        action_item_ids: List[int]
    ) -> int:
        """Add an alpha brief with linked signals and action items"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert brief
            cursor.execute("""
                INSERT INTO alpha_briefs (date, sources_used, metadata)
                VALUES (?, ?, ?)
            """, (
                brief.date,
                json.dumps(brief.sources_used),
                json.dumps(brief.metadata)
            ))
            brief_id = cursor.lastrowid
            
            # Link signals
            for signal_id in signal_ids:
                cursor.execute("""
                    INSERT INTO brief_signals (brief_id, signal_id)
                    VALUES (?, ?)
                """, (brief_id, signal_id))
            
            # Link action items
            for action_id in action_item_ids:
                cursor.execute("""
                    INSERT INTO brief_action_items (brief_id, action_item_id)
                    VALUES (?, ?)
                """, (brief_id, action_id))
            
            return brief_id
    
    def get_latest_brief(self) -> Optional[AlphaBrief]:
        """Get the most recent alpha brief"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alpha_briefs ORDER BY date DESC LIMIT 1")
            row = cursor.fetchone()
            
            if not row:
                return None
            
            row_dict = dict(row)
            brief_id = row_dict['id']
            
            # Get linked signals
            cursor.execute("""
                SELECT s.* FROM alpha_signals s
                INNER JOIN brief_signals bs ON s.id = bs.signal_id
                WHERE bs.brief_id = ?
            """, (brief_id,))
            signal_rows = cursor.fetchall()
            
            signals = []
            for sig_row in signal_rows:
                sig_dict = dict(sig_row)
                signals.append(AlphaSignal(
                    id=sig_dict['id'],
                    signal_type=sig_dict['signal_type'],
                    content=sig_dict['content'],
                    source=sig_dict['source'],
                    confidence=sig_dict.get('confidence'),
                    narrative=sig_dict.get('narrative'),
                    created_at=datetime.fromisoformat(sig_dict['created_at']) if isinstance(sig_dict['created_at'], str) else sig_dict['created_at'],
                    metadata=json.loads(sig_dict.get('metadata', '{}'))
                ))
            
            # Get linked action items
            cursor.execute("""
                SELECT a.* FROM action_items a
                INNER JOIN brief_action_items ba ON a.id = ba.action_item_id
                WHERE ba.brief_id = ?
            """, (brief_id,))
            action_rows = cursor.fetchall()
            
            action_items = []
            for act_row in action_rows:
                act_dict = dict(act_row)
                action_items.append(ActionItem(
                    id=act_dict['id'],
                    task=act_dict['task'],
                    category=act_dict.get('category'),
                    time_estimate=act_dict.get('time_estimate'),
                    urgency=act_dict.get('urgency'),
                    tools_needed=act_dict.get('tools_needed'),
                    status=act_dict.get('status', 'pending'),
                    created_at=datetime.fromisoformat(act_dict['created_at']) if isinstance(act_dict['created_at'], str) else act_dict['created_at'],
                    metadata=json.loads(act_dict.get('metadata', '{}'))
                ))
            
            # Separate signals by type
            early_signals = [s for s in signals if s.signal_type == 'early_signal']
            conflicting = [s for s in signals if s.signal_type == 'conflicting_view']
            blind_spots = [s for s in signals if s.signal_type == 'blind_spot']
            
            return AlphaBrief(
                id=brief_id,
                date=datetime.fromisoformat(row_dict['date']) if isinstance(row_dict['date'], str) else row_dict['date'],
                early_signals=early_signals,
                conflicting_views=conflicting,
                action_items=action_items,
                blind_spots=blind_spots,
                sources_used=json.loads(row_dict.get('sources_used', '[]')),
                metadata=json.loads(row_dict.get('metadata', '{}'))
            )
    
    def get_action_items(
        self,
        status: Optional[str] = None,
        urgency: Optional[str] = None
    ) -> List[ActionItem]:
        """Get action items with optional filters"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM action_items WHERE 1=1"
            params = []
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if urgency:
                query += " AND urgency = ?"
                params.append(urgency)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            action_items = []
            for row in rows:
                row_dict = dict(row)
                action_items.append(ActionItem(
                    id=row_dict['id'],
                    task=row_dict['task'],
                    category=row_dict.get('category'),
                    time_estimate=row_dict.get('time_estimate'),
                    urgency=row_dict.get('urgency'),
                    tools_needed=row_dict.get('tools_needed'),
                    status=row_dict.get('status', 'pending'),
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                ))
            return action_items
    
    def update_action_item(
        self,
        action_item_id: int,
        status: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Update an action item"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            for key, value in kwargs.items():
                if value is not None and key in ['category', 'time_estimate', 'urgency', 'tools_needed']:
                    updates.append(f"{key} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(action_item_id)
            query = f"UPDATE action_items SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            return cursor.rowcount > 0
    
    def add_trade(self, trade_data: Dict[str, Any], project_id: Optional[int] = None) -> int:
        """Add a trade record"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trades (
                    project_id, entry_date, exit_date, symbol, entry_price, exit_price,
                    quantity, pnl, return_pct, strategy, setup_type, notes, fees,
                    duration_days, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id,
                trade_data.get('entry_date'),
                trade_data.get('exit_date'),
                trade_data.get('symbol'),
                trade_data.get('entry_price'),
                trade_data.get('exit_price'),
                trade_data.get('quantity'),
                trade_data.get('pnl'),
                trade_data.get('return_pct'),
                trade_data.get('strategy'),
                trade_data.get('setup_type'),
                trade_data.get('notes'),
                trade_data.get('fees'),
                trade_data.get('duration_days'),
                json.dumps(trade_data.get('metadata', {}))
            ))
            return cursor.lastrowid
    
    def add_trades_batch(self, trades: List[Dict[str, Any]], project_id: Optional[int] = None) -> int:
        """Add multiple trades in a batch"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            count = 0
            for trade_data in trades:
                cursor.execute("""
                    INSERT INTO trades (
                        project_id, entry_date, exit_date, symbol, entry_price, exit_price,
                        quantity, pnl, return_pct, strategy, setup_type, notes, fees,
                        duration_days, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project_id,
                    trade_data.get('entry_date'),
                    trade_data.get('exit_date'),
                    trade_data.get('symbol'),
                    trade_data.get('entry_price'),
                    trade_data.get('exit_price'),
                    trade_data.get('quantity'),
                    trade_data.get('pnl'),
                    trade_data.get('return_pct'),
                    trade_data.get('strategy'),
                    trade_data.get('setup_type'),
                    trade_data.get('notes'),
                    trade_data.get('fees'),
                    trade_data.get('duration_days'),
                    json.dumps(trade_data.get('metadata', {}))
                ))
                count += 1
            return count
    
    def get_trades(
        self,
        project_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        strategy: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get trades with filters"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM trades WHERE 1=1"
            params = []
            
            if project_id:
                query += " AND project_id = ?"
                params.append(project_id)
            
            if start_date:
                query += " AND entry_date >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND entry_date <= ?"
                params.append(end_date)
            
            if strategy:
                query += " AND strategy = ?"
                params.append(strategy)
            
            query += " ORDER BY entry_date DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            trades = []
            for row in rows:
                row_dict = dict(row)
                # Parse dates and metadata
                if row_dict.get('entry_date'):
                    if isinstance(row_dict['entry_date'], str):
                        row_dict['entry_date'] = datetime.fromisoformat(row_dict['entry_date'])
                if row_dict.get('exit_date'):
                    if isinstance(row_dict['exit_date'], str):
                        row_dict['exit_date'] = datetime.fromisoformat(row_dict['exit_date'])
                row_dict['metadata'] = json.loads(row_dict.get('metadata', '{}'))
                trades.append(row_dict)
            
            return trades
    
    def add_skill(self, skill: Skill) -> int:
        """Add a skill"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO skills (name, category, first_seen, last_used, proficiency_level, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                skill.name,
                skill.category,
                skill.first_seen,
                skill.last_used,
                skill.proficiency_level,
                json.dumps(skill.metadata)
            ))
            return cursor.lastrowid
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a skill by name"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skills WHERE name = ?", (skill_name,))
            row = cursor.fetchone()
            
            if row:
                row_dict = dict(row)
                return Skill(
                    id=row_dict['id'],
                    name=row_dict['name'],
                    category=row_dict.get('category'),
                    first_seen=datetime.fromisoformat(row_dict['first_seen']) if isinstance(row_dict['first_seen'], str) else row_dict['first_seen'],
                    last_used=datetime.fromisoformat(row_dict['last_used']) if isinstance(row_dict['last_used'], str) else row_dict['last_used'],
                    proficiency_level=row_dict.get('proficiency_level'),
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                )
            return None
    
    def list_skills(self, category: Optional[str] = None) -> List[Skill]:
        """List all skills"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if category:
                cursor.execute("SELECT * FROM skills WHERE category = ? ORDER BY last_used DESC", (category,))
            else:
                cursor.execute("SELECT * FROM skills ORDER BY last_used DESC")
            
            rows = cursor.fetchall()
            skills = []
            for row in rows:
                row_dict = dict(row)
                skills.append(Skill(
                    id=row_dict['id'],
                    name=row_dict['name'],
                    category=row_dict.get('category'),
                    first_seen=datetime.fromisoformat(row_dict['first_seen']) if isinstance(row_dict['first_seen'], str) else row_dict['first_seen'],
                    last_used=datetime.fromisoformat(row_dict['last_used']) if isinstance(row_dict['last_used'], str) else row_dict['last_used'],
                    proficiency_level=row_dict.get('proficiency_level'),
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                ))
            return skills
    
    def add_opportunity(self, opportunity: Opportunity) -> int:
        """Add an opportunity"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO opportunities (title, opportunity_type, description, value, currency, required_skills, status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                opportunity.title,
                opportunity.opportunity_type,
                opportunity.description,
                opportunity.value,
                opportunity.currency,
                json.dumps(opportunity.required_skills),
                opportunity.status,
                json.dumps(opportunity.metadata)
            ))
            return cursor.lastrowid
    
    def list_opportunities(self, status: Optional[str] = None) -> List[Opportunity]:
        """List opportunities"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if status:
                cursor.execute("SELECT * FROM opportunities WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM opportunities ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            opportunities = []
            for row in rows:
                row_dict = dict(row)
                opportunities.append(Opportunity(
                    id=row_dict['id'],
                    title=row_dict['title'],
                    opportunity_type=row_dict['opportunity_type'],
                    description=row_dict.get('description'),
                    value=row_dict.get('value'),
                    currency=row_dict.get('currency', 'USD'),
                    required_skills=json.loads(row_dict.get('required_skills', '[]')),
                    status=row_dict.get('status', 'open'),
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                ))
            return opportunities
    
    def add_monetization_path(self, path: MonetizationPath) -> int:
        """Add a monetization path"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO monetization_paths (skill_name, path_type, description, target_revenue, revenue_model, status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                path.skill_name,
                path.path_type,
                path.description,
                path.target_revenue,
                path.revenue_model,
                path.status,
                json.dumps(path.metadata)
            ))
            return cursor.lastrowid
    
    def get_monetization_paths(self, skill_name: Optional[str] = None) -> List[MonetizationPath]:
        """Get monetization paths"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if skill_name:
                cursor.execute("SELECT * FROM monetization_paths WHERE skill_name = ? ORDER BY created_at DESC", (skill_name,))
            else:
                cursor.execute("SELECT * FROM monetization_paths ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            paths = []
            for row in rows:
                row_dict = dict(row)
                paths.append(MonetizationPath(
                    id=row_dict['id'],
                    skill_name=row_dict['skill_name'],
                    path_type=row_dict['path_type'],
                    description=row_dict['description'],
                    target_revenue=row_dict.get('target_revenue'),
                    revenue_model=row_dict.get('revenue_model'),
                    status=row_dict.get('status', 'pending'),
                    created_at=datetime.fromisoformat(row_dict['created_at']) if isinstance(row_dict['created_at'], str) else row_dict['created_at'],
                    metadata=json.loads(row_dict.get('metadata', '{}'))
                ))
            return paths

