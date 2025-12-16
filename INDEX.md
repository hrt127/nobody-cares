# Repository Index

**Your map to the codebase.** Know what you're looking at, how it connects, and where to extend.

**Quality Reports:** See [audited/](audited/) folder for walkthrough reports, API docs, and learning logs.

**Quality Reports:** See [audited/](audited/) folder for walkthrough reports, API docs, and learning logs.

---

## 📁 Directory Structure

```
nobody-cares/
├── src/                    # Source code (all modules here)
│   ├── cli/               # Command-line interface (entry point)
│   ├── core/              # Core models, storage, utilities (foundation)
│   ├── alpha/             # Alpha signal generation
│   ├── examples/          # Example library & templates
│   ├── importers/         # Data importers (trading, etc.)
│   ├── improvements/      # Improvement tracking templates
│   ├── insights/          # Pattern detection & analysis
│   ├── outputs/           # Content generation (Twitter, LinkedIn, etc.)
│   └── review/            # Review prompts & system adaptation
├── tests/                  # Test suite
├── data/                   # Database (auto-created: nobody_cares.db)
├── docs/                   # Extended documentation (optional)
└── audited/                # Quality reports & audits
```

---

## 🗺️ Module Map

### Core Layer (Foundation)

**`src/core/`** - Everything depends on this.

- **`models.py`** - Pydantic models (Entry, RiskEntry, Project, etc.)
  - **Boundary:** All data structures defined here
  - **Extend:** Add new models here, update existing ones
  
- **`storage.py`** - SQLite database layer
  - **Boundary:** All database operations go through Storage class
  - **Extend:** Add new query methods, new tables via `_init_db()`
  
- **`currency.py`** - Multi-currency formatting & utilities
  - **Boundary:** Currency formatting logic
  - **Extend:** Add new currency types, formatting rules
  
- **`utils.py`** - Date/time utilities, helpers
  - **Boundary:** Shared utility functions
  - **Extend:** Add new utility functions

**Data Flow:** Models → Storage → Database

---

### CLI Layer (User Interface)

**`src/cli/main.py`** - Single entry point, orchestrates everything.

- **Imports from:** All other modules
- **Boundary:** All user interaction happens here
- **Extend:** Add new commands, modify existing ones

**Data Flow:** User Input → CLI → Core/Other Modules → Storage → Database

**Key Commands:**

- `nc q` - Quick capture
- `nc risk` - Risk entry
- `nc risks` - List risks
- `nc patterns` - Pattern detection
- `nc content` - Content generation
- `nc review` - Review prompts
- `nc adapt` - System adaptation

---

### Feature Modules

#### **`src/insights/`** - Pattern Detection

- **`patterns.py`** - Misalignment, drift, ownership correlation
- **Depends on:** `core.storage`, `core.models`
- **Boundary:** Analysis queries only (read-only)
- **Extend:** Add new pattern detection functions

**Data Flow:** Storage → Patterns → Results

---

#### **`src/outputs/`** - Content Generation

- **`content.py`** - Main ContentGenerator class
- **`twitter.py`** - Twitter thread generation
- **`linkedin.py`** - LinkedIn post generation
- **`pdf.py`** - PDF report generation
- **`video_script.py`** - Video script generation
- **Depends on:** `core.storage`, `core.models`
- **Boundary:** Content generation only (read-only from storage)
- **Extend:** Add new content generators, new formats

**Data Flow:** Storage → ContentGenerator → Formatted Content

---

#### **`src/review/`** - Review & Adaptation

- **`prompts.py`** - Review prompts, field usage tracking, adaptation suggestions
- **Depends on:** `core.storage`, `core.models`
- **Boundary:** Analysis and suggestions only (read-only)
- **Extend:** Add new review prompts, new adaptation logic

**Data Flow:** Storage → Review Analysis → Suggestions

---

#### **`src/examples/`** - Examples Library

- **`library.py`** - Predefined examples and templates
- **Depends on:** `core.models` (for structure)
- **Boundary:** Static examples only
- **Extend:** Add new examples, new templates

**Data Flow:** Examples → CLI (display only)

---

#### **`src/alpha/`** - Alpha Signal Generation

- **`brief_generator.py`** - Generates alpha briefs from emails/on-chain
- **`formatter.py`** - Formats briefs for display
- **Depends on:** `core.storage`, `core.models`
- **Boundary:** Alpha signal processing
- **Extend:** Add new signal sources, new extraction logic

**Data Flow:** Sources → BriefGenerator → Storage

---

#### **`src/importers/`** - Data Importers

