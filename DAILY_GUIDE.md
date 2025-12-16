# Daily Guide: Nobody Cares - Daily Improvement Hub

A comprehensive guide to using this repository for tracking daily activities, building skills portfolios, analyzing performance, and generating shareable artifacts.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Daily Workflow](#daily-workflow)
3. [Entry Types & Best Practices](#entry-types--best-practices)
4. [Project Management](#project-management)
5. [Risk Tracking](#risk-tracking)
6. [Alpha Brief Generation](#alpha-brief-generation)
7. [Trading Performance Import](#trading-performance-import)
8. [Improvement Tracking](#improvement-tracking)
9. [Output Generation](#output-generation)
10. [Workflow Integration](#workflow-integration)

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

1. **Log daily** - Build the data foundation
2. **Track risks** - Learn from decisions
3. **Improve projects** - Add value systematically
4. **Generate outputs** - Share and monetize
5. **Iterate** - Build on previous work

Each step feeds into the next, creating a compounding effect on your skills, portfolio, and opportunities.

**Remember: Nobody cares until you show them why they should. This system helps you build the proof.**
