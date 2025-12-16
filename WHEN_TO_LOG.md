# When to Log: Practical Checklist

**The rule:** Log as you're doing it, not after. If you're building something, log it while building. If you're betting, log it when you place the bet.

---

## The Checklist (Run This Whenever)

Ask yourself:

1. **Am I risking money/time/energy right now?** → Log it
2. **Am I making a decision that matters?** → Log it
3. **Am I building something to improve?** → Log it (as you build, not after)
4. **Am I noticing something that feels important?** → Log it
5. **Am I about to do something I've done before?** → Log it (track patterns)

**If yes to any → Log it immediately, even if minimal.**

---

## What Qualifies? (Concrete Examples)

### ✅ YES - Log These

**Building/Improving:**

- Setting up a new tool/system
- Writing code for a project
- Configuring something
- Researching a solution
- Testing something new

**Risking Money:**

- Placing a bet (sports, prediction market, etc.)
- Making a trade
- Buying something significant
- Investing time in something uncertain

**Making Decisions:**

- Choosing between options
- Committing to something
- Saying yes/no to something
- Changing direction

**Noticing Patterns:**

- "This feels similar to X"
- "I've seen this before"
- "This doesn't match what I expected"

### ❌ NO - Don't Log These

- Routine daily tasks (unless they're risks)
- Things you already finished (log while doing, not after)
- Pure thoughts with no action
- Things that take >60 seconds to describe

---

## How to Log: Real Examples

### Example 1: Building Something

**You're setting up a new database:**

```bash
# Log it AS you're doing it
nc q 0 "Setting up Postgres for project X"

# Or if you have 30 seconds:
nc risk other \
  --cost 0 \
  --risk-type "setup" \
  --what-i-saw "Need to configure Postgres for new project" \
  --why-it-mattered "This is infrastructure that will be used" \
  --ownership mine \
  --aligned-with-self \
  --voluntary \
  "Setting up Postgres"
```

**Key point:** Log while building, not after it's done.

---

### Example 2: Placing a Bet

**You're about to place a sports bet:**

```bash
# Quick capture (if overwhelmed):
nc q 100 "Houston bet"

# Or full context (if you have time):
nc risk sports_bet \
  --cost 100 \
  --odds 2.5 \
  --my-probability 0.55 \
  --market-probability 0.40 \
  --what-i-saw "Line moved but I still see value" \
  --why-it-mattered "Similar pattern last week worked" \
  --ownership mine \
  --aligned-with-self \
  --voluntary \
  "Houston vs Denver"
```

**Key point:** Log when you place it, not after the game.

---

### Example 3: Making a Decision

**You're choosing between two options:**

```bash
# Log the decision AS you make it
nc risk other \
  --cost 0 \
  --risk-type "decision" \
  --what-i-saw "Two options: A or B" \
  --why-it-mattered "This affects next steps" \
  --ownership mine \
  --aligned-with-self \
  --voluntary \
  "Chose option A because..."
```

**Key point:** Log the decision, not the outcome.

---

### Example 4: Noticing a Pattern

**You see something that reminds you of something else:**

```bash
# Quick capture:
nc q 0 "This feels like the crypto pattern from last month"

# Or with context:
nc risk other \
  --cost 0 \
  --risk-type "pattern" \
  --what-i-saw "Vol compressed despite news" \
  --why-it-mattered "Same as BTC breakout pattern" \
  --related-trades 123 \
  --pattern-match "Similar to crypto trade #123" \
  "Noticing pattern match"
```

**Key point:** Log the observation, link to related entries.

---

### Example 5: Researching Something

**You're researching a solution:**

```bash
# Log it while researching
nc q 0 "Researching Postgres connection pooling"

# Or with context:
nc risk other \
  --cost 0 \
  --risk-type "research" \
  --time-invested 0.5 \
  --what-i-saw "Need to understand connection pooling" \
  --why-it-mattered "This will affect performance" \
  --ownership mine \
  --aligned-with-self \
  "Researching Postgres pooling"
```

**Key point:** Log while researching, track time invested.

---

### Example 6: Testing Something

**You're testing a new approach:**

```bash
# Quick capture:
nc q 0 "Testing new CLI command structure"

# Or with context:
nc risk other \
  --cost 0 \
  --risk-type "test" \
  --what-i-saw "New CLI structure might be better" \
  --why-it-mattered "Could improve workflow" \
  --ownership mine \
  --aligned-with-self \
  "Testing new CLI approach"
```

**Key point:** Log the test, not just the result.

---

## The "I Don't Understand What I'm Doing" Problem

**If you're building something and don't understand it:**

1. **Log it anyway** - use quick capture:

   ```bash
   nc q 0 "Setting up X, not sure how it works yet"
   ```

2. **Add context later** when you understand:

   ```bash
   nc update-risk <id> --what-i-saw "Actually, it does Y" --why-it-mattered "Because Z"
   ```

3. **Track the learning:**

   ```bash
   nc update-risk <id> --notes "Learned that X works by doing Y"
   ```

**Key point:** Log the confusion, update when clarity comes.

---

## The "When Does It Qualify?" Problem

**Simple test:** If you're asking "should I log this?", the answer is **yes**.

**Better test:**

- Is this a decision? → Log it
- Is this a risk? → Log it
- Is this building something? → Log it
- Does this feel important? → Log it

**If unsure:** Use quick capture (`nc q 0 "<what you're doing>"`), add context later.

---

## The "I Forgot to Log" Problem

**If you already did something:**

1. **Log it now anyway** - better late than never:

   ```bash
   nc q 0 "Already did X, logging now"
   ```

2. **Add context about when it happened:**

   ```bash
   nc update-risk <id> --notes "Actually did this yesterday, logging now"
   ```

3. **Next time:** Log while doing, not after.

**Key point:** Don't skip logging because you forgot. Log it now.

---

## The "I'm Building Things to Improve" Problem

**You're building tools to improve, but need to actually USE them:**

1. **Log the building:**

   ```bash
   nc q 0 "Building new logging tool"
   ```

2. **Log when you USE it:**

   ```bash
   nc q 0 "Using new logging tool for first time"
   ```

3. **Track if it works:**

   ```bash
   nc update-risk <id> --notes "Tool worked well, will use again"
   ```

**Key point:** Log both building AND using. Track what works.

---

## The "I Know When Something Feels Right" Problem

**If something feels right, log WHY:**

```bash
nc risk other \
  --cost 0 \
  --risk-type "intuition" \
  --what-i-saw "This approach feels right" \
  --why-it-mattered "Matches pattern from successful X" \
  --gut-feeling "strong" \
  --ownership mine \
  --aligned-with-self \
  "This feels right because..."
```

**Key point:** Capture the "feels right" moment, explain why later.

---

## Practical Workflow

**Morning (or whenever you start):**

1. Open terminal
2. Run `nc today` to see what's open
3. As you do things, log them immediately

**While working:**

- Building something? → `nc q 0 "Building X"`
- Making a decision? → `nc q 0 "Deciding Y"`
- Noticing something? → `nc q 0 "Noticing Z"`

**End of session (optional):**

- Run `nc today` to review
- Add context to quick entries if you have time

**Key point:** Log as you go, review when you have time.

---

## Common Scenarios

### Scenario: Setting Up a New Project

```bash
# Step 1: Log that you're starting
nc q 0 "Starting new project X"

# Step 2: As you configure things, log them
nc q 0 "Configuring database for project X"
nc q 0 "Setting up API keys for project X"

# Step 3: When done, update with context
nc update-risk <id> --what-i-saw "Project setup complete" --why-it-mattered "Infrastructure ready"
```

### Scenario: Placing Multiple Bets

```bash
# Bet 1: Quick capture
nc q 100 "Bet 1: Houston"

# Bet 2: Quick capture
nc q 50 "Bet 2: Over/under"

# Later: Add context to both
nc update-risk <id1> --odds 2.5 --my-probability 0.55
nc update-risk <id2> --odds 1.8 --my-probability 0.60
```

### Scenario: Researching and Then Acting

```bash
# Step 1: Log research
nc q 0 "Researching X solution"

# Step 2: Log the decision
nc q 0 "Decided to use Y approach"

# Step 3: Log implementation
nc q 0 "Implementing Y approach"

# Later: Link them together
nc update-risk <id2> --related-trades <id1>
nc update-risk <id3> --related-trades <id1>,<id2>
```

---

## Remember

1. **Log as you go** - not after
2. **Quick capture is fine** - add context later
3. **If unsure, log it** - better to log too much than too little
4. **60-second rule** - if it takes >60 seconds, it's not signal
5. **Don't skip because you forgot** - log it now anyway

---

## Next Steps

- **Want deeper workflows?** → See [DAILY_GUIDE.md](DAILY_GUIDE.md)
- **Need basic commands?** → See [QUICKSTART.md](QUICKSTART.md)
- **Understanding the system?** → See [README.md](README.md)

---

**Remember:** Log as you go, not after. If you're building something, log it while building. If you're betting, log it when you place the bet.