- **`base.py`** - Base importer class
- **`trading_performance.py`** - Trading data importer
- **Depends on:** `core.storage`, `core.models`
- **Boundary:** External data → Internal format
- **Extend:** Add new importers (inherit from BaseImporter)

**Data Flow:** External Data → Importer → Storage

---

#### **`src/improvements/`** - Improvement Tracking

- **`templates.py`** - Improvement templates
- **Depends on:** `core.models`
- **Boundary:** Template definitions only
- **Extend:** Add new templates

**Data Flow:** Templates → CLI (display only)

---

## 🔄 Data Flow Diagram

```
User Input
    ↓
CLI (main.py)
    ↓
    ├─→ Core (models, storage) ──→ Database
    ├─→ Insights (patterns) ──→ Analysis Results
    ├─→ Outputs (content) ──→ Generated Content
    ├─→ Review (prompts) ──→ Suggestions
    ├─→ Examples (library) ──→ Display Examples
    ├─→ Alpha (brief_generator) ──→ Alpha Briefs
    └─→ Importers (trading) ──→ Imported Data
```

---

## 🎯 Extension Points

### Where to Add New Features

#### 1. **New Data Type**

**Add to:** `src/core/models.py`

- Create new Pydantic model
- Add to `EntryType` enum if needed
- Update `Storage._init_db()` for new table

**Example:** Adding a new "experiment" entry type

#### 2. **New CLI Command**

**Add to:** `src/cli/main.py`

- Add `@main.command()` decorator
- Import needed modules
- Use `Storage` for data access

**Example:** `nc experiments` command

#### 3. **New Pattern Detection**

**Add to:** `src/insights/patterns.py`

- Add new function (e.g., `detect_X_patterns()`)
- Export in `src/insights/__init__.py`
- Add CLI command in `main.py`

**Example:** `nc patterns experiments`

#### 4. **New Content Format**

**Add to:** `src/outputs/`

- Create new file (e.g., `blog.py`)
- Implement generator class
- Export in `src/outputs/__init__.py`
- Add to `ContentGenerator` or create new class

**Example:** Blog post generator

#### 5. **New Importer**

**Add to:** `src/importers/`

- Create new file (e.g., `crypto_import.py`)
- Inherit from `BaseImporter`
- Implement `import_data()` method
- Add CLI command in `main.py`

**Example:** Crypto exchange importer

---

## 📚 Documentation Map

### Getting Started

- **`QUICKSTART.md`** - 5-minute getting started
- **`WHEN_TO_LOG.md`** - Practical checklist & examples

### Usage Guides

- **`DAILY_GUIDE.md`** - Deep workflows & best practices
- **`README.md`** - Overview & feature list

### Change Documentation (in docs/)

- **`docs/MAJOR_SHIFTS.md`** - Detailed explanation of major changes
- **`docs/SHIFTS_SUMMARY.md`** - Quick reference for changes
- **`docs/CHANGES_SUMMARY.md`** - Technical summary

### Extended Documentation

- **`docs/`** - Additional technical documentation (architecture, deep dives)

### This Document

- **`INDEX.md`** - Repository structure & extension points (you are here)

---

## 🔌 Module Dependencies

```
cli/
  └─→ core, alpha, examples, importers, improvements, insights, outputs, review

core/
  └─→ (no dependencies - foundation)

alpha/
  └─→ core

examples/
  └─→ core

importers/
  └─→ core

improvements/
  └─→ core

insights/
  └─→ core

outputs/
  └─→ core

review/
  └─→ core
```

**Key Rule:** Only `cli` imports from other modules. Feature modules only import from `core`.

---

## 🗄️ Database Schema

**Location:** `data/nobody_cares.db` (auto-created)

**Tables:**

- `entries` - All entries (trades, code, alpha, risk, etc.)
- `projects` - Project definitions
- `improvements` - Improvement tracking
- `alpha_signals` - Alpha signals
- `alpha_briefs` - Generated alpha briefs
- `skills` - Skill definitions
- `opportunities` - Monetization opportunities

**Schema defined in:** `src/core/storage.py` → `_init_db()`

**Extend:** Add new tables in `_init_db()`, add models in `models.py`

---

## 🧪 Testing

**Location:** `tests/`

**Structure:**

- `test_*.py` - One test file per module
- `conftest.py` - Shared fixtures
- `README.md` - Test documentation

**Run tests:**

```bash
pytest
```

**Extend:** Add new test files following existing pattern

---

## 🚀 Entry Points

### CLI Entry Point

