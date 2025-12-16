# API Overview

**Quick reference:** What's available for programmatic access (Python API)

---

## Core API

### Storage Class (`src.core.storage.Storage`)

**Primary interface for all data operations.**

```python
from src.core.storage import Storage

storage = Storage()  # Uses default: data/nobody_cares.db
# Or: Storage(db_path=Path("custom.db"))
```

**Entry Operations:**

- `add_entry(entry: Entry) -> Entry` - Create new entry
- `get_entries(entry_type: Optional[EntryType] = None, limit: int = 100, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Entry]` - Query entries
- `get_entry(entry_id: int) -> Optional[Entry]` - Get single entry
- `update_entry(entry: Entry) -> Entry` - Update existing entry
- `delete_entry(entry_id: int) -> bool` - Delete entry

**Project Operations:**

- `add_project(project: Project) -> Project`
- `get_projects() -> List[Project]`
- `get_project(project_id: int) -> Optional[Project]`
- `update_project(project: Project) -> Project`

**Risk Entry Operations:**

- All risk entries stored as `Entry` with `entry_type=EntryType.RISK`
- Risk data stored in `entry.metadata` dict
- Use standard entry operations above

---

## Models (`src.core.models`)

**Data structures (Pydantic models):**

- `Entry` - Base entry model
- `RiskEntry` - Risk entry model (extends Entry via metadata)
- `Project` - Project model
- `Improvement` - Improvement tracking
- `AlphaSignal` - Alpha signal
- `AlphaBrief` - Alpha brief
- `Skill` - Skill definition
- `Opportunity` - Monetization opportunity
- `EntryType` - Enum for entry types
- `OwnershipType` - Enum for ownership (mine/influenced/performed)

**Usage:**

```python
from src.core.models import Entry, EntryType, RiskEntry

entry = Entry(
    entry_type=EntryType.RISK,
    notes="My bet",
    metadata={"entry_cost": 100, "currency": "USD"}
)
```

---

## Feature Modules

### Pattern Detection (`src.insights.patterns`)

```python
from src.insights import (
    detect_misalignment_patterns,
    detect_drift_patterns,
    analyze_ownership_correlation
)

storage = Storage()
misalignment = detect_misalignment_patterns(storage, days=90)
drift = detect_drift_patterns(storage, days=90)
ownership = analyze_ownership_correlation(storage, days=90)
```

### Content Generation (`src.outputs.content`)

```python
from src.outputs import ContentGenerator

storage = Storage()
generator = ContentGenerator(storage)

entry = storage.get_entry(entry_id=1)
twitter_thread = generator.generate_twitter(entry, brevity='medium')
linkedin_post = generator.generate_linkedin(entry)
blog_post = generator.generate_blog(entry)
lessons = generator.extract_lessons(entry)
```

### Review & Adaptation (`src.review.prompts`)

```python
from src.review import get_review_prompts, suggest_iterations

storage = Storage()
prompts = get_review_prompts(storage)
suggestions = suggest_iterations(storage)
```

### Examples Library (`src.examples.library`)

```python
from src.examples import EXAMPLES, TEMPLATES, get_example, get_template

example = get_example('sports-bet-quick')
template = get_template('value-bet')
```

### Currency Utilities (`src.core.currency`)

```python
from src.core.currency import format_cost, get_last_used_currency

formatted = format_cost(100.5, "USD")  # "$100.50"
last_currency = get_last_used_currency(storage)  # "USD"
```

### Alpha Brief Generator (`src.alpha`)

```python
from src.alpha import AlphaBriefGenerator

storage = Storage()
generator = AlphaBriefGenerator(storage)
brief = generator.generate_brief(email_source="...")
```

### Importers (`src.importers`)

```python
from src.importers import TradingPerformanceImporter

importer = TradingPerformanceImporter(storage)
importer.import_from_csv("trades.csv")
```

---

## Complete API List

### Core

- `Storage` class - All database operations
- `Entry`, `RiskEntry`, `Project`, etc. - Data models
- `EntryType`, `OwnershipType` - Enums

### Insights

- `detect_misalignment_patterns(storage, days)` - Misalignment analysis
- `detect_drift_patterns(storage, days)` - Drift analysis
- `analyze_ownership_correlation(storage, days)` - Ownership vs outcomes

### Outputs

- `ContentGenerator` class - Content generation
- `TwitterThreadGenerator` class - Twitter threads
- `LinkedInPostGenerator` class - LinkedIn posts
- `VideoScriptGenerator` class - Video scripts
- `PDFReportGenerator` class - PDF reports

### Review

- `get_review_prompts(storage)` - Review prompts
- `suggest_iterations(storage)` - System adaptation suggestions

### Examples

- `EXAMPLES` dict - Predefined examples
- `TEMPLATES` dict - Command templates
- `get_example(id)` - Get example by ID
- `get_template(id)` - Get template by ID
- `get_contrast(storage, entry_id)` - Compare entry to examples

### Utilities

- `format_cost(cost, currency)` - Format currency
- `get_last_used_currency(storage)` - Get last currency
- `get_week_start(date)`, `get_week_end(date)` - Date utilities

---

## Usage Pattern

**Typical workflow:**

```python
from src.core.storage import Storage
from src.core.models import Entry, EntryType
from src.insights import detect_misalignment_patterns
from src.outputs import ContentGenerator

# Initialize
storage = Storage()

# Create entry
entry = Entry(
    entry_type=EntryType.RISK,
    notes="My bet",
    metadata={"entry_cost": 100, "currency": "USD"}
)
entry = storage.add_entry(entry)

# Query
entries = storage.get_entries(entry_type=EntryType.RISK, limit=10)

# Analyze
patterns = detect_misalignment_patterns(storage, days=90)

# Generate content
generator = ContentGenerator(storage)
content = generator.generate_twitter(entry)
```

---

## Notes

- **No REST API** - This is a Python library, not a web service
- **Local only** - All operations are local (SQLite database)
- **CLI is primary** - Most users interact via `nc` commands
- **Python API available** - For programmatic access or scripting

---

**Last Updated:** Current
