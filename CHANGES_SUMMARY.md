# Changes Summary: Agency & Ownership Tracking

## What Was Added

### 1. New Model Fields

**Agency & Ownership (Binary Data):**

- `ownership`: Enum (`mine` / `influenced` / `performed`)
- `aligned_with_self`: Boolean (True/False)
- `voluntary`: Boolean (True/False)

**Influence Surface (Access Control):**

- `voices_present`: List[str] - Identifiers of who influenced

**Motivation Integrity (Classification):**

- `motivation_internal`: Boolean (True/False)
- `motivation_type`: Enum (`alignment` / `expectation` / `avoidance` / `pruning`)

**Structured Intuition (Observable Patterns):**

- `what_i_saw`: Observable pattern or anomaly (replaces free-form `what_i_see`)
- `why_it_mattered`: Why this signal was relevant (replaces free-form `why_i_trust_this`)

### 2. New CLI Options

**Risk Command:**

- `--what-i-saw` (structured, preferred)
- `--why-it-mattered` (structured, preferred)
- `--ownership mine/influenced/performed`
- `--aligned-with-self` / `--not-aligned`
- `--voluntary` / `--under-pressure`
- `--voices-present "name1,name2"`
- `--motivation-internal` / `--motivation-external`
- `--motivation-type alignment/expectation/avoidance/pruning`

**Update Risk Command:**

- All new fields supported via `nc update-risk <id> --<field> <value>`

**New Commands:**

- `nc patterns misalignment` - Detect repeated deviations from self
- `nc patterns drift` - Detect repeated corrections back to self
- `nc patterns ownership` - Analyze ownership vs outcomes correlation

### 3. New Modules

- `src/insights/patterns.py` - Pattern detection queries
- `src/insights/__init__.py` - Insights module exports

### 4. Documentation Updates

- `MAJOR_SHIFTS.md` - Detailed explanation of changes
- `SHIFTS_SUMMARY.md` - Quick reference
- `DAILY_GUIDE.md` - Updated with new fields and pattern detection
- `README.md` - Updated feature list

---

## What Changed (Breaking in Approach, Backward Compatible)

### Intuition Fields Restructured

**OLD (Still Works):**

```bash
--what-i-see "Market slow"  # Free-form
--why-i-trust-this "Pattern match"  # Free-form
```

**NEW (Preferred):**

```bash
--what-i-saw "Vol compressed despite catalyst"  # Observable pattern
--why-it-mattered "Structure didn't match narrative"  # Why relevant
```

**Impact:** Forces observable patterns, not feelings. Legacy fields still accepted.

---

## What Stayed the Same

- All existing fields work
- Quick capture (`nc q`) unchanged
- Multi-currency support unchanged
- Content generation unchanged
- Database schema unchanged (uses JSON metadata)
- Backward compatible

---

## Key Principles Added

1. **Binary data, not narrative** - Ownership, alignment, voluntary are binary
2. **Observable patterns, not feelings** - `what_i_saw` is observable, not emotional
3. **Access control, not emotion** - `voices_present` is who gets access, not how you feel
4. **Classification, not journaling** - Motivation is classification, not prose
5. **Longitudinal patterns, not mood** - Pattern detection over time, not daily feelings
6. **60-second rule** - If it can't be logged in under 60 seconds, it's not signal

---

## Migration

**No migration needed** - system is backward compatible.

**For new entries**, prefer:

- Structured fields (`--what-i-saw`, `--why-it-mattered`)
- Agency tracking (`--ownership`, `--aligned-with-self`, `--voluntary`)
- Influence tracking (`--voices-present`)
- Motivation tracking (`--motivation-internal`, `--motivation-type`)

**Legacy fields still work** for backward compatibility.

---

## Files Modified

1. `src/core/models.py` - Added new fields and OwnershipType enum
2. `src/cli/main.py` - Added CLI options and pattern detection commands
3. `src/insights/patterns.py` - New pattern detection module
4. `src/insights/__init__.py` - New insights module
5. `DAILY_GUIDE.md` - Updated documentation
6. `README.md` - Updated feature list
7. `MAJOR_SHIFTS.md` - Detailed change documentation
8. `SHIFTS_SUMMARY.md` - Quick reference

---

## Testing

All changes are backward compatible. Existing entries work fine. New entries can use structured approach.

Run basic validation:

```bash
python -c "from src.core.models import OwnershipType; print('OK')"
```
