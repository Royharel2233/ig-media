# Bookkeeping note (2026-11-01, parent-approved, NOT a rule change)

forward_tracker.py now records realized segments at each rotation: outgoing positions'
exit prices at the execution close, segment gross_avg, and a cumulative NAV
(nav = nav_gross_mult x cash_mult). Signals, execution timing (next-bar) and the
0.1%-per-leg cost model are unchanged from the frozen FORWARD_DESIGN.md.

- segments[] entries recorded live have reconstructed=false.
- segments[0] (2026-10-24 -> 2026-10-31) was backfilled 2026-11-01 with
  reconstructed=true; exit prices re-fetched from MEXC 1d klines, ZEC exit
  cross-validated against the recorded re-entry price, NAV verified by
  independent calculation and QA replay of the preserved pre-rotation state.
- nav_gross_mult is the compounded gross factor (1 + segment gross_avg);
  cash_mult is the cost-drag factor only. nav combines them. Entry-day marks of
  0.0 do not touch NAV.
- Overlap treatment (frozen model): a symbol picked in consecutive weeks is
  modeled as sold and rebought; it pays a 0.1% cost leg at rotation like any
  other slot.
