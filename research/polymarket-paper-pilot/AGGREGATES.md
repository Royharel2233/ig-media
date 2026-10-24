# Polymarket paper-trading pilot - durable archive (2026-10-23)

Paper only. No real money. Read-only public data (gamma / data-api / Coinbase).
Owner: Roy. Todo: todo-01M5ECKPM14F87B4B1AH3DKXNV. Genesis: 1792558500 (2026-10-21 04:55 UTC).

## Contents
- data/ledger_replay_cycle48_20261023.jsonl - REPLAY-vintage ledger, 19,008 rows, genesis -> cycle 48
  (cursors 5m=1792736700, 15m=1792736100), sha size 5,110,178 bytes.
- data/summary_replay_cycle48_20261023.json - summary at cycle 48.
- data/pilot.py - collector as of 2026-10-23 (includes --until chunking patch).
- data/SPEC.md - strategy/simulation spec.
- data/AGGREGATES.md - this file.

## DATA VINTAGES (do not merge)
Two sandbox wipes (2026-10-22, 2026-10-23) destroyed the live-collected row-level ledger, and
agent-message attachment blobs proved unrecoverable after workspace reset. What survives:

### LIVE vintage (partial-tape hourly collection) - AGGREGATES ONLY (row-level unavailable)
Cycle 35 milestone (2026-10-22 18:23 IDT, cursors 5m=1792682400, 15m=1792682100):
- A90: 150 settled, 140W/10L (93.3%), net -$77.36. avg entry 0.9665.
- A45: 59 settled, 57W/2L, +$0.52.  A90d: 225 settled, 203W/22L, -$169.84.
- B05: 63 settled, 53W/10L, -$0.08. avg entry 0.8532. B02: 118, 100W/18L, -$6.46. B10: 18, 13W/5L, -$65.56.
Cycle 47 (2026-10-23 06:24 IDT, last live cycle before wipe #2):
- A90 185 (175W/10L, -$58.59), A45 89 (86W/3L, +$0.52), A90d 288 (262W/26L, -$175.22),
  B05 75 (63W/12L, +$2.40), B02 149 (124W/25L, -$40.59), B10 21 (16W/5L, -$50.50).

### REPLAY vintage (complete-tape deterministic replay; ongoing collection continues on it)
Cycle 48 (2026-10-23 09:30 IDT):
- A90 198 (186W/12L, -$82.79), A45 99 (95W/4L, -$10.43), A90d 307 (277W/30L, -$223.48),
  B05 82 (68W/14L, -$19.74), B02 164 (136W/28L, -$45.96), B10 22 (17W/5L, -$48.83).


Cycle 72 (2026-10-24 09:28 IDT) - snapshot files: ledger_replay_cycle72_20261024.jsonl,
  summary_replay_cycle72_20261024.json; cursors 5m=1792823100 15m=1792822500:
- A90 295 (275W/20L, -$156.57), A45 146 (138W/8L, -$51.45), A90d 454 (407W/47L, -$372.59),
  B05 116 (98W/18L, -$1.71), B02 238 (199W/39L, -$31.23), B10 30 (25W/5L, -$29.17).
- Pattern since cycle 48: B05 peaked +$25.04 (cycle 67) then gave back on correlated tail flips;
  A-variant losses keep arriving in same-window clusters (e.g. 7x -$15 in cycle 63, 4x in cycle 61).
- 2 stale open rows carried since ~cycle 55 (A45 btc 5m 1792746900, A90d btc 5m 1792757700).


Cycle 74 (2026-10-24 11:29 IDT, after wipe-3 recovery) - snapshot files: ledger_replay_cycle74_20261024.jsonl,
  summary_replay_cycle74_20261024.json; cursors 5m=1792830300 15m=1792829700:
- A90 301 (279W/22L, -$184.23), A45 150 (142W/8L, -$49.09), A90d 470 (418W/52L, -$435.39),
  B05 119 (99W/20L, -$28.61), B02 248 (207W/41L, -$40.88), B10 30 (25W/5L, -$29.17).
- Wipe #3 (2026-10-24 ~11:27 IDT): workspace reset; recovered from this archive (cycle-72 snapshot)
  with zero row loss; ~2h delta replayed deterministically in one 65s run. Third wipe overall.
- Correlated cluster during the gap: 10 paper losses across 5m windows 1792827000 (x7) and 1792828800 (x3).

## Divergence note (aggregate level only - matched-fill attribution impossible without live rows)
Replay shows equal or more losses per variant over comparable spans (e.g. B05 -$19.74 replay vs
+$2.40 live; A45 -$10.43 vs +$0.52; A90 -$82.79/12L vs -$58.59/10L live at cycle 47). Pattern is
consistent with complete tapes filling a few more (adverse-selected) entries that live collection
skipped while tapes were partially ingested. This is a DATA-VINTAGE effect, not evidence the replay
models live execution better: both vintages share the same fill-proxy bias (strict-below print,
fills cluster with collapses, queue position unmeasurable). Neither vintage measures real maker fills.

## Declared strategy results
- Strategy A (A90 primary): DEAD on the LIVE vintage as originally observed - 150 settled, 140W/10L,
  net -$77.36, pre-registered early-dead criterion (net <= -$75 after >=40 settled) met 2026-10-22
  18:23 IDT. Replay sensitivity alongside: 198 settled, 186W/12L, -$82.79 at cycle 48 (direction unchanged).
- Strategy B variants: roughly break-even (live) to negative (replay); correlated tail flips
  (BTC+ETH+SOL flipping in one 5-min window) erase accumulated edge; no live-trading justification.

## Standing caveats
Maker fill proxy is conservative AND adverse-selected; taker fee model = shares*0.07*p*(1-p), maker 0;
ask proxy +-1 tick for B; $15 paper clips; correlated tail risk dominates; recommendation remains
paper-only, no live justification, max loss ~$1,000 if Roy ever goes live, near-passive requirement.
