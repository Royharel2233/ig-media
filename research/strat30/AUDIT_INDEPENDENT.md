# Independent audit of strat30 v2 (2026-10-24, second agent)
Scope: verify arithmetic reproducibility and check for signal/return indexing, candle
timing, turnover cost, baseline and basket errors in the v2 30-day screen (commit 3d3a30d /
b455738). Research only; no trades. Method: reimplemented all computations from scratch
(audit_recompute.py) against the repo's frozen series, then verified the series themselves
against live MEXC klines and CoinGecko market_chart.

## VERIFIED AS CORRECT
- All v2 headline numbers reproduce EXACTLY from the frozen data with independent code:
  M1 BTC -3.52 / ETH -11.12 / SOL -11.42; M2 next -3.81(10sw) / -11.99(6) / -11.06(4),
  same -8.64 / -8.30 / -2.98; M3 next +37.87, same +41.48, exQNT -15.08 / -11.08,
  liquid20 -12.22 / -15.16; EW baseline -7.96 / -3.53. Identical pick logs.
- "same-close" convention carries no lookahead: a signal at close t earns only returns
  from t onward (trade at close t). It is an execution assumption, correctly labeled.
- Candle timing: last completed UTC close at request time (2026-10-23T21:27Z) was the
  candle opened 2026-10-22; all computations correctly exclude the incomplete Oct 23
  candle (stored in the series files but outside the grid).
- Price integrity: every picked asset and major (QNT NEAR ENA PUMP BTW OKB M PEPE XMR WLD
  BTC ETH SOL BCH AAVE) matches live MEXC daily closes to 0.000% on all 29 grid dates.
- QNT mania week confirmed on two independent sources: MEXC 70.69 (Sep 23 close) ->
  286.94 (Sep 27) -> 287.44 (Sep 30); CoinGecko agrees exactly once its daily-series
  date-labeling offset (label d = UTC close of d-1) is applied.
- figure-heloc / leo-token duplicate rows exist only on 2026-10-23 (outside grid): no impact.

## ERRORS FOUND IN v2 (all corrected below; conclusions unchanged)
1. falcon-finance.json holds USDF (Falcon USD, a ~$1.00 stablecoin), not the FF token
   (verified vs live MEXC: matches USDFUSDT 0.000%, deviates from FFUSDT by ~90%).
   A stablecoin sat in the "non-stablecoin" basket and was the Oct 8 pick #3 (-0.13% 7d
   momentum). Corrected: TRON takes the slot.
2. the-open-network.json holds GRAM (GRAMUSDT), not TON (TONUSDT does not exist on MEXC).
   Affected only the liquid-20 probe (GRAM was its Oct 1 pick) and the EW baseline.
   Corrected with true TON daily closes from CoinGecko (date-label offset applied).
3. M4 dip-buy "trailing 7-day high" window in strat30_recompute.py spans 8 days
   (dates[i-7..i]). With a true 7-day window SOL fires 2 signals (Oct 9, Oct 12), not 4.
   BTC/ETH still 0. Conclusion unchanged.
4. figure-heloc (tokenized HELOC, RWA, ~$1.00-1.08) stayed in the basket although the
   frozen design excludes pegged/RWA instruments. Never picked; negligible EW impact.
5. DESIGN.md named CoinGecko market_chart as the data source; the run used MEXC klines.
   A deviation from the frozen design, but the MEXC data verifies as accurate.

## CORRECTED NUMBERS (basket: USDF excluded, true TON substituted)
| series | v2 reported | corrected |
|---|---|---|
| M3 next (PRIMARY) | +37.87% | +38.37% |
| M3 same | +41.48% | +41.45% |
| M3 next ex-QNT | -15.08% | -14.77% |
| M3 liquid20 next | -12.22% | -12.24% (true TON) |
| M3 liquid20 same | -15.16% | -15.14% (true TON) |
| EW baseline next | -7.96% | -8.18% |
| EW baseline same | -3.53% | -3.65% |
| M4 SOL signals | 4 | 2 (Oct 9, Oct 12) |

## MODELING NOTES (disclosed conventions, not errors)
- M3 charges 0.1% x 3 positions at every rebalance even when a pick repeats (QNT carried
  across the first two rebalances): slightly conservative.
- EW baseline charges 0.1% total per rebalance (understates its own turnover): flatters
  the baseline, i.e. conservative for the M3 comparison.
- M3 'next' coverage starts at the Sep 25 close (first execution), M1 at the Sep 24 close;
  EW-next matches M3-next exactly. Final segment Oct 16->22 is 6 days, the others 7.

## VERDICT
The +37.9% headline is arithmetically reproducible (corrected: +38.4%) and every v2
qualitative conclusion stands: the momentum screen's positive result is carried by one
token (QNT, ex-QNT -14.8%), disappears in a liquid-only basket (-12.2%), rests on n=4
weekly rebalances in one regime, and uses a survivorship-flagged basket chosen from
today's top-50. Descriptive, not a validated method. M1/M2/M4 negative or signal-free.
