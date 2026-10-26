# Final report source - Polymarket short-window crypto paper pilot (closed 2026-10-26)

Paper only; no real money was or will be traded. Roy approved stopping the pilot on 2026-10-26 19:12 IST.

- App.tsx - source of the PRIVATE final-report File (Instinct Files components, Hebrew).
- report_data.json - the computed series behind the charts (cumulative net per variant sampled every 3h, losses per day, per-variant stats, top loss clusters), derived from ../ledger.jsonl (replay vintage, cycle 130, frozen 2026-10-26 18:34 IST).

Declared results: Strategy A dead on the LIVE vintage 2026-10-22 (150 settled, 140W/10L, -$77.36, pre-registered criterion). Strategy B primary (B05) stopped on its pre-registered criterion 2026-10-26 (190 settled, 155W/35L, -$112.89 replay vintage). B10 underpowered (n=45), neither proven nor disproven. Tested variants all negative does not prove no configuration works. See ../AGGREGATES.md for full vintage-separated aggregates and caveats.
