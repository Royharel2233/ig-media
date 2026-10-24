# Polymarket paper-trading pilot - SPEC (no real money, read-only public data)

Genesis: 1792558500 (2026-10-21 04:55 UTC). Owner: Roy. Todo: todo-01M5ECKPM14F87B4B1AH3DKXNV.

## Universe
- Assets: BTC, ETH, SOL, XRP. Series: 5m and 15m "Up or Down" markets.
- Discovery: gamma events endpoint, slug `<asset>-updown-<5m|15m>-<window_start_unix>`.
- Tape: data-api.polymarket.com/trades?market=<conditionId> (full history, taker side, price, size, ts).
- Spot: Coinbase Exchange 1m candles (BTC-USD, ETH-USD, SOL-USD, XRP-USD).
- Settlement: gamma event market outcomePrices when closed=true (max>=0.99), provisional if now>end+1200s and max>=0.995.

## Strategy A - maker near-certain buying (the 0xee65685d class)
- At T-lag seconds before close (A90 primary lag=90, A45 shadow lag=45), look at last tape trade L (stale>60s -> skip).
- If L.price in [min_px, 0.995] (min_px: A90/A45=0.95, A90d shadow=0.90): paper-rest a bid on that outcome.
- Bid proxy: SELL-side ref -> floor(L.price, cent); BUY-side ref -> floor(L.price-0.01, cent); clamp [0.90, 0.99].
- Clip: $15 notional. Fee: 0 (maker). Rebate (estimate, separate line): 20% of tape taker-fee pool * our notional/market volume.
- Fill STRICT (headline): any later trade on same token before close prints strictly below our bid.
  fill_touch flag: any SELL-side print at <= bid (less conservative sensitivity).
- KNOWN LIMIT: queue position unmeasurable from public data; strict rule is a conservative proxy but still
  adversely selects (we "fill" exactly when price trades through us -> clustering with flips).

## Strategy B - taker spot-lag on crypto 5m/15m
- Decision at T-30s. Signal: Coinbase TWAP-to-date (mean of complete 1m candle closes in window) vs
  window-start candle open. Thresholds: B05 primary 0.05%, shadows B02 0.02%, B10 0.10%.
- If |move| >= thr: paper market-buy the move direction. Ask proxy: ref trade BUY-side -> its price;
  SELL-side -> price+0.01 (cap 0.99). Skip if ask proxy outside [0.50, 0.97] or ref stale >45s.
- Clip $15. Taker fee = shares * 0.07 * p * (1-p) (Polymarket docs fee formula, crypto category).
- KNOWN LIMIT: real ask/spread at T-30s not in tape; proxy +-1 tick. Fee is exact.

## Bankroll model (report-time, primary variants only)
$1,000 start, $15 clips, max $250 concurrent open exposure, -$50/day stop. Tail losses included (full -$15 per wrong flip).

## Fees source
https://docs.polymarket.com/trading/fees : fee = C * feeRate * p * (1-p); Crypto taker 0.07, maker 0, maker rebate 20%.

## Cadence & reporting
Hourly collection wake (deterministic replay from genesis possible from public data).
Report to parent: weekly, or A90 settled >=150, or early-dead (A90 net<=-$75 after >=40 settled / B05 net<=-$100 after >=60 settled), or 3 consecutive failed cycles.
