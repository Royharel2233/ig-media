# Polymarket paper-trading pilot - durable archive (updated 2026-10-26, cycle 130)

Paper only. No real money. Read-only public data (gamma / data-api / Coinbase).
Owner: Roy. Todo: todo-01M5ECKPM14F87B4B1AH3DKXNV. Genesis: 1792558500 (2026-10-21 04:55 UTC).

## Contents
- data/ledger_replay_cycle48_20261023.jsonl - REPLAY-vintage ledger, 19,008 rows, genesis -> cycle 48
  (cursors 5m=1792736700, 15m=1792736100), sha size 5,110,178 bytes.
- data/summary_replay_cycle48_20261023.json - summary at cycle 48.
- data/ledger_replay_cycle99_20261025.jsonl - REPLAY-vintage ledger, cycle 99 snapshot
  (cursors 5m=1792920300, 15m=1792919700), 10,394,931 bytes.
- data/summary_replay_cycle99_20261025.json - summary at cycle 99.
- data/ledger_replay_cycle114_20261026.jsonl - REPLAY-vintage ledger, cycle 114 snapshot
  (cursors 5m=1792975200, 15m=1792974600), post-wipe-4 recovery.
- data/summary_replay_cycle114_20261026.json - summary at cycle 114.
- data/ledger_replay_cycle124_20261026.jsonl - REPLAY-vintage ledger, cycle 124 snapshot
  (cursors 5m=1793010900, 15m=1793010600), post-wipe-5 recovery, 13,033,068 bytes.
- data/summary_replay_cycle124_20261026.json - summary at cycle 124.
- data/ledger_replay_cycle130_20261026.jsonl - REPLAY-vintage ledger, cycle 130 snapshot
  (cursors 5m=1793032200, 15m=1793032200), B05 early-dead trigger cycle.
- data/summary_replay_cycle130_20261026.json - summary at cycle 130.
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


Cycle 99 (2026-10-25 11:30 IST; Israel moved IDT->IST/UTC+2 2026-10-25 02:00) - snapshot files:
  ledger_replay_cycle99_20261025.jsonl, summary_replay_cycle99_20261025.json;
  cursors 5m=1792920300 15m=1792919700:
- A90 391 (360W/31L, -$276.67), A45 193 (182W/11L, -$73.63), A90d 594 (529W/65L, -$543.81),
  B05 146 (121W/25L, -$42.86), B02 323 (273W/50L, -$30.37), B10 38 (33W/5L, -$0.10).
- B-variants partially recovered from the cycle-74 trough (B02 -$40.88 -> -$30.37,
  B10 -$29.17 -> -$0.10) before a correlated sol 5m hit on window 1792917600
  (A45 + B02 + B05, -$15/-$15.34/-$15.34) in cycle 99.
- 2 stale open rows still carried (A45 btc 5m 1792746900, A90d btc 5m 1792757700; resolution
  data still absent from gamma as of cycle 99).


Cycle 114 (2026-10-26 02:42 IST, after wipe-4 recovery) - snapshot files:
  ledger_replay_cycle114_20261026.jsonl, summary_replay_cycle114_20261026.json;
  cursors 5m=1792975200 15m=1792974600:
- A90 457 (422W/35L, -$301.95), A45 215 (204W/11L, -$63.05), A90d 693 (618W/75L, -$620.04),
  B05 153 (128W/25L, -$30.72), B02 359 (305W/54L, -$28.79), B10 39 (34W/5L, +$0.53).
- Wipe #4 (2026-10-26 ~02:32 IST): workspace reset; recovered from this archive (cycle-99
  snapshot) with zero row loss; ~15.7h delta replayed deterministically in 8x2h chunks
  (~9 min total). Fourth wipe overall.
- New losses in the recovered span (cycles 114): A90d eth 5m 1792971000 Down (-$15),
  B02 xrp 5m 1792973700 Up (-$15.11). B10 turned net positive (+$0.53).
