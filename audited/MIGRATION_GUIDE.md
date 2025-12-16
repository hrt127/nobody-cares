# Data Migration Guide

**How to handle schema changes and data migration**

---

## Current Schema

**Database:** SQLite (`data/nobody_cares.db`)

**Tables:**

- `entries` - All entries (JSON metadata)
- `projects` - Projects
- `improvements` - Improvements
- `alpha_signals` - Alpha signals
- `alpha_briefs` - Alpha briefs
- `skills` - Skills
- `opportunities` - Opportunities

---

## Migration Strategy

### Backward Compatibility (Current Approach)

**How it works:**

- New fields added to models don't break old data
- Metadata stored as JSON (flexible)
- Missing fields default to `None`
- Old entries work with new code

**Example:**

- Old entry has `what_i_see` (legacy field)
- New code expects `what_i_saw` (structured field)
- System handles both (backward compatible)

---

## Manual Migration Steps

### If Schema Changes (Future)

**1. Backup First:**

```bash
cp data/nobody_cares.db data/nobody_cares.db.backup
```

**2. Check Current Schema:**

```bash
sqlite3 data/nobody_cares.db ".schema"
```

**3. Run Migration Script (if provided):**

```bash
python scripts/migrate_v1_to_v2.py
```

**4. Verify:**

```bash
nc risks  # Check entries still work
```

---

## Field Migration Examples

### Migrating Legacy Fields

**Example: Migrate `what_i_see` → `what_i_saw`**

```python
import sqlite3
import json

conn = sqlite3.connect('data/nobody_cares.db')
cursor = conn.cursor()

# Get all entries
cursor.execute("SELECT id, metadata FROM entries WHERE entry_type = 'risk'")
entries = cursor.fetchall()

for entry_id, metadata_json in entries:
    metadata = json.loads(metadata_json)
    
    # Migrate field
    if 'what_i_see' in metadata and 'what_i_saw' not in metadata:
        metadata['what_i_saw'] = metadata['what_i_see']
        # Optionally remove old field
        # del metadata['what_i_see']
    
    # Update entry
    cursor.execute(
        "UPDATE entries SET metadata = ? WHERE id = ?",
        (json.dumps(metadata), entry_id)
    )

conn.commit()
conn.close()
```

---

## Version Tracking (Future)

**Recommended: Add version to database:**

```sql
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Check version:**

```python
cursor.execute("SELECT MAX(version) FROM schema_version")
version = cursor.fetchone()[0] or 0
```

---

## Best Practices

**1. Always Backup:**

- Before any migration
- Before schema changes
- Regular backups recommended

**2. Test Migration:**

- Test on copy of database first
- Verify all entries still accessible
- Check that new fields work

**3. Document Changes:**

- Document what changed
- Document why it changed
- Document migration steps

**4. Backward Compatibility:**

- Prefer adding fields over removing
- Keep legacy fields working
- Gradual migration (not forced)

---

## Current Status

**No Migration Needed:**

- Current system is backward compatible
- New fields are optional
- Old entries work with new code

**Future Migrations:**

- Will be documented here
- Will include scripts if needed
- Will maintain backward compatibility

---

## Emergency Recovery

**If Migration Fails:**

1. **Restore Backup:**

   ```bash
   cp data/nobody_cares.db.backup data/nobody_cares.db
   ```

2. **Check Logs:**
   - Look for error messages
   - Check database integrity

3. **Manual Fix:**
   - Use SQLite browser
   - Fix corrupted entries
   - Re-run migration

---

**Last Updated:** Current  
**Status:** No migration needed (backward compatible)
