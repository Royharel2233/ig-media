# FROZEN DESIGN - 30-day retrospective crypto strategy screen
Frozen at 2026-10-23T21:30 UTC (Oct 24 00:30 IDT), BEFORE any result is computed.
Research only. No trades, no accounts, no spending. Anchor: Roy's request received 2026-10-24 00:27 IDT = 2026-10-23T21:27Z.

## Window
Trailing 30 days: 2026-09-23T21:27Z to 2026-10-23T21:27Z. Daily close series will be used (CoinGecko market_chart), so effective test grid is UTC daily closes Sep 24..Oct 23.

## What "a method that worked" must mean (frozen acceptance bar)
A method only counts as "worked" if ALL of:
1. Rule is fully specified in advance (no parameters tuned on this window).
2. Signals computable in real time from data available at decision time (no lookahead).
3. Net of modeled costs (fees+slippage, stated per method).
4. Beats its honest baseline (same-window buy-and-hold of the same assets, or stablecoin carry ~0.3-0.7%/30d).
5. Reported WITH: n of independent bets, survivorship/lookahead caveats, and the fact that 30 days cannot validate a method (descriptive, not validated).

## Methods under test (frozen, no additions after results are seen)
M1 Buy-and-hold majors: BTC, ETH, SOL. Baseline.
M2 Trend filter (per major, frozen params): hold when daily close > trailing 7-day SMA of closes, else flat (assume 0% cash). 0.1% cost per switch. No tuning.
M3 Cross-sectional momentum rotation: basket = top 50 non-stablecoin cryptoassets by market cap as of TODAY (survivorship-flagged: today's list, delisted losers missing, results biased UP). Weekly (every 7th day) rebalance equal-weight into top 3 by trailing 7-day return; 0.1% cost per position change. Baseline: equal-weight whole basket, same cost.
M4 Majors dip-buy (frozen): buy when close <= 10% below trailing 7-day high; exit after 7 days or at +5%, 0.15% round-trip cost. Report n of signals (may be 0 - that is a result).
M5 Carry baseline (not a backtest, arithmetic): stablecoin lending 4-8% APY -> 0.33-0.66% per 30d; SOL staking ~6.5% APY -> ~0.53% per 30d.
M6 Memecoin graduate rule v1: NOT re-run here; cite the live paper tracker (currently 24 closed, all-stale-mark wins, mean quoted net ~-72%) as this-window memecoin evidence.

## Data
CoinGecko free API: market_chart (days=31, daily) for BTC/ETH/SOL; /coins/markets top ~100 for basket selection, market_chart daily for basket members (max 50 pulls, rate-limit spaced). Failures documented, not filled.

## Honest reporting requirements
- State n, window, and that 30d is one regime, not validation.
- M3 survivorship bias stated next to every number.
- If nothing clears the bar, the answer is "nothing cleared the bar" plus the carry baseline.
