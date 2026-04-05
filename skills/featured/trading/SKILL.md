---
name: trading-analysis
description: Trigger on requests relating to trading, technical analysis, algorithmic trading, backtesting, or market data evaluation. Uses the comprehensive Trading Agent Skills Library.
---

# Trading Agent Skills Library
> Sourced from [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)
> Selected & consolidated: technical-analyst · trader-memory-core · macro-regime-detector · signal-postmortem · edge-signal-aggregator · edge-strategy-designer

---

## TABLE OF CONTENTS

1. [Technical Analyst](#1-technical-analyst)
2. [Trader Memory Core](#2-trader-memory-core)
3. [Macro Regime Detector](#3-macro-regime-detector)
4. [Signal Postmortem](#4-signal-postmortem)
5. [Edge Signal Aggregator](#5-edge-signal-aggregator)
6. [Edge Strategy Designer](#6-edge-strategy-designer)
7. [Technical Analysis Framework Reference](#7-technical-analysis-framework-reference)
8. [Regime Detection Methodology Reference](#8-regime-detection-methodology-reference)
9. [Outcome Classification Guide](#9-outcome-classification-guide)
10. [Signal Weighting Framework](#10-signal-weighting-framework)

---

## 1. TECHNICAL ANALYST

**Trigger:** User provides chart images and requests technical analysis, trend identification, support/resistance levels, scenario planning, or probability assessments based purely on chart data.

### Core Principles
1. **Pure Chart Analysis** — Base all conclusions exclusively on technical data visible in the chart
2. **Systematic Approach** — Follow a structured methodology for each chart analysis
3. **Objective Assessment** — Avoid subjective bias; focus on observable patterns and data
4. **Probabilistic Scenarios** — Express future possibilities as probability-weighted scenarios
5. **Sequential Processing** — Analyze each chart individually and document findings immediately

### Analysis Workflow

#### Step 1 — Receive Chart Images
- Confirm receipt of all chart images
- Identify number of charts to analyze
- Note any specific focus areas requested
- Proceed sequentially, one chart at a time

#### Step 2 — Analyze Each Chart Systematically

**3.1 Trend Analysis**
- Identify direction: uptrend / downtrend / sideways
- Assess strength: strong / moderate / weak
- Note trend duration and exhaustion signals
- Examine HH/HL or LH/LL pattern

**3.2 Support and Resistance Analysis**
- Mark significant horizontal S/R levels
- Identify trendline S/R
- Note S/R role reversals
- Assess confluence zones

**3.3 Moving Average Analysis**
- Position relative to 20-week, 50-week, 200-week MAs
- MA alignment: bullish / bearish / neutral
- MA slope: rising / falling / flat
- Recent or pending MA crossovers
- MAs acting as dynamic S/R

**3.4 Volume Analysis**
- Overall volume trend: increasing / decreasing / stable
- Volume spikes in context
- Volume confirmation or divergence with price
- Volume climax or exhaustion patterns

**3.5 Chart Patterns and Price Action**
- Reversal patterns: hammers, shooting stars, engulfing
- Continuation patterns: flags, triangles
- Significant candlestick formations
- Recent breakouts or breakdowns

**3.6 Synthesize**
- Integrate all elements into coherent assessment
- Identify most significant factors
- Flag conflicting signals
- Establish key levels determining future direction

#### Step 3 — Develop Probabilistic Scenarios

Each scenario must include:
1. **Scenario Name** — Clear descriptive title
2. **Probability Estimate** — % likelihood (all scenarios must sum to 100%)
3. **Description** — What it entails and how it unfolds
4. **Supporting Factors** — Minimum 2–3 technical factors
5. **Target Levels** — Expected price if scenario plays out
6. **Invalidation Level** — Price that negates this scenario

**Typical Framework:**
- Base Case (40–60%): Most likely outcome based on current structure
- Bull Case (20–40%): Optimistic, requires upside breakout
- Bear Case (20–40%): Pessimistic, requires downside breakdown
- Alternative Scenario (5–15%): Lower probability but technically plausible

#### Step 4 — Generate Analysis Report

Report sections:
1. Chart Overview
2. Trend Analysis
3. Support and Resistance Levels
4. Moving Average Analysis
5. Volume Analysis
6. Chart Patterns and Price Action
7. Current Market Assessment
8. Scenario Analysis (2–4 scenarios with probabilities)
9. Summary
10. Disclaimer

**File naming:** `[SYMBOL]_technical_analysis_[YYYY-MM-DD].md`

### Quality Standards
- Base all analysis strictly on observable chart data
- No external information (news, fundamentals, sentiment)
- No subjective language ("I think", "I feel")
- Express uncertainty clearly when signals are ambiguous
- Present both bullish and bearish possibilities
- Provide specific price levels — not vague descriptions
- Scenarios must be distinct and mutually exclusive

---

## 2. TRADER MEMORY CORE

**Trigger:** "register thesis", "track this idea", "thesis status", "review due", "close position", "postmortem", "trading journal"

### Overview
Persistent state layer that bundles screening → analysis → position sizing → portfolio management into a single thesis object per trade idea. Tracks what you thought, what happened, and what you learned — across conversations.

Phase 1: Single-ticker theses of types: `dividend_income`, `growth_momentum`, `mean_reversion`, `earnings_drift`, `pivot_breakout`

### Thesis Lifecycle

```
IDEA → ENTRY_READY → ACTIVE → CLOSED
                            → INVALIDATED
```

Rules:
- **Forward-only transitions** — no backtracking
- **Raw provenance preserved** — all original screener data kept
- **Atomic writes** — tempfile + os.replace for file safety
- **Git-tracked state** — state/ directory committed for audit trail

### Workflow

**1. Register** — Ingest screener output as thesis
```bash
python3 thesis_ingest.py --source edge-candidate-agent \
  --input reports/signals.json --state-dir state/theses/
```

**2. Query** — Search and list theses
```bash
python3 thesis_store.py --state-dir state/theses/ list \
  --ticker AAPL --status ACTIVE
```

**3. Update** — Manage transitions
- `transition()` → IDEA → ENTRY_READY
- `open_position()` → ENTRY_READY → ACTIVE (only path to ACTIVE)
- `terminate()` → CLOSED or INVALIDATED (computes P&L)
- `mark_reviewed()` → advances next_review_date
- `attach_position()` → links position sizing data
- `link_report()` → cross-references analysis documents

**4. Review** — Check due dates
```bash
python3 thesis_review.py --state-dir state/theses/ \
  review-due --as-of 2026-04-15
```

**5. Postmortem** — Close and reflect
```bash
python3 thesis_review.py --state-dir state/theses/ \
  postmortem th_aapl_div_20260314_a3f1
```
Generates structured postmortem in `state/journal/`. Includes MAE/MFE (Maximum Adverse/Favorable Excursion) if FMP API key available.

**6. Summary statistics**
```bash
python3 thesis_review.py --state-dir state/theses/ summary
```
Shows win rate, average P&L%, per-type breakdown across all closed theses.

### Thesis Object Structure (YAML)
- **Identity:** thesis_id, ticker, created_at
- **Classification:** thesis_type, setup_type, catalyst
- **Lifecycle:** status, status_history
- **Entry/Exit:** target prices, actual prices, conditions
- **Position:** shares, value, risk
- **Monitoring:** review dates, triggers, alerts
- **Origin:** source skill, screening grade, raw provenance
- **Outcome:** P&L, holding days, MAE/MFE, lessons learned

---

## 3. MACRO REGIME DETECTOR

**Trigger:** User asks about macro regime, market regime change, structural rotation, or long-term market positioning.

### Overview
Detect structural macro regime transitions using monthly-frequency cross-asset ratio analysis. Identifies 1–2 year regime shifts for strategic portfolio positioning.

### 6 Components

| # | Component | Ratio/Data | Weight | What It Detects |
|---|-----------|------------|--------|-----------------|
| 1 | Market Concentration | RSP/SPY | 25% | Mega-cap concentration vs market broadening |
| 2 | Yield Curve | 10Y–2Y spread | 20% | Interest rate cycle transitions |
| 3 | Credit Conditions | HYG/LQD | 15% | Credit cycle risk appetite |
| 4 | Size Factor | IWM/SPY | 15% | Small vs large cap rotation |
| 5 | Equity-Bond | SPY/TLT + correlation | 15% | Stock-bond relationship regime |
| 6 | Sector Rotation | XLY/XLP | 10% | Cyclical vs defensive appetite |

### 5 Regime Classifications

| Regime | Characteristics |
|--------|----------------|
| **Concentration** | Mega-cap leadership, narrow market |
| **Broadening** | Expanding participation, small-cap/value rotation |
| **Contraction** | Credit tightening, defensive rotation, risk-off |
| **Inflationary** | Positive stock-bond correlation, traditional hedging fails |
| **Transitional** | Multiple signals but unclear pattern |

### 3-Layer Signal Detection

**Layer 1 — MA Crossover (0–40 pts)**
- Golden Cross: 6M SMA crosses above 12M SMA (recent = 40pts, older = 20pts)
- Death Cross: 6M SMA crosses below 12M SMA
- Converging: SMAs within 1% gap (0–25pts based on proximity)

**Layer 2 — Momentum Shift (0–30 pts)**
- Reversal Signal: 12M ROC negative but 3M ROC positive (or vice versa)
- Acceleration: Strong 3M ROC in same direction as 12M ROC
- Scales linearly with 3M ROC magnitude (capped at 5%)

**Layer 3 — Cross-Confirmation (0–30 pts)**
- Crossover present: +10
- Short-term ROC confirms crossover direction: +10
- SMA gap widening (momentum building): +10

### Component Score Scale

| Range | Interpretation |
|-------|---------------|
| 0–20 | Stable regime, no transition signal |
| 20–40 | Minor fluctuation, possibly noise |
| 40–60 | Transition zone — MAs converging |
| 60–80 | Clear transition — recent crossover |
| 80–100 | Strong confirmed transition |

### Confidence Levels
- **High:** Best regime score ≥ 4
- **Moderate:** Best regime score ≥ 3
- **Low:** Best regime score ≥ 2
- **Very Low:** Best regime score < 2

### Transition Probability

| Signaling Count | Avg Score | Probability |
|----------------|-----------|-------------|
| 4+ | ≥ 50 | High (70–90%) |
| 3+ | ≥ 40 | Moderate (40–60%) |
| 2+ | ≥ 30 | Low (20–40%) |
| < 2 | < 30 | Minimal (<20%) |

### vs Other Skills

| Aspect | Macro Regime | Market Top Detector | Breadth Analyzer |
|--------|-------------|--------------------|--------------------|
| Horizon | 1–2 years | 2–8 weeks | Current snapshot |
| Granularity | Monthly (6M/12M SMA) | Daily (25 days) | Daily CSV |
| Target | Regime transitions | 10–20% corrections | Breadth health |
| API calls | ~10 | ~33 | 0 (free CSV) |

---

## 4. SIGNAL POSTMORTEM

**Trigger:** After closing a trade, reviewing matured signals, identifying false positive patterns, building skill improvement backlog, or running weekly/monthly signal quality audits.

### Overview
Records and analyzes outcomes of trading signals. Compares predicted edge direction against 5-day and 20-day realized returns. Categorizes outcomes and generates feedback for signal aggregator weight adjustments and skill improvement.

### Outcome Categories

| Category | Definition |
|----------|-----------|
| **TRUE_POSITIVE** | Predicted direction matched realized return sign |
| **FALSE_POSITIVE** | Predicted direction opposite to realized return |
| **MISSED_OPPORTUNITY** | Signal not taken but would have been profitable |
| **REGIME_MISMATCH** | Signal failed due to market regime change |
| **NEUTRAL** | \|return\| < 0.5%, too small to classify |

### Classification Decision Tree

```
1. Was the trade taken?
   NO  → If would have been profitable: MISSED_OPPORTUNITY
         Otherwise: SKIPPED (no postmortem)
   YES → Continue

2. Did regime change during holding period?
   YES → Return in wrong direction AND > 2% loss?
         YES → REGIME_MISMATCH
         NO  → Continue
   NO  → Continue

3. Is |return| < 0.5%?
   YES → NEUTRAL
   NO  → Continue

4. Does return sign match predicted direction?
   YES → TRUE_POSITIVE
   NO  → FALSE_POSITIVE (check severity: mild -0.5%→-2%, severe <-2%)
```

### Holding Periods

| Metric | 5-Day | 20-Day |
|--------|-------|--------|
| Purpose | Short-term edge validation | Medium-term edge validation |
| Threshold | 0.5% | 1.0% |
| Weight for feedback | 60% | 40% |

### Workflow

**Step 1 — Record outcome**
```bash
python3 postmortem_recorder.py \
  --signals-file state/signals/aggregated_signals.json \
  --holding-periods 5,20 --output-dir reports/
```

**Step 2 — Generate weight feedback**
```bash
python3 postmortem_analyzer.py \
  --postmortems-dir reports/postmortems/ \
  --generate-weight-feedback --output-dir reports/
```

**Step 3 — Generate skill improvement backlog**
```bash
python3 postmortem_analyzer.py \
  --postmortems-dir reports/postmortems/ \
  --generate-improvement-backlog --output-dir reports/
```

**Step 4 — Summary statistics**
```bash
python3 postmortem_analyzer.py \
  --postmortems-dir reports/postmortems/ \
  --summary --group-by skill,month --output-dir reports/
```

### Attribution Rules
- **Single-source signals:** Full attribution to source skill
- **Aggregated signals:** Attribution proportional to each skill's contribution weight
- **Human override:** Separate analysis track (`human_override = true`)

### Confidence Adjustment Factors

| Factor | Adjustment |
|--------|-----------|
| High volume day | +10% |
| Low volume day | −10% |
| Earnings during holding period | −20% |
| VIX spike > 5 points | −15% |
| Large gap (> 3%) | −15% |

### Key Principles
1. **Honest Attribution** — Every outcome attributed to source skill for accountability
2. **Regime Awareness** — Regime context recorded to distinguish skill failure from market regime shifts
3. **Minimum Sample Size** — Weight adjustments require 20+ signals for statistical validity
4. **Feedback Loop Closure** — Results flow back to improve signal aggregation and skill quality

---

## 5. EDGE SIGNAL AGGREGATOR

**Trigger:** After running multiple edge-finding skills and wanting a unified conviction ranking. Before making portfolio allocation decisions based on multiple signal sources.

### Overview
Combine outputs from multiple upstream edge-finding skills into a single weighted conviction dashboard. Applies configurable weights, deduplicates overlapping themes, flags contradictions, and ranks composite edge ideas by aggregate confidence score.

### Default Skill Weights

| Skill | Weight | Rationale |
|-------|--------|-----------|
| edge-candidate-agent | 0.25 | Primary quantitative signal, least narrative bias |
| edge-concept-synthesizer | 0.20 | Integrates multiple inputs, requires corroboration |
| theme-detector | 0.15 | Narrative momentum |
| sector-analyst | 0.15 | Rotational flows |
| institutional-flow-tracker | 0.15 | Smart money positioning |
| edge-hint-extractor | 0.10 | Suggestive, requires validation |

### Composite Score Formula

```
base_score = Σ(skill_weight × normalized_score) / Σ(skill_weight)
composite  = min(1.0, (base_score + agreement_bonus + merge_bonus) × recency_factor)
```

**Agreement Bonus (additive):**
- 2 skills agree: +0.10
- 3+ skills agree: +0.20

**Merge Bonus:** +0.05 per merged duplicate

**Recency Factor (multiplicative):**
- Within 24h: ×1.00
- 1–3 days: ×0.95
- 3–7 days: ×0.90
- 7+ days: ×0.85

### Deduplication Logic
Two signals are duplicates if direction matches AND either:
1. Ticker overlap ≥ 30% (Jaccard)
2. Title similarity ≥ 60% (word-based Jaccard)

Merge strategy: Keep highest raw score as primary, aggregate contributing skills, boost +5% per merged duplicate.

### Contradiction Detection

| Level | Criteria | Action |
|-------|----------|--------|
| LOW | Different time horizons | Log, no penalty |
| MEDIUM | Same horizon, different skills | Flag, −10% to both scores |
| HIGH | Same skill, opposite signals | Critical alert, exclude from ranking |

### Weight Customization by Style

**Momentum Traders:**
```yaml
edge_candidate_agent: 0.30 | theme_detector: 0.25 | sector_analyst: 0.20
edge_concept_synthesizer: 0.15 | institutional_flow: 0.05 | edge_hint: 0.05
```

**Value/Position Traders:**
```yaml
institutional_flow: 0.30 | edge_concept_synthesizer: 0.25 | edge_candidate: 0.20
sector_analyst: 0.15 | theme_detector: 0.05 | edge_hint: 0.05
```

**Thematic Investors:**
```yaml
theme_detector: 0.30 | edge_concept_synthesizer: 0.25 | sector_analyst: 0.20
edge_candidate: 0.15 | institutional_flow: 0.05 | edge_hint: 0.05
```

### Minimum Conviction Thresholds

| Style | Min Conviction |
|-------|---------------|
| Aggressive | 0.50 |
| Moderate | 0.65 |
| Conservative | 0.80 |

### Workflow

```bash
python3 aggregate_signals.py \
  --edge-candidates reports/edge_candidate_*.json \
  --themes reports/theme_detector_*.json \
  --sectors reports/sector_analyst_*.json \
  --institutional reports/institutional_flow_*.json \
  --min-conviction 0.65 --output-dir reports/
```

### Output
- `edge_signal_aggregator_YYYY-MM-DD_HHMMSS.json` — structured data
- `edge_signal_aggregator_YYYY-MM-DD_HHMMSS.md` — ranked conviction dashboard with provenance, contradictions, and dedup log

---

## 6. EDGE STRATEGY DESIGNER

**Trigger:** When you have `edge_concepts.yaml` and need concrete strategy draft variants with entry/exit specs for multiple risk profiles.

### Overview
Translate concept-level hypotheses into concrete strategy draft specs. Sits after concept synthesis and before pipeline export validation.

### Workflow

1. Load `edge_concepts.yaml`
2. Choose risk profile: `conservative` / `balanced` / `aggressive`
3. Generate per-concept variants with hypothesis-type exit calibration
4. Apply `HYPOTHESIS_EXIT_OVERRIDES` per type:
   - `breakout` — wider stop, higher reward target
   - `earnings_drift` — time-stop after earnings window
   - `panic_reversal` — tight stop, fast take-profit
5. Clamp reward-to-risk at `RR_FLOOR = 1.5` (prevents C5 review failures)
6. Export v1-ready ticket YAML for downstream validation

### Commands

**Generate drafts only:**
```bash
python3 design_strategy_drafts.py \
  --concepts /tmp/edge-concepts/edge_concepts.yaml \
  --output-dir /tmp/strategy-drafts \
  --risk-profile balanced
```

**Generate drafts + exportable tickets:**
```bash
python3 design_strategy_drafts.py \
  --concepts /tmp/edge-concepts/edge_concepts.yaml \
  --output-dir /tmp/strategy-drafts \
  --exportable-tickets-dir /tmp/exportable-tickets \
  --risk-profile conservative
```

### Output
- `strategy_drafts/*.yaml` — one YAML per concept variant
- `strategy_drafts/run_manifest.json` — run summary
- `exportable_tickets/*.yaml` — for downstream `export_candidate.py`

---

## 7. TECHNICAL ANALYSIS FRAMEWORK REFERENCE

### Trend Classification

**Uptrend:** HH + HL pattern, price above key MAs, MAs aligned bullish (shorter > longer)
**Downtrend:** LH + LL pattern, price below key MAs, MAs aligned bearish (shorter < longer)
**Sideways:** No clear pattern, oscillating between defined S/R, flat or intertwined MAs

**Trend Strength:**
- Strong: Clear consecutive HH/LL, minimal retracements, volume confirming
- Weak: Irregular, deep retracements (>50%), price/volume divergence
- Exhaustion Signals: Decreasing momentum on new highs/lows, volume declining, extended distance from MAs, reversal candlestick patterns

### Support & Resistance

**Valid S/R criteria:** Price bounced/rejected 2–3+ times, volume spikes at level, longer timeframe = more weight, round numbers = psychological levels

**S/R Flip:** Broken support → resistance; broken resistance → support (role reversal on retest)

**Strong S/R:** 3+ touches, months to years old, high volume, confluence with Fibonacci/MAs/round numbers

### Moving Averages (Weekly Charts)

- **20-week:** Short-term (~4 months)
- **50-week:** Medium-term (~1 year)
- **200-week:** Long-term (~4 years)

**Golden Cross:** 20W crosses above 50W (bullish)
**Death Cross:** 20W crosses below 50W (bearish)

**Bullish alignment:** 20W > 50W > 200W, all rising
**Bearish alignment:** 20W < 50W < 200W, all falling
**Compressed/converging MAs:** Often precedes significant directional move

### Volume Interpretation

| Price | Volume | Signal |
|-------|--------|--------|
| Rising | Rising | Healthy uptrend |
| Falling | Rising | Healthy downtrend |
| Rising | Falling | Weak uptrend, lack of conviction |
| Falling | Falling | Weak downtrend, possible exhaustion |

**Volume Climax:** Extremely high volume often marks trend extremes
**Bullish Divergence:** New lows but volume declining (selling exhaustion)
**Bearish Divergence:** New highs but volume declining (buying exhaustion)

### Candlestick Patterns

**Bullish Reversal:** Hammer (long lower wick at support), Bullish Engulfing, Morning Star, Double/Triple Bottom

**Bearish Reversal:** Shooting Star (long upper wick at resistance), Bearish Engulfing, Evening Star, Double/Triple Top

**Continuation:** Bull Flag, Ascending Triangle (bullish) | Bear Flag, Descending Triangle (bearish)

**Pattern weight increases when:** At key S/R, accompanied by high volume, confirmed by MAs, occurring on weekly timeframe

### Probability Assignment Framework

| Probability | Criteria |
|-------------|---------|
| High (50–70%) | Aligned with current trend, multiple confirming factors, clear invalidation |
| Medium (25–45%) | Requires trend change or major breakout, some supporting factors |
| Low (5–20%) | Contrary to most technical factors, requires significant structure shift |

### Common Pitfalls
- Overcomplicating with too many indicators
- Ignoring volume
- Forcing patterns that aren't clearly there
- Being too certain (markets are probabilistic)

---

## 8. REGIME DETECTION METHODOLOGY REFERENCE

### Data Pipeline

```
Daily OHLCV (600 days, ~2.4 years)
  → Monthly Downsampling (last business day per month)
  → Ratio Calculation (e.g., RSP/SPY)
  → Moving Average Computation (6M SMA, 12M SMA)
  → 3-Layer Signal Detection
  → Component Scoring (0–100 per component)
  → Weighted Composite (6 components)
  → Regime Classification (decision tree)
  → Transition Probability Assessment
```

**Why monthly frequency:** Regime transitions are structural (1–2 year) phenomena. Daily/weekly data introduces noise.

### Regime Classification Decision Tree

**Concentration** (+2 each): RSP/SPY concentrating, IWM/SPY large-cap-leading, credit stable (+1)

**Broadening** (+2 each): RSP/SPY broadening, IWM/SPY small-cap-leading, credit stable (+1), XLY/XLP risk-on (+1)

**Contraction** (+2 each): Credit tightening, XLY/XLP risk-off, SPY/TLT risk-off (+1)

**Inflationary** (+3): Stock-bond correlation positive, SPY/TLT risk-off (+1)

**Transitional:** 3+ components signaling but no regime scores ≥ 3

### Limitations
1. **Lagging by design** — Monthly frequency = signals appear weeks to months after daily indicators
2. **False positives** — Converging MAs can generate signals that reverse before completing
3. **Regime overlap** — Real markets often exhibit characteristics of multiple regimes simultaneously
4. **Historical bias** — Classification rules derived from post-2000 patterns

---

## 9. OUTCOME CLASSIFICATION GUIDE

### Regime Detection for Classification

- **RISK_ON:** VIX < 20, breadth > 60%, leading stocks advancing
- **RISK_OFF:** VIX > 25, breadth < 40%, defensive rotation
- **TRANSITION:** Mixed signals, high uncertainty

### Sub-categories for FALSE_POSITIVE
- `FALSE_POSITIVE_MILD` — −0.5% to −2% for LONG (or +0.5% to +2% for SHORT)
- `FALSE_POSITIVE_SEVERE` — worse than −2% for LONG (or +2% for SHORT)

### Edge Cases

**Flat Outcome (|return| < 0.5%):** NEUTRAL — does not count as TP or FP

**Early Exit (closed before target holding period):**
- Use actual holding period for return calculation
- Note `early_exit = true`, include reason: stop_loss / target_reached / discretionary

**Gap Events:** Record `gap_event = true`, include `gap_pct`, analyze separately

**Multiple Holding Periods:** A signal can be TRUE_POSITIVE at 5 days but FALSE_POSITIVE at 20 days. Both recorded.

---

## 10. SIGNAL WEIGHTING FRAMEWORK

### Scoring: Confidence Breakdown

| Factor | Weight | Description |
|--------|--------|-------------|
| multi_skill_agreement | 0.35 | How many skills corroborate |
| signal_strength | 0.40 | Average normalized score across contributing skills |
| recency | 0.25 | Time decay adjustment |

### Score Normalization
- 0–1 scale inputs: used as-is
- 0–100 scale inputs: divided by 100
- Categorical grades: A=1.0 / B=0.8 / C=0.6 / D=0.4 / F=0.2
- Missing values: 0.0 (no contribution)

### Best Practices
1. **Regular Weight Tuning** — Review and adjust weights quarterly based on backtested performance
2. **Contradiction Review** — Always manually review HIGH severity contradictions
3. **Provenance Audit** — Periodically trace high-conviction signals back to source data
4. **Diverse Inputs** — Run at least 3 upstream skills before aggregating for meaningful consensus

### Limitations
1. Garbage In, Garbage Out — aggregation quality depends on upstream skill quality
2. Weight Sensitivity — small weight changes can shift rankings significantly
3. No Fundamental Override — aggregator doesn't validate fundamental thesis
4. Temporal Lag — some skills (institutional flow) have inherent reporting delays