- 2 stale open rows still carried (A45 btc 5m 1792746900, A90d btc 5m 1792757700).

Cycle 124 (2026-10-26 12:40 IST, after wipe-5 recovery) - snapshot files:
  ledger_replay_cycle124_20261026.jsonl, summary_replay_cycle124_20261026.json;
  cursors 5m=1793010900 15m=1793010600:
- A90 517 (480W/37L, -$299.40), A45 235 (223W/12L, -$68.38), A90d 776 (697W/79L, -$617.54),
  B05 181 (150W/31L, -$67.49), B02 402 (337W/65L, -$129.97), B10 45 (39W/6L, -$9.87).
- Wipe #5 (2026-10-26 ~12:33 IST): workspace reset; recovered from this archive (cycle-114
  snapshot) with zero row loss; ~8.8h delta replayed deterministically in 5x2h chunks
  (~7 min total). Fifth wipe overall.
- Losses in the recovered span (cycles 115-124): two correlated clusters - 2026-10-26 ~09:00 IST
  Up-flips (9 losses: B02+B05 eth+sol 5m 1792997400, B02 btc+eth 15m + B05 eth 15m 1792998000,
  A45 sol 5m 1792998900, B02 xrp 5m 1792999200; ~-$121 across variants) and xrp 5m 1793006400
  Down hitting all 3 B variants (-$15.36 each); plus A90/A90d xrp+sol 5m 1793008500 Up (3x -$15).
  B02 fell -$28.79 -> -$129.97; B05 -$30.72 -> -$67.49; B10 back negative.
- 2 stale open rows still carried (A45 btc 5m 1792746900, A90d btc 5m 1792757700).

Cycle 130 (2026-10-26 18:34 IST) - B05 EARLY-DEAD TRIGGER - snapshot files:
  ledger_replay_cycle130_20261026.jsonl, summary_replay_cycle130_20261026.json;
  cursors 5m=1793032200 15m=1793032200:
- A90 540 (503W/37L, -$286.70), A45 244 (230W/14L, -$93.64), A90d 811 (729W/82L, -$636.46),
  B05 190 (155W/35L, -$112.89), B02 418 (347W/71L, -$186.79), B10 45 (39W/6L, -$9.87).
- B05 crossed its pre-registered early-dead criterion (net <= -$100 after >=60 settled)
  at cycle 130 (18:34 IST): -$112.89 after 190 settled. Same criterion class as the one
  that declared Strategy A dead on 2026-10-22.
- All six variants net negative on the replay vintage. Losses today arrived in 5 correlated
  clusters (~09:00 x9, ~14:24 x4, ~15:10 x3, ~16:50 x4, ~18:05 x5; windows 1792997400,
  1792998000, 1793006400, 1793008500, 1793014200, 1793016600, 1793017800, 1793023200,
  1793029500, 1793030700). B05 simulated taker fees $30.77 of the -$112.89 net.
- 2 stale open rows still carried (A45 btc 5m 1792746900, A90d btc 5m 1792757700).

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
- Strategy B: B05 (primary) met its pre-registered early-dead criterion 2026-10-26 18:34 IST
  (replay vintage; -$112.89 after 190 settled). B02 shadow -$186.79 / 418 settled; B10 shadow
  -$9.87 / 45 settled (underpowered, neither proven nor disproven). Correlated tail flips
  (multiple assets flipping in one 5-min window) erase accumulated edge on every tested variant;
  no live-trading justification. Untested thresholds are not ruled out by this pilot.

## Standing caveats
Maker fill proxy is conservative AND adverse-selected; taker fee model = shares*0.07*p*(1-p), maker 0;
ask proxy +-1 tick for B; $15 paper clips; correlated tail risk dominates; recommendation remains
paper-only, no live justification, max loss ~$1,000 if Roy ever goes live, near-passive requirement.
