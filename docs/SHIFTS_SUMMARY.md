# Major Shifts Summary

## What Changed

### 1. Intuition Fields → Structured (BREAKING in approach, backward compatible)

**OLD:**

```bash
--what-i-see "Market slow to react"  # Free-form
--why-i-trust-this "Similar pattern"  # Free-form
```

**NEW (Preferred):**

```bash
--what-i-saw "Vol compressed despite catalyst"  # Observable pattern
--why-it-mattered "Structure didn't match narrative"  # Why relevant
```

**Impact:** Forces observable patterns, not feelings. Legacy fields still work.

---

### 2. NEW: Agency & Ownership (Binary Data)

**Added:**

```bash
--ownership mine/influenced/performed  # Binary classification
--aligned-with-self  # True/False
--voluntary  # True/False
```

**Why:** Binary data, not narrative. Enables correlation analysis.

---

### 3. NEW: Influence Surface (Access Control)

**Added:**

```bash
--voices-present "scadet,euko"  # Who gets access to influence
```

**Why:** Track who influences you. Everyone else is noise.

---

### 4. NEW: Motivation Integrity (Classification)

**Added:**

```bash
--motivation-internal  # True/False
--motivation-type alignment/expectation/avoidance/pruning
```

**Why:** Classification, not journaling. Track internal vs external.

---

### 5. NEW: Pattern Detection Commands

**Added:**

```bash
nc patterns misalignment  # Repeated deviations from self
nc patterns drift  # Repeated corrections back to self
nc patterns ownership  # Ownership vs outcomes correlation
```

**Why:** Longitudinal pattern data, not mood.

---

## What Stayed the Same

- All existing fields work
- Quick capture (`nc q`) unchanged
- Multi-currency support unchanged
- Content generation unchanged
- Backward compatible

---

## Migration

**No migration needed** - system is backward compatible.

**For new entries**, prefer structured fields:

- Use `--what-i-saw` instead of `--what-i-see`
- Use `--why-it-mattered` instead of `--why-i-trust-this`
- Add `--ownership`, `--aligned-with-self`, `--voluntary` when relevant
- Add `--voices-present` to track influence
- Add `--motivation-internal`, `--motivation-type` for motivation tracking

---

## Key Principle

**This is a personal signal extraction engine, not a feelings database.**

- Binary data, not narrative
- Observable patterns, not feelings
- Access control, not emotion
- Classification, not journaling
- Longitudinal patterns, not mood