- **File:** `src/cli/main.py`
- **Function:** `main()` (decorated with `@click.group()`)
- **Registered in:** `pyproject.toml` → `[project.scripts]` → `nc = "src.cli.main:main"`

### Python API (if needed)

- Import `Storage` from `src.core.storage`
- Import models from `src.core.models`
- Use directly (no CLI needed)

---

## 🎨 Design Principles

### 1. **Modularity**

- Each feature in its own module
- Modules only depend on `core`
- `cli` orchestrates everything

### 2. **Data Layer**

- All data goes through `Storage` class
- Models defined in `core.models`
- Database schema in `Storage._init_db()`

### 3. **Extensibility**

- Clear boundaries (extension points documented)
- New features don't break existing ones
- Backward compatible (legacy fields still work)

### 4. **User-Centric**

- CLI is primary interface
- Quick capture for low-friction logging
- Progressive enhancement (add details later)

---

## 🔍 Finding Things

### "Where is X defined?"

- **Data models** → `src/core/models.py`
- **Database operations** → `src/core/storage.py`
- **CLI commands** → `src/cli/main.py`
- **Pattern detection** → `src/insights/patterns.py`
- **Content generation** → `src/outputs/content.py`
- **Review logic** → `src/review/prompts.py`
- **Examples** → `src/examples/library.py`

### "How does X connect to Y?"

- **CLI → Everything:** `src/cli/main.py` imports all modules
- **Everything → Storage:** All modules use `Storage` class
- **Storage → Database:** `Storage` handles SQLite operations
- **Models → Storage:** Models are serialized/deserialized by Storage

### "Where do I add X?"

- **New command** → `src/cli/main.py`
- **New model** → `src/core/models.py`
- **New table** → `src/core/storage.py` → `_init_db()`
- **New pattern** → `src/insights/patterns.py`
- **New content format** → `src/outputs/`
- **New importer** → `src/importers/`

---

## 🛑 Boundaries (Where Things Stop)

### Data Layer Boundary

- **Stops at:** `Storage` class
- **Doesn't go:** Direct SQLite access from other modules
- **Why:** Centralized database operations, easier to maintain

### CLI Boundary

- **Stops at:** `main.py` (all user interaction)
- **Doesn't go:** Direct module access from outside
- **Why:** Single entry point, consistent interface

### Model Boundary

- **Stops at:** `core.models.py` (all data structures)
- **Doesn't go:** Ad-hoc dictionaries in other modules
- **Why:** Type safety, validation, consistency

### Feature Module Boundaries

- **Stops at:** Each module's own files
- **Doesn't go:** Feature modules importing from each other
- **Why:** Modularity, clear dependencies

---

## 📝 Quick Reference

### Add a New Risk Field

1. Add to `RiskEntry` in `src/core/models.py`
2. Add CLI option in `src/cli/main.py` → `log_risk()`
3. Add to `update_risk()` if updatable
4. Add to display in `list_risks()` if needed

### Add a New Command

1. Add `@main.command()` in `src/cli/main.py`
2. Import needed modules
3. Use `Storage` for data access
4. Add to help text if needed

### Add a New Pattern

1. Add function to `src/insights/patterns.py`
2. Export in `src/insights/__init__.py`
3. Add CLI command in `src/cli/main.py` → `patterns` group

### Add a New Content Format

1. Create file in `src/outputs/`
2. Implement generator class
3. Export in `src/outputs/__init__.py`
4. Add to `ContentGenerator` or create new class
5. Add CLI command in `src/cli/main.py` → `content` group

---

## 🎯 Where to Start Pushing

### High-Level Extensions

- **New entry types** → `core/models.py` + `core/storage.py`
- **New analysis** → `insights/patterns.py`
- **New outputs** → `outputs/`
- **New importers** → `importers/`

### Low-Level Extensions

- **New CLI commands** → `cli/main.py`
- **New utilities** → `core/utils.py` or `core/currency.py`
- **New examples** → `examples/library.py`

### Data Extensions

- **New fields** → `core/models.py` (add to existing models)
- **New tables** → `core/storage.py` (add to `_init_db()`)

---

## 🔗 See Also

- [README.md](README.md) - Overview
- [QUICKSTART.md](QUICKSTART.md) - Getting started
- [WHEN_TO_LOG.md](WHEN_TO_LOG.md) - Practical examples
- [DAILY_GUIDE.md](DAILY_GUIDE.md) - Deep workflows
- [docs/MAJOR_SHIFTS.md](docs/MAJOR_SHIFTS.md) - Recent changes

---

**Last Updated:** See git history for latest changes.
