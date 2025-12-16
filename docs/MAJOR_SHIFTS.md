# Major Shifts: Agency & Ownership Tracking

## Overview

The system has been updated to model **agency, ownership, and influence as structured data** - not narrative or feelings. This is a shift from free-form intuition tracking to **binary classifications and observable patterns**.

---

## Major Shifts

### 1. **Intuition → Structured Fields** (BREAKING CHANGE in approach, backward compatible)

**Before:**

- `what_i_see`: Free-form text ("What you're noticing")
- `why_i_trust_this`: Free-form text ("Past experience, pattern match")

**After:**

- `what_i_saw`: **Structured** - Observable pattern or anomaly (e.g., "Vol compressed despite catalyst")
- `why_it_mattered`: **Structured** - Why this signal was relevant (e.g., "Structure didn't match narrative")

**Why:**

- Forces you to capture **observable patterns**, not feelings
- Makes intuition trackable as data, not prose
- Enables pattern detection over time

**Migration:**

- Legacy fields (`what_i_see`, `why_i_trust_this`) still work
- New structured fields preferred
- System accepts both (backward compatible)

---

### 2. **New: Agency & Ownership Tracking** (NEW FEATURE)

**Added Fields:**

- `ownership`: Enum (`mine` / `influenced` / `performed`)
  - **mine**: Decision was mine
  - **influenced**: Decision was influenced by others
  - **performed**: Action performed under pressure/expectation
  
- `aligned_with_self`: Boolean (True/False)
  - True if aligned with non-negotiables
  - False if not
  
- `voluntary`: Boolean (True/False)
  - True if voluntary decision
  - False if under pressure

**Why:**

- Binary data, not narrative
- Enables correlation analysis (ownership vs outcomes)
- Tracks state transitions (freedom removes excuses)

**Usage:**

```bash
nc risk sports_bet --cost 100 --ownership mine --aligned-with-self --voluntary "My decision"
nc risk sports_bet --cost 100 --ownership influenced --not-aligned --under-pressure "Under pressure"
```

---

### 3. **New: Influence Surface Tracking** (NEW FEATURE)

**Added Field:**

- `voices_present`: Array of identifiers (e.g., `["scadet", "euko"]`)

**Why:**

- Access control, not emotion
- Track who gets to influence you
- Everyone else is noise
- Enables correlation: which voices correlate with better outcomes?

**Usage:**

```bash
nc risk sports_bet --cost 100 --voices-present "scadet,euko" "Influenced by these voices"
```

---

### 4. **New: Motivation Integrity Tracking** (NEW FEATURE)

**Added Fields:**

- `motivation_internal`: Boolean (True/False)
  - True if internal alignment
  - False if external expectation
  
- `motivation_type`: Enum (`alignment` / `expectation` / `avoidance` / `pruning`)

**Why:**

- Classification, not journaling
- Track: Was this done for internal alignment or external expectation?
- Track: Was this avoidance, or pruning?

**Usage:**

```bash
nc risk sports_bet --cost 100 --motivation-internal --motivation-type alignment "Internal alignment"
nc risk sports_bet --cost 100 --motivation-external --motivation-type expectation "External expectation"
```

---

### 5. **New: Pattern Detection Queries** (NEW FEATURE)

**Added Commands:**

- `nc patterns misalignment` - Detect repeated deviations from self
- `nc patterns drift` - Detect repeated corrections back to self
- `nc patterns ownership` - Analyze ownership vs outcomes correlation

**Why:**

- Longitudinal pattern data, not mood
- Track cost of drift
- See which ownership types correlate with better outcomes

**Usage:**

```bash
nc patterns misalignment --days 90
nc patterns drift --days 90
nc patterns ownership --days 90
```

---

## What Stayed the Same

- All existing fields still work
- Legacy intuition fields (`what_i_see`, `why_i_trust_this`) still accepted
- Quick capture mode (`nc q`) unchanged
- Multi-currency support unchanged
- Content generation unchanged

---

## Migration Guide

### For Existing Entries

No migration needed - system is backward compatible. New fields are optional.

### For New Entries

**Recommended approach:**

1. Use structured fields when possible:
   - `--what-i-saw` instead of `--what-i-see`
   - `--why-it-mattered` instead of `--why-i-trust-this`

2. Add agency/ownership tracking:
   - `--ownership mine/influenced/performed`
   - `--aligned-with-self` or `--not-aligned`
   - `--voluntary` or `--under-pressure`

3. Track influence:
   - `--voices-present "name1,name2"`

4. Track motivation:
   - `--motivation-internal` or `--motivation-external`
   - `--motivation-type alignment/expectation/avoidance/pruning`

**Quick capture still works:**

```bash
nc q 100 "quick bet"  # Still works, add details later
```

---

## Examples

### Before (Free-form intuition)

```bash
nc risk sports_bet --cost 100 \
  --what-i-see "Market slow to react" \
  --why-i-trust-this "Similar pattern in trading" \
  "Value bet"
```

### After (Structured + Agency)

```bash
nc risk sports_bet --cost 100 \
  --what-i-saw "Vol compressed despite catalyst" \
  --why-it-mattered "Structure didn't match narrative" \
  --ownership mine \
  --aligned-with-self \
  --voluntary \
  "Value bet"
```

### With Influence Tracking

```bash
nc risk sports_bet --cost 100 \
  --what-i-saw "Market slow to react" \
  --why-it-mattered "Similar pattern in trading" \
  --ownership influenced \
  --voices-present "scadet" \
  --not-aligned \
  --under-pressure \
  "Influenced bet"
```

---

## Key Principles

1. **Binary data, not narrative** - Ownership, alignment, voluntary are binary
2. **Observable patterns, not feelings** - `what_i_saw` is observable, not emotional
3. **Access control, not emotion** - `voices_present` is who gets access, not how you feel
4. **Classification, not journaling** - Motivation is classification, not prose
5. **Longitudinal patterns, not mood** - Pattern detection over time, not daily feelings
6. **60-second rule** - If it can't be logged in under 60 seconds, it's not signal

## Anti-Drama Constraint

**System Rule (documented, not enforced):**
> "If it can't be logged in under 60 seconds, it's not signal."

This protects you from:

- Overfitting
- Emotional spirals
- Turning this into a diary

Your `nc q` command already supports this. Good instinct.

---

## Impact

**What you can now do:**

- Track ownership vs outcomes: Does "mine" correlate with better results?
- Detect drift patterns: When do you deviate from self? When do you correct?
- Analyze influence: Which voices correlate with better/worse outcomes?
- Track alignment: What's the cost of misalignment?

**What you can't do:**

- Turn this into a feelings database (by design)
- Journal about emotions (system doesn't support it)
- Track daily mood (not the point)

---

## Next Steps

1. Start using structured fields for new entries
2. Add agency/ownership tracking when relevant
3. Run pattern detection queries periodically
4. Review misalignment patterns to see where you drift
5. Analyze ownership correlation to see what works

The system is backward compatible - existing entries work fine. New entries can use the structured approach.
