# FORWARD paper tracking - weekly top-3 cross-sectional momentum (FROZEN 2026-10-24)
Authorized by Roy (WhatsApp 2026-10-24 09:42: "בסדר תעקוב"). PAPER ONLY: no trades, no
accounts, no spending. This is FORWARD tracking of the audited rule; it is DISTINCT from
the retrospective 30-day sample (which is not validation) and from the memecoin n25 watch.

## Rule (identical to canonical audit commit 4225410, research/strat30/)
- Universe, reconstructed in REAL TIME at each rebalance: top 50 cryptoassets by market cap
  (CoinGecko /coins/markets), minus pegged/RWA instruments (stablecoins, tokenized funds,
  gold tokens, yield tokens), minus assets with no MEXC USDT daily pair. Universe
  membership is re-derived each rebalance from that day's data - no hindsight list.
- Signal at each weekly rebalance (every 7 days, UTC daily close): rank universe by
  trailing 7-day return (close_t / close_{t-7} - 1); pick top 3, equal weight.
- Execution: at the UTC daily close of the rebalance day (same-close execution; the
  independent audit verified this convention carries no lookahead for daily-close data and
  is a disclosed execution assumption). 0.1% modeled cost per position change.
- Positions held until the next weekly rebalance. Daily marks recorded at each UTC close.
- First rebalance: 2026-10-23 UTC close (completed 2026-10-24T00:00Z, observed after
  completion at ~2026-10-24 09:45 IDT). Anchor day: every 7 days thereafter.

## Honesty constraints (locked)
- Forward results are a SINGLE live sample, not validation; the prior +38.37% retrospective
  was QNT-dependent (ex-QNT -14.77%), 4 rebalances, current-list biased.
- Report daily marks and each rebalance to parent; report n of rebalances with every number.
- If the rule loses, report the loss. No parameter changes after this freeze. Any change
  requires a new frozen design, not an edit.
## Data
- CoinGecko /coins/markets (universe), MEXC /api/v3/klines 1d (prices), CoinGecko
  market_chart as fallback/cross-check. Missing data documented, never filled.
