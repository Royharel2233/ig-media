# 30-day retrospective crypto strategy screen - AUDIT v2 (Oct 24 2026)
Research only. No trades, no accounts, no spending. Supersedes RESULTS_v1_superseded.md
(v1 used the incomplete 2026-10-23 UTC candle as a "close" and let a stablecoin into the
basket; corrected here. v1 kept for audit trail only - do not cite its numbers).

## Window and data (verified against raw timestamps)
Request received 2026-10-23T21:27Z. At that moment the 2026-10-23 UTC daily candle was
INCOMPLETE, so it is excluded. Test grid: UTC daily CLOSES 2026-09-24 .. 2026-10-22
(29 closes; candle opened date d 00:00Z closes at d+1 00:00Z, all complete before request).
Sources (public, no keys):
- MEXC klines: GET https://api.mexc.com/api/v3/klines?symbol={SYM}USDT&interval=1d&limit=40
  (rows [open_time_ms, open, high, low, close, volume, ...]; close used).
- Basket list: CoinGecko GET https://api.coingecko.com/api/v3/coins/markets (top 50 by mcap).
- QNT cross-check: CoinGecko GET https://api.coingecko.com/api/v3/coins/quant-network/market_chart?vs_currency=usd&days=31&interval=daily
Basket: 41 non-stablecoin assets (50 top-list minus 9 pegged/RWA: BUIDL, global-dollar,
hashnote-usyc, ondo-us-dollar-yield, pax-gold, ripple-usd, spiko-amundi, tether-gold,
USD1 - v1 error let USD1 in and the rule "picked" it Oct 8). SURVIVORSHIP-FLAGGED: today's
top-50 list, delisted losers of the window missing, results biased UP.

## Execution timing (explicit, per audit)
Signals use closes up to and including day t. PRIMARY convention "next": trade at the NEXT
close (t+1) - no same-close fills. "same" (trade at close t) reported only as the idealized
variant. The 2026-10-22 signal would execute 2026-10-23, outside verified data, so the
primary run has 4 executed rebalances; the idealized run has 5.
Costs: 0.1% per position change (frozen in DESIGN.md). No slippage model on thin books.

## Results (AUDIT v2, grid Sep 24 - Oct 22 2026)
| method | next-bar (PRIMARY) | same-close (idealized) | baseline | verdict |
|---|---|---|---|---|
| M1 B&H BTC | -3.5% | - | - | negative |
| M1 B&H ETH | -11.1% | - | - | negative |
| M1 B&H SOL | -11.4% | - | - | negative |
| M2 7d-SMA BTC | -3.8% (10 switches) | -8.6% | -3.5% | no better than hold |
| M2 7d-SMA ETH | -12.0% (6) | -8.3% | -11.1% | no better than hold |
| M2 7d-SMA SOL | -11.1% (4) | -3.0% | -11.4% | no better than hold |
| M4 dip-buy | 0 signals BTC/ETH, 4 SOL | - | - | no evidence |
| M3 weekly top-3 momentum | +37.9% (4 rebalances) | +41.5% (5) | EW basket -8.0% (next) / -3.5% (same) | positive ONLY pre-robustness |
| M3 ex-QNT probe | -15.1% | -11.1% | - | collapses |
| M3 liquid-top-20 probe | -12.2% | -15.2% | - | collapses |

Key correction vs v1: M2's apparent improvement on ETH/SOL was an ARTIFACT of same-close
execution timing. Under honest next-bar execution the trend filter does not beat buy-and-hold
on any major. M3 headline softens 42.7% -> 37.9% and its ex-QNT probe worsens -6.9% -> -15.1%.

## The M3 momentum finding, honestly (v2)
Picks (signal date / execution date): Sep 24->25 QNT, NEAR, ENA; Oct 1->2 QNT, PUMP, BTW;
Oct 8->9 OKB, Memecore, FF; Oct 15->16 BTW, NEAR, PEPE. Oct 22 signal (XMR, WLD, PEPE)
unexecutable within verified data.
Why it is NOT a validated method:
1. ONE name carries it: QNT ~70 -> ~287 (4x) Sep 24-28 (verified on both MEXC and CoinGecko).
   Excluding QNT: -15.1% (next-bar). The "edge" is one token's mania week.
2. Restricted to liquid top-20: -12.2%. The apparent edge lives in long-tail alts where
   daily-close fills at 0.1% cost are least believable.
3. n = 4 executed weekly rebalances (12 position-weeks). 30 days is one regime.
4. Basket chosen from TODAY's known top-50: survivor selection bias upward.
5. Freezing the design before COMPUTING results is not genuine historical pre-registration:
   the window's broad market history was known to the analyst; there is no train/test
   separation and no out-of-sample validation. All numbers are descriptive, never validated.

## Carry / staking (withdrawn as a "reliable positive")
v1 called stablecoin yield (~0.33-0.66%/30d) and SOL staking (~0.53%/30d) "the only reliable
positive". WITHDRAWN: those are advertised annualized rates converted arithmetically, not
realized 30-day total returns. SOL staking over this window would have returned roughly
-11.4% (price) + 0.5% (yield) ~ -10.9%. Stablecoin lending carries depeg, credit, lockup and
platform risk that this screen did not verify; no realized-return claim is made.

## M6 (memecoin graduate rule v1)
Live paper tracker, unchanged: 24 closed trades, mean quoted net ~-72%, all positive marks
are stale drained-pool quotes (see ACCOUNTING.md in the archive).

## Files (standalone, executable)
- strat30_fetch.py - data fetcher (endpoints above; MEXC primary, CoinGecko basket+cross-check)
- strat30_recompute.py - audit-v2 computation (this table), reads the per-coin JSONs
- strat30_v2_results.json - full machine-readable v2 output incl. pick log
- DESIGN.md (frozen design), RESULTS_v1_superseded.md (audit trail),
  m3_results.json / m3_robustness.json (v1 artifacts, superseded), per-coin series (*.json)
