# FORWARD paper tracking - weekly top-3 cross-sectional momentum (FROZEN 2026-10-24)
Authorized by Roy (WhatsApp 2026-10-24 09:42: "בסדר תעקוב"). PAPER ONLY: no trades, no
accounts, no spending. This is FORWARD tracking of the audited rule; it is DISTINCT from
the retrospective 30-day sample (which is not validation) and from the memecoin n25 watch.

## Rule (canonical audit commit 4225410, research/strat30/)
- Universe, reconstructed in REAL TIME at each rebalance: top 50 cryptoassets by market cap
  (CoinGecko /coins/markets), minus pegged/RWA instruments (stablecoins, tokenized funds,
  gold tokens, yield tokens), minus assets with no MEXC USDT daily pair. Universe
  membership is re-derived each rebalance from that day's data - no hindsight list.
- Signal at each weekly rebalance (every 7 days, UTC daily close): rank universe by
  trailing 7-day return (close_t / close_{t-7} - 1); pick top 3, equal weight.
- Execution: NEXT-BAR, matching the audited headline convention: signal computed at UTC
  close t (universe + trailing-7d ranks from completed data), positions entered at UTC
  close t+1 at that close's observed prices. 0.1% modeled cost per position change.
- Positions held until the next weekly execution. Daily marks recorded at each UTC close.
- PROSPECTIVE TIMING (corrected 2026-10-24 after parent review; v1 same-close/backdated
  setup superseded, provenance kept in git): Roy's approval arrived 2026-10-24 09:42 IDT.
  Decision/universe snapshot taken AFTER approval (2026-10-24 ~06:46Z) from the completed
  2026-10-23 close. FIRST ELIGIBLE ENTRY = 2026-10-24 UTC close (future observable price).
  NO holdings or P&L exist before that entry; the 2026-10-23 signal record is labeled
  indicative-only. No backdated fills.
- DISCLOSED DIFFERENCE from the audited retrospective: that test used a FIXED 39-asset
  basket (survivorship-flagged). Forward tracking cannot reconstruct a future-known list,
  so the universe is re-derived in real time at each signal (CG top-50 minus pegged/RWA
  minus no-MEXC-pair). This is the honest forward analogue of the audited rule, not the
  identical test.

## Honesty constraints (locked)
- Forward results are a SINGLE live sample, not validation; the prior +38.37% retrospective
  was QNT-dependent (ex-QNT -14.77%), 4 rebalances, current-list biased.
- Report daily marks and each rebalance to parent; report n of rebalances with every number.
- If the rule loses, report the loss. No parameter changes after this freeze. Any change
  requires a new frozen design, not an edit.
## Data
- CoinGecko /coins/markets (universe), MEXC /api/v3/klines 1d (prices), CoinGecko
  market_chart as fallback/cross-check. Missing data documented, never filled.
