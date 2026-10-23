# 30-day retrospective crypto strategy screen (Oct 24 2026)
Research only. No trades, no accounts, no spending. Anchor: request received 2026-10-24 00:27 IDT. Window: 2026-09-24 to 2026-10-23 UTC daily closes. Design frozen BEFORE results (DESIGN.md). Data: MEXC public daily klines (40 coins), cross-checked vs CoinGecko for the decisive series (QNT). All returns are simulated on daily closes; nothing was executed.

## Bottom line
Of 6 pre-registered methods, exactly ONE showed good results this window: weekly top-3 cross-sectional momentum on a broad top-50 basket, +42.7% vs -2.9% equal-weight baseline. It does NOT survive scrutiny as a trustworthy method (below). Everything else was flat-to-negative. The only reliable positive carry remains yield: stablecoin lending ~0.33-0.66%/30d, SOL staking ~0.53%/30d.

## Results table (window Sep 24 - Oct 23 2026)
| method | result | baseline | n | verdict |
|---|---|---|---|---|
| M1 buy&hold BTC | -3.6% | - | 1 asset | negative |
| M1 buy&hold ETH | -10.7% | - | 1 | negative |
| M1 buy&hold SOL | -11.3% | - | 1 | negative |
| M2 7d-SMA trend BTC | -8.8% (12 switches) | -3.6% | 1 | worse than hold |
| M2 7d-SMA trend ETH | -8.5% (8) | -10.7% | 1 | better, still negative |
| M2 7d-SMA trend SOL | -3.2% (6) | -11.3% | 1 | better, still negative |
| M4 dip-buy majors | 0 signals BTC/ETH, 2 SOL | - | 2 | no evidence |
| M3 weekly top-3 momentum | +42.7% | -2.9% EW | 5 rebalances | ONLY positive - see caveats |
| M5 carry (arithmetic) | +0.33-0.66% stable, +0.53% SOL staking | - | - | reliable, small |
| M6 memecoin graduate rule v1 | live paper tracker: 24 closed, ~-72% mean quoted, all positive marks are stale drained-pool quotes | - | 24 | negative |

## The M3 momentum finding, honestly
What the frozen rule did: every 7 days, buy equal-weight the 3 of the 40-asset basket with the best trailing-7-day return, 0.1% cost per position change. Picks: Sep 24 ENA/NEAR/QNT; Oct 1 BTW/PUMP/QNT; Oct 8 OKB/Memecore/USD1 (USD1 = stablecoin picked at 0.0% in an all-red week - rule effectively parked in cash); Oct 15 BTW/NEAR/PEPE; Oct 22 XMR/WLD/PEPE.

Why it is NOT a validated method:
1. ONE name carries it: QNT went ~70 -> ~287 (4x) Sep 24-28 (verified independently on MEXC and CoinGecko). Post-hoc probe excluding QNT: -6.9%.
2. Post-hoc probe on liquid top-20 only: -15.9%. The "edge" lives in long-tail alts where daily-close fills at 0.1% cost are least believable.
3. n = 5 weekly rebalances, 15 position-weeks. 30 days is one regime; this is a description of one lucky-hot window, not evidence the rule repeats.
4. Basket = today's top-50 by market cap (CoinGecko): survivorship-flagged (delisted losers of the window are missing, biasing results up); 8 of 50 excluded as pegged/RWA instruments with no MEXC pair; 2 more (figure-heloc, leo-token) lacked pairs -> 40 assets tested.
5. Execution idealizations: daily-close fills, 0.1% costs, no slippage model on thin books during mania weeks.

What it IS: a pre-registered rule (frozen before results were computed) whose signals were computable in real time, which caught the window's one explosive mover. That is a legitimate descriptive observation and the honest answer to "did anything work in the last 30 days" - with the explicit warning that its entire profit is one token's mania week.

## Files
- DESIGN.md (frozen pre-registration), RESULTS.md (this), fetch+test code embedded in run log, m3_results.json, m3_robustness.json, per-coin series (*.json, source: MEXC klines; QNT cross-verified vs CoinGecko).
