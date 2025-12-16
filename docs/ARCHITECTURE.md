# Architecture Documentation

**Deep dive into the system architecture.**

---

## Overview

This document provides detailed architectural information beyond the quick reference in `INDEX.md`.

---

## System Architecture

### Layer Structure

```
┌─────────────────────────────────────┐
│         CLI Layer (main.py)         │  ← User Interface
├─────────────────────────────────────┤
│      Feature Modules                │  ← Business Logic
│  (insights, outputs, review, etc.)  │
├─────────────────────────────────────┤
│         Core Layer                  │  ← Foundation
│  (models, storage, utils, currency) │
├─────────────────────────────────────┤
│      SQLite Database                │  ← Persistence
└─────────────────────────────────────┘
```

### Data Flow

1. **User Input** → CLI command
2. **CLI** → Validates input, calls feature modules
3. **Feature Modules** → Use Storage for data operations
4. **Storage** → SQLite database operations
5. **Response** → CLI formats output → User

---

## Module Dependencies

### Dependency Graph

```
cli/
  └─→ core (models, storage, utils, currency)
  └─→ alpha
  └─→ examples
  └─→ importers
  └─→ improvements
  └─→ insights
  └─→ outputs
  └─→ review

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

**Key Rule:** Only `cli` imports from feature modules. Feature modules only import from `core`.

---

## Design Patterns

### Repository Pattern

- **Storage class** abstracts database operations
- All data access goes through Storage
- No direct SQLite access from other modules

### Factory Pattern

- **Content generators** create different output formats
- Each generator handles one format (Twitter, LinkedIn, etc.)

### Strategy Pattern

- **Importers** use base class with specific implementations
- **Content generation** uses different strategies per format

### Template Method

- **BaseImporter** defines structure, subclasses implement specifics

---

## Extension Points

### Adding a New Feature Module

1. Create `src/new_feature/` directory
2. Add `__init__.py` with exports
3. Implement feature (import only from `core`)
4. Add to `cli/main.py` (import and use)
5. Update `pyproject.toml` packages list

### Adding a New Data Model

1. Add to `src/core/models.py`
2. Update `Storage._init_db()` for new table
3. Add CRUD methods to `Storage` class
4. Add CLI commands in `main.py`

### Adding a New Content Format

1. Create `src/outputs/new_format.py`
2. Implement generator class
3. Export in `src/outputs/__init__.py`
4. Add CLI command in `main.py`

---

## Database Schema

### Tables

- `entries` - All entries (trades, code, alpha, risk, etc.)
- `projects` - Project definitions
- `improvements` - Improvement tracking
- `alpha_signals` - Alpha signals
- `alpha_briefs` - Generated alpha briefs
- `action_items` - Action items from briefs
- `trades` - Trading performance data
- `skills` - Skill definitions
- `opportunities` - Monetization opportunities
- `monetization_paths` - Paths to monetize skills

### Schema Design

- **Flexible metadata** - JSON fields for extensibility
- **Type safety** - Pydantic models for validation
- **Indexes** - On frequently queried fields
- **Foreign keys** - For relationships (projects, etc.)

---

## Error Handling Strategy

### Layers

1. **Input Validation** - Pydantic models validate structure
2. **Business Logic** - Try/catch in feature modules
3. **Storage Layer** - Context managers for transactions
4. **CLI Layer** - User-friendly error messages

### Principles

- **Graceful degradation** - Missing data doesn't break
- **Helpful errors** - Messages include hints
- **No silent failures** - Errors are logged/displayed
- **Transaction safety** - Database operations are atomic

---

## Performance Considerations

### Current Approach

- **SQLite** - Lightweight, local-only
- **No connection pooling** - Context managers handle connections
- **Simple queries** - No complex joins (metadata in JSON)
- **Indexes** - On timestamp, entry_type, project_id

### Scalability

- **Current limit:** ~10,000 entries (comfortable)
- **Future:** Could add pagination, query optimization
- **Database:** SQLite handles millions of rows

---

## Security & Privacy

### Design Principles

- **Local-only** - No network access
- **No external deps** - For storage (SQLite is local)
- **User owns data** - Database file is user's
- **No telemetry** - No tracking, no analytics

### Data Protection

- **`.gitignore`** - Database files never committed
- **No secrets in code** - Credentials in `.env` (gitignored)
- **Input validation** - Pydantic prevents injection
- **Type safety** - Type hints catch errors early

---

## Testing Strategy

### Current Coverage

- **Unit tests** - Models, utilities, storage
- **Integration tests** - CLI commands, workflows
- **Test structure** - Mirrors source structure

### Test Organization

```
tests/
├── test_models.py      # Model validation
├── test_storage.py     # Database operations
├── test_cli.py         # CLI commands
├── test_risk_tracking.py  # Risk entry workflows
└── ...
```

---

## Future Considerations

### Potential Enhancements

1. **API Layer** - REST API for programmatic access
2. **Web UI** - Browser-based interface
3. **Backup System** - User-controlled cloud backup
4. **Visualization** - Charts for pattern data
5. **Migration System** - Automated schema migrations

### Architecture Decisions

- **Keep local-only** - Privacy-first principle
- **Maintain modularity** - Easy to extend
- **Backward compatibility** - Don't break existing usage
- **Progressive enhancement** - Add features incrementally

---

**Last Updated:** Current
