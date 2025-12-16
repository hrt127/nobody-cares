# Daily Guide: Nobody Cares - Daily Improvement Hub

A comprehensive guide to using this repository for tracking daily activities, building skills portfolios, analyzing performance, and generating shareable artifacts.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Daily Workflow](#daily-workflow)
3. [Entry Types & Best Practices](#entry-types--best-practices)
4. [Project Management](#project-management)
5. [Risk Tracking](#risk-tracking)
6. [Sports Betting - Your Edge System](#sports-betting---your-edge-system)
7. [Pattern Detection](#pattern-detection)
8. [Alpha Brief Generation](#alpha-brief-generation)
9. [Trading Performance Import](#trading-performance-import)
10. [Improvement Tracking](#improvement-tracking)
11. [Output Generation](#output-generation)
12. [Review & Iterate](#review--iterate)
13. [Workflow Integration](#workflow-integration)
14. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

```bash
# Install the package in development mode
pip install -e .

# Verify installation
nc --version
```

### First-Time Setup

1. **Database Initialization**: The database is automatically created on first use in `data/nobody_cares.db`
2. **Verify Setup**: Run a test command to ensure everything works:

   ```bash
   nc today
   ```

3. **Try Quick Capture** (when overwhelmed):

   ```bash
   nc q 100 "test bet"
   ```

4. **See Examples** (to stay grounded):

   ```bash
   nc examples list
   nc template list
   ```

---

## Daily Workflow

### Morning Routine (5-10 minutes)

**1. Review Yesterday's Entries**

```bash
nc today --type trade
nc today --type alpha
```

**Purpose**: Get context for today's activities and identify follow-ups.

**2. Check Open Risks**

```bash
nc risks --status open
```

**Purpose**: Review active risk positions and update expectations if needed.

**3. Generate Alpha Brief** (Optional, if configured)

```bash
nc alpha brief --email-label "📊"
```

**Purpose**: Get structured insights from emails and on-chain data to inform today's decisions.

---

### Throughout the Day

**Log Activities as They Happen**

The key is to log entries immediately after activities, not at the end of the day. This ensures accuracy and completeness.

#### Trading Activities

```bash
# Simple trade log
nc log trade "BTC long @ 45k, exit @ 46.2k, +2.6%"

# Trade with tags for better organization
nc log trade "ETH short @ 3200, stop @ 3250, -1.5%" --tags swing,stop_loss

# Trade with context
nc log trade "SOL breakout trade, entry @ 95, target 110, stop 90" --tags breakout,momentum
```

**Best Practices:**

- Include entry/exit prices and P/L in the notes
- Use consistent tags (e.g., `swing`, `scalp`, `breakout`, `reversal`)
- Log immediately after closing a position
- Include strategy context when relevant

**How it feeds forward:**

- Trading entries → Trading performance import → Project metrics → Output generation

#### Coding Activities

```bash
# Feature development
nc log code "Implemented user authentication with JWT tokens" --tags backend,security

# Bug fixes
nc log code "Fixed memory leak in data processing pipeline" --tags bugfix,performance

# Learning/experimentation
nc log code "Explored React Server Components for new feature" --tags learning,frontend
```

**Best Practices:**

- Link to PRs/issues when possible: `"Fixed auth bug, PR #123"`
- Use descriptive tags for skill tracking
- Include context about complexity or learning

**How it feeds forward:**

- Code entries → Skill extraction → Monetization paths → Portfolio building

#### Alpha/Research Activities

```bash
# Early signals
nc log alpha "Saw restaking narrative gaining traction in Telegram" --tags restaking,degen

# Conflicting views
nc log alpha "Noticed split opinion on LayerZero airdrop timing" --tags layerzero,airdrop

# Blind spots
nc log alpha "Realized I'm not tracking DeFi yield opportunities" --tags defi,yield
```

**Best Practices:**

- Capture the source (Telegram, Twitter, email, etc.)
- Note confidence level in your notes
- Use tags to group related narratives

**How it feeds forward:**

- Alpha entries → Alpha brief generation → Action items → Trading opportunities

#### Learning Activities

```bash
nc log learning "Completed Advanced Python course on Coursera" --tags python,education

nc log learning "Read 'Flash Boys' - insights on HFT strategies" --tags trading,books
```

**Best Practices:**

- Track both formal and informal learning
- Include what you learned, not just what you consumed
- Link to resources when helpful

**How it feeds forward:**

- Learning entries → Skill tracking → Opportunity matching

#### Action Items

```bash
nc log action "Research Uniswap V4 hooks implementation" --tags research,defi

nc log action "Set up automated trading alerts for BTC" --tags automation,trading
```

**Best Practices:**

- Be specific and actionable
- Include deadline or urgency in notes if relevant
- Update when completed (can be done via notes or separate tracking)

**How it feeds forward:**

- Action entries → Project planning → Improvement tracking

#### Opportunities

```bash
nc log opportunity "Consulting gig for DeFi protocol analysis - $5k" --tags consulting,defi

nc log opportunity "Content creator program for trading platform" --tags content,monetization
```

**Best Practices:**

- Include estimated value when known
- Note required skills
- Track status (open, applied, closed)

**How it feeds forward:**

- Opportunity entries → Monetization path planning → Skill development priorities

---

### Risk Tracking Workflow

Risk tracking is a specialized workflow for tracking any risk-taking activity (NFTs, sports bets, prediction markets, trades, etc.) with comprehensive metadata.

#### Logging a New Risk

```bash
# NFT purchase with full context
nc risk nft \
  --cost 6.3 \
  --expected-value 15 \
  --timeframe "4 weeks" \
  --opportunity-cost 5 \
  --confidence 0.7 \
  --max-loss 6.3 \
  --max-gain 50 \
  --liquidity low \
  --allocation 2.5 \
  "Cool Punks #1234 - narrative play on PFP resurgence"

# Sports bet with odds analysis
nc risk sports_bet \
  --cost 100 \
  --odds 3.21 \
  --fair-value 2.0 \
  --expected-value 160.5 \
  --confidence 0.75 \
  --risk-factors "no_cash_out,game_time_risk" \
  --timeframe "end of game" \
  "Game X vs Y - value bet on underdog"

# Prediction market position
nc risk prediction_market \
  --cost 50 \
  --expected-value 150 \
  --confidence 0.8 \
  --max-loss 50 \
  --opportunity-cost 20 \
  --opportunity-cost-notes "Could have used capital for higher EV trade" \
  "Event outcome - high conviction play"
```

**Best Practices:**

- **Always include cost**: This is required and represents capital at risk
- **Set initial expected value**: Your best estimate of the outcome value
- **Track opportunity cost**: Both perceived (what you think you're giving up) and real (what you actually gave up)
- **Use confidence levels**: 0.0-1.0 scale helps track conviction
- **Note risk factors**: Illiquidity, timing risk, correlation, etc.
- **Set allocation %**: Helps with portfolio management

**How it feeds forward:**

- Risk entries → Portfolio analysis → Risk-adjusted returns → Learning from outcomes

#### Updating Risks

As situations change, update your risk entries:

```bash
# Update expected reward (e.g., market moved favorably)
nc update-risk 1 --reward 20 --reason "market moved favorably, narrative strengthening"

# Update opportunity cost (e.g., you realized you missed a better opportunity)
nc update-risk 1 --opportunity-cost-real 8 --reason "missed better opportunity that materialized"

# Close a position with realized value
nc update-risk 1 --status closed --realized-value 12.5
```

**Best Practices:**

- Update rewards when your thesis changes
- Track opportunity cost changes over time
- Always include a reason for updates
- Close positions when they resolve

#### Reviewing Risks

```bash
# View all open risks
nc risks --status open

# View risks with full details
nc risks --show-all

# View risks with history
nc risks --show-history

# Filter by type
nc risks --type nft
```

**How it feeds forward:**

- Risk reviews → Portfolio optimization → Better risk management → Improved decision-making

---

## Sports Betting - Your Edge System

### Quick Capture Mode (When Overwhelmed)

When you're overwhelmed or just need to capture quickly:

```bash
# Ultra-quick entry - just cost and notes
nc q 100 "houston bet"

# With currency
nc q 0.1 --currency ETH "ETH bet"
```

**60-Second Rule:**
> "If it can't be logged in under 60 seconds, it's not signal."

This protects you from:

- Overfitting
- Emotional spirals
- Turning this into a diary

Quick capture mode enforces this - minimal fields, add details later.

**What happens:**

- System remembers your last used currency (smart default)
- Entry is flagged as `quick_mode` for later enhancement
- You can add all details later with `nc update-risk <id>`

**Best Practices:**

- Use quick mode when overwhelmed - don't skip logging
- Add context later when you have time
- System suggests what to add when you review

### Multi-Currency Support

Track bets in any currency - system doesn't force conversion:

```bash
# USD bet
nc risk sports_bet --cost 100 --currency USD "USD bet"

# ETH bet with gas fees
nc risk sports_bet --cost 0.1 --currency ETH --gas-fee 0.001 --gas-currency ETH "ETH bet"

# SOL bet
nc risk sports_bet --cost 2.5 --currency SOL --gas-fee 0.01 "SOL bet"
```

**Key Points:**

- Gas fees tracked separately (important early, less later)
- Original currency preserved (no forced conversion)
- System formats costs appropriately per currency
- Last used currency remembered as default

### Capturing Your Intuition & Edge

Log your unique edge, not just numbers. Use **structured fields** for observable patterns, not feelings:

```bash
# Full context with structured intuition + agency tracking
nc risk sports_bet \
  --cost 100 \
  --odds 3.21 \
  --my-probability 0.45 \
  --market-probability 0.31 \
  --what-i-saw "Vol compressed despite catalyst" \
  --why-it-mattered "Structure didn't match narrative" \
  --ownership mine \
  --aligned-with-self \
  --voluntary \
  --red-flags "No cash-out available, might get stuck" \
  --related-trades 123 \
  --pattern-match "Similar momentum shift in crypto" \
  "Houston vs Denver - halftime value bet"
```

**Structured Fields (Preferred):**

- `--what-i-saw`: **Observable pattern or anomaly** (e.g., "Vol compressed despite catalyst")
- `--why-it-mattered`: **Why this signal was relevant** (e.g., "Structure didn't match narrative")
- `--ownership`: **mine/influenced/performed** - Binary classification, not narrative
- `--aligned-with-self`: **True/False** - Aligned with non-negotiables?
- `--voluntary`: **True/False** - Voluntary decision or under pressure?
- `--voices-present`: **Comma-separated identifiers** (e.g., "scadet,euko") - Who influenced?
- `--motivation-internal`: **True/False** - Internal alignment or external expectation?
- `--motivation-type`: **alignment/expectation/avoidance/pruning** - Classification

**Legacy Fields (Still Supported):**

- `--what-i-see`: [Legacy] Free-form - use `--what-i-saw` for structured
- `--why-i-trust-this`: [Legacy] Free-form - use `--why-it-mattered` for structured
- `--gut-feeling`: Quick capture helper

**Key Principle:**

- **Binary data, not narrative** - Ownership, alignment are binary classifications
- **Observable patterns, not feelings** - `what_i_saw` is observable, not emotional
- **Access control, not emotion** - `voices_present` is who gets access, not how you feel

**How it feeds forward:**

- Your intuition → Track accuracy → Learn when you're right → Trust your process
- Ownership tracking → Pattern detection → See what works (mine vs influenced)
- Alignment tracking → Drift detection → See when you deviate from self

### Cash-Out Tracking (The Real Problem)

Track when you can't cash out - this is where value gets lost:

```bash
# Log bet with cash-out availability
nc risk sports_bet \
  --cost 100 \
  --odds 3.21 \
  --cash-out-available \
  "Bet with cash-out option"

# Or when cash-out NOT available (your frustration)
nc risk sports_bet \
  --cost 100 \
  --odds 3.21 \
  --no-cash-out \
  "Bet without cash-out - might get stuck"
```

**After outcome, update with missed value:**

```bash
# Update with missed cash-out value
nc update-risk 1 \
  --status closed \
  --realized-value 0 \
  --missed-cash-out-value 85 \
  --why-stuck "Platform no cash-out, optimal exit was Q4 when Houston led" \
  --optimal-cash-out-time "Q4, 2 minutes remaining"
```

**Why this matters:**

- You captured the edge correctly (14% edge)
- But couldn't realize value due to platform limitation
- System tracks this as real opportunity cost
- Learn: Check cash-out availability before betting

### Cross-Domain Connections

Connect sports betting insights to your other activities:

```bash
# Link to similar trade
nc risk sports_bet \
  --cost 100 \
  --odds 3.21 \
  --related-trades 123 \
  --pattern-match "Similar to BTC breakout last week" \
  --domain-knowledge "Applied momentum pattern from trading" \
  "Cross-domain insight"
```

**How it works:**

- `--related-trades`: Comma-separated entry IDs of similar trades
- `--related-alpha`: Link to alpha signals
- `--related-code`: Link to code projects
- `--pattern-match`: Free-form description of similarity
- `--domain-knowledge`: What you're applying from other domains

**Benefits:**

- See patterns across trading, sports, code
- Apply insights from one domain to another
- Build on what works

### Examples & Templates

See what others do to stay grounded:

```bash
# List available examples
nc examples list

# Show specific example
nc examples show sports-bet-intuition

# List templates
nc template list

# Show template
nc template show value-bet

# See how others structure similar bets
nc contrast <your_risk_id>
```

**Available Examples:**

- `sports-bet-quick`: Quick capture when overwhelmed
- `sports-bet-full`: Full context when you have time
- `sports-bet-multi-currency`: Crypto bets with gas fees
- `sports-bet-intuition`: Capturing your intuition
- `sports-bet-connected`: Cross-domain connections

**Available Templates:**

- `value-bet`: Value betting with edge calculation
- `quick-capture`: Ultra-fast entry
- `multi-currency`: Crypto bets
- `intuition-capture`: Gut feeling and reasoning

### Content Generation & Distribution

Generate content from your entries - one source, many outputs:

```bash
# Generate Twitter thread
nc content generate --from-risk 1 --format twitter --brevity high

# Generate LinkedIn post
nc content generate --from-risk 1 --format linkedin

# Generate blog post
nc content generate --from-risk 1 --format blog

# Generate for multiple platforms
nc content publish --from-risk 1 --to twitter,linkedin --dry-run
```

**Brevity Levels:**

- `high`: Ultra-concise, key points only
- `medium`: Balanced (default)
- `low`: More detail

**Content Includes:**

- The bet setup (amount, odds, your probability)
- What you saw (your edge)
- Outcome and lessons learned
- Hard-won insights (tasteful, educational)

**Distribution:**

- Generate once, copy/paste to multiple platforms
- Filter what to share (exclude personal/internal)
- Dry-run mode to preview before publishing

### Pattern Detection

Detect repeated deviations and corrections:

```bash
# Detect misalignment patterns (repeated deviations from self)
nc patterns misalignment --days 90

# Detect drift patterns (repeated corrections back to self)
nc patterns drift --days 90

# Analyze ownership vs outcomes correlation
nc patterns ownership --days 90
```

**What you get:**

- Misalignment rate: How often you deviate from self
- Ownership distribution: Which ownership types in misaligned entries
- Voices distribution: Which voices present when misaligned
- Corrections: When you corrected course
- Ownership correlation: Does "mine" correlate with better outcomes?

**Key Insight:**

- Track **longitudinal patterns**, not mood
- See **cost of drift** over time
- Identify **what works** (ownership type, alignment, voices)

### Review & Iterate (Not Daily)

Adapt the system to YOUR process:

```bash
# Weekly review
nc review --period week

# System adaptation suggestions
nc adapt
```

**What you get:**

- Review prompts (unresolved risks, missing context)
- Usage analytics (what you use vs skip)
- Suggestions: "You never use --gut-feeling, remove it?"
- Or: "You always add --what-i-see, make it easier?"

**Key Point:**

- Not daily habits - frequent review cycles
- System adapts to YOU, not generic best practices
- Remove unused complexity, add what you need

### Complete Sports Betting Workflow

**1. Quick Capture (When Overwhelmed)**

```bash
nc q 100 "houston bet"
```

**2. Add Context Later (When You Have Time)**

```bash
nc update-risk 1 \
  --odds 3.21 \
  --my-probability 0.45 \
  --market-probability 0.31 \
  --what-i-see "Market slow to react" \
  --why-i-trust-this "Similar pattern in trading"
```

**3. Track Live (During Game)**

```bash
nc update-risk 1 --odds 1.97 --market-probability 0.51
```

**4. Update Outcome (After Game)**

```bash
nc update-risk 1 \
  --status closed \
  --realized-value 0 \
  --missed-cash-out-value 85 \
  --why-stuck "No cash-out available"
```

**5. Learn from It**

```bash
nc content generate --from-risk 1 --format twitter
# Extract lessons, share insights
```

**6. Review & Adapt**

```bash
nc review --period week
nc adapt
```

---

### Evening Routine (10-15 minutes)

**1. Review Today's Entries**

```bash
nc today
```

**Purpose**: Ensure completeness and add any missing context.

**2. Update Open Risks**

```bash
# Check if any risks need updating
nc risks --status open --show-history
```

**3. Plan Tomorrow**

```bash
# Review action items
nc recent --type action --limit 10

# Check opportunities
nc recent --type opportunity --limit 5
```

---

## Entry Types & Best Practices

### Entry Type Reference

| Type | Use Case | Example | Tags to Consider |
|------|----------|---------|------------------|
| `trade` | Trading activities | "BTC long @ 45k, exit @ 46.2k" | `swing`, `scalp`, `breakout` |
| `code` | Development work | "Fixed auth bug, PR #123" | `backend`, `frontend`, `bugfix` |
| `alpha` | Market insights | "Restaking narrative emerging" | `narrative`, `signal`, `research` |
| `learning` | Education/study | "Completed Python course" | `education`, `skill`, `course` |
| `action` | Tasks/todos | "Research Uniswap V4" | `research`, `task`, `followup` |
| `note` | General notes | "Market sentiment shift" | `observation`, `idea` |
| `opportunity` | Monetization chances | "Consulting gig - $5k" | `consulting`, `monetization` |
| `risk` | Risk-taking activities | Use `nc risk` command | `nft`, `sports_bet`, `trade` |

### Tagging Best Practices

**Consistency is Key:**

- Use lowercase tags
- Avoid duplicates (`trading` vs `trade` - pick one)
- Use plural for categories (`trades`, `projects`)
- Use singular for specific items (`bitcoin`, `ethereum`)

**Suggested Tag Categories:**

- **Skills**: `python`, `javascript`, `trading`, `defi`
- **Projects**: `project-name`, `client-name`
- **Strategies**: `swing`, `scalp`, `momentum`, `mean-reversion`
- **Markets**: `crypto`, `stocks`, `forex`
- **Narratives**: `restaking`, `ai`, `layer2`
- **Status**: `completed`, `in-progress`, `blocked`

---

## Project Management

### Creating Projects

Projects aggregate related work (trades, code, improvements) for analysis and output generation.

```bash
# Create a project
nc project create "Trading Bot v2" --description "Automated trading system with ML signals"

# List all projects
nc project list
```

**Best Practices:**

- Create projects for major initiatives
- Use descriptive names
- Add descriptions for context
- Projects can span multiple days/weeks

### Associating Work with Projects

When importing trading data, you can associate it with a project:

```bash
nc import-data trading-performance trades.csv --project "Trading Bot v2"
```

**How it feeds forward:**

- Projects → Aggregated metrics → Output generation → Portfolio showcase

---

## Alpha Brief Generation

Alpha briefs extract structured insights from emails and on-chain data.

### Setup (One-Time)

1. Configure Gmail API credentials (when implemented)
2. Set up email labels (e.g., "📊" for alpha-related emails)

### Daily Generation

```bash
# Generate brief from emails with specific label
nc alpha brief --email-label "📊"

# Save to file
nc alpha brief --output alpha_brief_2024-01-15.md
```

### Reviewing Action Items

```bash
# List all action items
nc alpha actions

# Filter by urgency
nc alpha actions --urgency high

# Filter by status
nc alpha actions --status pending
```

**How it feeds forward:**

- Alpha briefs → Action items → Trading opportunities → Risk entries

---

## Trading Performance Import

Import complete trading performance reports from CSV files.

### CSV Format

Your CSV should include these columns (flexible naming):

**Required:**

- Entry date
- Exit date
- Symbol
- Entry price
- Exit price
- Quantity
- PnL
- Return %

**Optional:**

- Strategy
- Setup type
- Notes
- Fees
- Duration (days)

### Import Process

```bash
# Import trading data
nc import-data trading-performance trades_2024.csv --project "Q1 Trading"

# The system will:
# 1. Validate CSV format
# 2. Parse and clean data
# 3. Calculate metrics (win rate, Sharpe ratio, etc.)
# 4. Store trades in database
# 5. Associate with project (if specified)
```

### Example CSV Structure

```csv
entry_date,exit_date,symbol,entry_price,exit_price,quantity,pnl,return_pct,strategy
2024-01-01,2024-01-03,BTC,45000,46200,0.1,120,2.67,swing
2024-01-05,2024-01-07,ETH,3200,3150,1,-50,-1.56,mean_reversion
```

**How it feeds forward:**

- Trading imports → Performance analysis → Project metrics → Output generation → Portfolio showcase

---

## Improvement Tracking

Improvements are structured enhancements you can add to projects to increase their value and shareability.

### Available Improvement Types

1. **Interactive Visualization** (`interactive_viz`)
   - Create interactive trade replays with annotations
   - Best for: Trading projects, data analysis

2. **Benchmark Comparison** (`benchmark`)
   - Compare returns against market benchmarks
   - Best for: Trading projects, portfolio analysis

3. **Monetization** (`monetization`)
   - Map skills to monetization paths
   - Best for: Any project with marketable skills

4. **Video Walkthrough** (`video`)
   - 90-second video script and production
   - Best for: All projects (great for social media)

5. **Open Source Playbook** (`open_source`)
   - Framework for others to fork and use
   - Best for: Tools, libraries, methodologies

### Adding Improvements

```bash
# Add an improvement to a project
nc improvements add "Trading Bot v2" --template interactive_viz --notes "Create replay of best trades"

# View improvement guide
nc improvements guide --template interactive_viz
```

### Managing Improvements

```bash
# List all improvements
nc improvements list

# Filter by project
nc improvements list --project "Trading Bot v2"

# Update improvement status
nc improvements update 1 --status in_progress

# Mark as completed
nc improvements update 1 --status completed --notes "Published on GitHub"
```

### Improvement Workflow Example

```bash
# 1. Create project
nc project create "DeFi Yield Optimizer"

# 2. Add improvements
nc improvements add "DeFi Yield Optimizer" --template benchmark
nc improvements add "DeFi Yield Optimizer" --template video
nc improvements add "DeFi Yield Optimizer" --template monetization

# 3. View guidance
nc improvements guide --template benchmark

# 4. Work through checklist, update status
nc improvements update 1 --status in_progress
nc improvements update 1 --status completed

# 5. Generate outputs (see Output Generation section)
nc generate pdf "DeFi Yield Optimizer" --output report.pdf
nc generate twitter "DeFi Yield Optimizer"
```

**How it feeds forward:**

- Improvements → Enhanced project value → Better outputs → Portfolio showcase → Monetization opportunities

---

## Output Generation

Generate shareable artifacts from your projects.

### PDF Reports

```bash
# Generate PDF report for a project
nc generate pdf "Trading Bot v2" --output trading_report_2024.pdf
```

**What's included:**

- Project overview
- Trading performance metrics
- Top trades
- Improvements completed
- Skills demonstrated

**Best Practices:**

- Generate after completing improvements
- Use for portfolio, job applications, client reports
- Update regularly as project evolves

### Twitter Threads

```bash
# Generate Twitter thread
nc generate twitter "Trading Bot v2"

# Save to file
nc generate twitter "Trading Bot v2" --output twitter_thread.txt

# Customize content
nc generate twitter "Trading Bot v2" --no-benchmarks --no-monetization
```

**Structure:**

1. Hook tweet
2. Key metrics
3. Edge demonstration
4. Top achievements
5. Monetization (optional)
6. Call-to-action

**Best Practices:**

- Review and edit before posting
- Add personal insights
- Include relevant hashtags
- Post when you have completed improvements

### LinkedIn Posts

```bash
# Generate LinkedIn post
nc generate linkedin "Trading Bot v2"

# Save to file
nc generate linkedin "Trading Bot v2" --output linkedin_post.txt
```

**Best Practices:**

- More professional tone than Twitter
- Focus on learnings and insights
- Include metrics and outcomes
- Add relevant connections/tags

### Video Scripts

```bash
# Generate 90-second video script
nc generate video-script "Trading Bot v2"

# Save to file
nc generate video-script "Trading Bot v2" --output video_script.txt
```

**Structure:**

- Hook (5 seconds)
- Problem (10-15 seconds)
- Solution/Demo (45-60 seconds)
- Call-to-action (10 seconds)

**Best Practices:**

- Use as starting point, customize for your voice
- Add timestamps and talking points
- Prepare visuals/screen recordings
- Keep it under 90 seconds

**How it feeds forward:**

- Outputs → Social media presence → Audience building → Monetization opportunities → More projects

### Content Generation (From Risk Entries)

Generate content from your risk entries - one source, many outputs:

```bash
# Generate Twitter thread from risk entry
nc content generate --from-risk 1 --format twitter --brevity high

# Generate LinkedIn post
nc content generate --from-risk 1 --format linkedin

# Generate blog post
nc content generate --from-risk 1 --format blog

# Generate for multiple platforms
nc content publish --from-risk 1 --to twitter,linkedin --dry-run
```

**Brevity Levels:**

- `high`: Ultra-concise, key points only
- `medium`: Balanced (default)
- `low`: More detail

**Content Includes:**

- The bet setup (amount, odds, your probability)
- What you saw (your edge)
- Outcome and lessons learned
- Hard-won insights (tasteful, educational)

**Best Practices:**

- Generate after outcome is known
- Review and customize before publishing
- Use dry-run to preview
- Filter personal/internal content if needed

---

## Pattern Detection

### Detect Repeated Deviations & Corrections

Track longitudinal patterns - not mood, but **repeated deviations and corrections**:

```bash
# Detect misalignment patterns (repeated deviations from self)
nc patterns misalignment --days 90

# Detect drift patterns (repeated corrections back to self)
nc patterns drift --days 90

# Analyze ownership vs outcomes correlation
nc patterns ownership --days 90
```

**What you get:**

- **Misalignment rate**: How often you deviate from self
- **Ownership distribution**: Which ownership types in misaligned entries
- **Voices distribution**: Which voices present when misaligned
- **Corrections**: When you corrected course
- **Ownership correlation**: Does "mine" correlate with better outcomes?

**Key Insight:**

- Track **longitudinal patterns**, not mood
- See **cost of drift** over time
- Identify **what works** (ownership type, alignment, voices)

---

## Review & Iterate

### Not Daily Habits - Frequent Adaptation

The system adapts to YOUR process, not generic best practices.

### Review Cycles

```bash
# Weekly review
nc review --period week

# Monthly review
nc review --period month
```

**What you get:**

- Review prompts (unresolved risks, missing context)
- Activity summary (what you logged vs skipped)
- Suggestions for follow-up

### System Adaptation

```bash
# Get suggestions for improving the system
nc adapt
```

**What you get:**

- Fields you use most (keep these)
- Fields you rarely use (consider simplifying)
- Suggestions: "You never use --gut-feeling, remove it?"
- Or: "You always add --what-i-see, make it easier?"

**Key Points:**

- Not daily - frequent review cycles
- System learns from YOUR usage
- Remove unused complexity
- Add what you actually need

### Examples & Templates

See what others do to stay grounded:

```bash
# List examples
nc examples list

# Show specific example
nc examples show sports-bet-intuition

# List templates
nc template list

# Show template
nc template show value-bet

# See how others structure similar bets
nc contrast <your_risk_id>
```

**Why this helps:**

- Stay grounded (not too far out)
- See practical patterns
- Learn from others' structure
- Adapt to what works

---

## Workflow Integration

### Complete Workflow Example: Trading Project

**Week 1: Setup and Tracking**

```bash
# Day 1: Create project
nc project create "Q1 2024 Trading" --description "Q1 trading performance analysis"

# Day 1-7: Log daily trades
nc log trade "BTC long @ 45k, exit @ 46.2k, +2.6%" --tags swing
nc log trade "ETH short @ 3200, stop @ 3250, -1.5%" --tags mean_reversion

# Day 7: Import complete trading data
nc import-data trading-performance q1_trades.csv --project "Q1 2024 Trading"
```

**Week 2: Improvements**

```bash
# Add improvements
nc improvements add "Q1 2024 Trading" --template benchmark
nc improvements add "Q1 2024 Trading" --template interactive_viz
nc improvements add "Q1 2024 Trading" --template video

# Get guidance
nc improvements guide --template benchmark

# Work through improvements, update status
nc improvements update 1 --status in_progress
# ... complete benchmark comparison ...
nc improvements update 1 --status completed
```

**Week 3: Output Generation**

```bash
# Generate all outputs
nc generate pdf "Q1 2024 Trading" --output q1_report.pdf
nc generate twitter "Q1 2024 Trading" --output q1_twitter.txt
nc generate linkedin "Q1 2024 Trading" --output q1_linkedin.txt
nc generate video-script "Q1 2024 Trading" --output q1_video_script.txt

# Review, edit, and publish
```

### Complete Workflow Example: Risk Tracking

**Day 1: Enter Risk**

```bash
nc risk nft \
  --cost 10 \
  --expected-value 25 \
  --timeframe "2 weeks" \
  --confidence 0.7 \
  --opportunity-cost 5 \
  "NFT purchase - narrative play"
```

**Day 3: Update as Situation Changes**

```bash
# Market moved favorably
nc update-risk 1 --reward 30 --reason "narrative strengthening, floor price up"
```

**Day 7: Update Opportunity Cost**

```bash
# Realized you missed a better opportunity
nc update-risk 1 --opportunity-cost-real 8 --reason "missed better NFT that 2x'd"
```

**Day 14: Close Position**

```bash
# Sold the NFT
nc update-risk 1 --status closed --realized-value 18
```

**Review: Learn from Outcome**

```bash
# View complete history
nc risks --show-history --show-all

# Analyze:
# - Initial expected value: $25
# - Final realized: $18
# - Opportunity cost: $8 (real)
# - Net: $18 - $10 - $8 = $0 (break even after OC)
```

### Daily Routine Summary

**Morning (5 min):**

1. `nc today` - Review yesterday
2. `nc risks --status open` - Check active risks
3. `nc alpha brief` - Get daily insights (optional)

**Throughout Day:**

- Log activities immediately: `nc log <type> <notes>`
- Update risks as they change: `nc update-risk <id> <options>`

**Evening (10 min):**

1. `nc today` - Review today's entries
2. `nc risks --status open` - Update any risks
3. `nc recent --type action` - Plan tomorrow

**Weekly (30 min):**

1. `nc week` - Weekly summary
2. Review and close completed risks
3. Update improvement statuses
4. Plan next week's improvements

**Monthly (1-2 hours):**

1. Import trading data: `nc import-data trading-performance <file>`
2. Generate outputs for completed projects
3. Review and update monetization paths
4. Plan next month's projects

---

## Best Practices Summary

### Logging

- ✅ Log immediately after activities
- ✅ Use consistent tags
- ✅ Include context and metrics
- ✅ Link to external resources (PRs, issues)

### Risk Tracking

- ✅ Always set initial expected value
- ✅ Track opportunity cost (perceived and real)
- ✅ Update as situations change
- ✅ Close positions when resolved
- ✅ Review history to learn

### Projects

- ✅ Create projects for major initiatives
- ✅ Associate related work
- ✅ Add improvements systematically
- ✅ Generate outputs when complete

### Outputs

- ✅ Complete improvements before generating
- ✅ Review and customize generated content
- ✅ Publish consistently
- ✅ Track engagement and iterate

### Continuous Improvement

- ✅ Review weekly summaries
- ✅ Learn from risk outcomes
- ✅ Update monetization paths
- ✅ Build on previous projects

---

## Troubleshooting

### Database Issues

If you encounter database errors:

```bash
# Database is located at: data/nobody_cares.db
# Delete and recreate if needed (WARNING: loses all data)
rm data/nobody_cares.db
nc today  # Recreates database
```

### Missing Dependencies

```bash
# Reinstall package
pip install -e .

# Install optional dependencies
pip install reportlab  # For PDF generation
```

### Entry Not Found

- Use `nc recent` to find entry IDs
- Check filters: `nc risks --status open`
- Verify project names: `nc project list`

### Common Errors & Solutions

**"Cost must be greater than 0"**

- Use positive numbers: `nc q 100 "bet"` not `nc q -100 "bet"`

**"Probability must be between 0 and 1"**

- Use decimal format: `--my-probability 0.45` not `--my-probability 45`
- Hint: 0.45 = 45%, 0.31 = 31%

**"Invalid entry ID"**

- Check ID exists: `nc recent` or `nc risks`
- IDs are numbers, not names

**Currency formatting issues**

- System handles any currency string: `USD`, `ETH`, `BTC`, `SOL`, etc.
- Gas fees tracked separately if different currency

**Quick mode entries missing context**

- This is expected - add details later: `nc update-risk <id> --odds <odds>`
- System suggests what to add when you review

### Error Handling

The system includes fallbacks for common issues:

- Invalid probabilities default to None (won't break)
- Missing metadata handled gracefully
- Storage errors show helpful messages
- Review prompts won't break if database issues occur

If something breaks:

1. Check error message - it usually has a hint
2. Try the command again (transient errors)
3. Check database: `nc today` (recreates if needed)
4. Review recent changes: `nc recent`

---

## Advanced Usage

### Custom Workflows

You can combine commands for custom workflows:

```bash
# Daily alpha review and action planning
nc alpha brief --output /tmp/brief.md && \
nc alpha actions --urgency high && \
nc today --type alpha
```

### Integration with Other Tools

- Export data: Database is SQLite, can be queried directly
- Import from other sources: Extend importers in `src/importers/`
- Automate logging: Create scripts that call `nc log` commands

---

## Getting Help

- Review this guide for common workflows
- Check command help: `nc <command> --help`
- Examine the codebase for implementation details
- Database schema: See `src/core/storage.py`

---

## Conclusion

This system is designed for **incremental value over time**. The key is consistency:

1. **Log daily** - Build the data foundation (or use quick capture when overwhelmed)
2. **Track risks** - Learn from decisions, capture your intuition
3. **Connect domains** - See patterns across trading, sports, code
4. **Improve projects** - Add value systematically
5. **Generate outputs** - Share and monetize (one source, many outputs)
6. **Review & iterate** - Adapt system to YOUR process

Each step feeds into the next, creating a compounding effect on your skills, portfolio, and opportunities.

### Your Edge System

This isn't generic - it's YOUR system:

- **Captures YOUR intuition** - not just numbers
- **Connects YOUR activities** - sports, trading, alpha, code
- **Learns from YOUR patterns** - not generic advice
- **Adapts to YOUR process** - remove unused, add what you need
- **Works when overwhelmed** - quick capture, add details later

**Remember: Nobody cares until you show them why they should. This system helps you build the proof - YOUR way.**
