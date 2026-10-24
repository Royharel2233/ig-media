# Five additional strategies judged worth forward paper-testing (2026-10-24)
Research only. No trades, no accounts, no spending. Requested by Roy (WhatsApp 2026-10-24
09:42, verified original): "find 5 more you believe with high probability will return money".
Interpretation (main): five STRATEGIES, not tokens.

## Honesty header (read first)
"High probability of returning money" must be qualified honestly:
- Only ONE candidate below has a genuinely high probability of a positive NOMINAL return
  (and it pays ~0.3%/month for it). Nothing in crypto offers high probability AND high return.
- Three others have real published evidence but only over multi-month/year horizons, with
  losing months along the way. One is structural but operationally risky.
- None of these is validated by us. Each gets a frozen paper test before any claim.
- What we will NOT recommend (own data): memecoin graduation buying (n=25 paper trades,
  corrected mean -70.7%, zero execution-verified wins), fast 7-day trend filters (failed
  our audited 30-day test), grid trading bots, airdrop farming.

## S1. Tokenized T-bill / RWA carry (cash-like yield)
Claim: buy-and-hold a tokenized US T-bill fund (OUSG, BUIDL, USYC class).
Evidence: live yields published - OUSG ~3.56% APY (bitcoinyield.co/assets/ousg, rwa.xyz).
Probability of positive nominal USD return: HIGH (it is a money-market instrument), return
~0.3%/month. Risks: issuer/custody/smart-contract/depeg/regulatory; access restricted
(qualified purchasers for OUSG). This is yield on cash, not a trading method - and it is
the honest answer to "what most reliably returns money".
Paper test: track published daily yield accrual vs T-bill rate; monitor depeg/discount events.

## S2. Perpetual funding-rate carry (delta-neutral basis)
Claim: long spot BTC/ETH + short the perp when funding is positive; collect funding.
Evidence: SSRN "Leveraged BTC Funding Carry Algorithm" (papers.ssrn.com abstract_id=5292305);
Presto Research "Optimizing Funding Fee Arbitrage" (prestolabs.io). Structural: perp funding
is positive in most bullish/neutral regimes; typical 5-15% annualized, regime-dependent.
Risks (material): funding flips negative for weeks (carry goes negative), liquidation and
exchange/counterparty risk, borrow/fees, execution skill. NOT a free lunch - operationally
the hardest one here. Probability of positive return over a year: moderate-high; over a
month: genuinely uncertain.
Paper test: replay public funding histories (Binance/Bybit funding APIs) with realistic
fees; track a simulated daily P&L series forward from a frozen start date.

## S3. Long-horizon trend following on BTC/ETH (200-day MA / 12-month time-series momentum)
Claim: hold only when price > long-horizon trend; else cash. Monthly decisions.
Evidence: "A Decade of Evidence of Trend Following Investing in Cryptocurrencies"
(arXiv 2009.12155); "Dynamic time series momentum of cryptocurrencies" (ScienceDirect
S1062940821000590). This is the horizon where crypto trend evidence actually exists - our
own audited test showed the FAST version (7-day SMA) does NOT work (-3.8 to -12% in 30d).
Risks: whipsaw drawdowns in sideways markets; works over years, will lose some months.
Probability of beating hold over a full cycle: moderate (published evidence), over 30 days:
no better than coin-flip - say so.
Paper test: frozen rule (200d MA, monthly check), forward paper track vs B&H baseline.

## S4. Slow cross-sectional momentum, liquid names only (monthly formation)
Claim: monthly rotation into the top-5 liquid alts by trailing 30-day return.
Evidence: "Momentum in the Cryptocurrency Market: A Comprehensive Analysis under Realistic
Assumptions" (Oxford Review of Asset Pricing Studies, raps/raag011); caveat: "Cryptocurrency
momentum has (not) its moments" (Springer 2025) shows the effect is regime-dependent and
weakened post-2018. Connects to our audit: weekly top-3 momentum was +38.37% descriptively
but collapsed ex-QNT (-14.77%) and in the liquid-20 (-12.24%) at the weekly horizon.
Risks: crowded reversals, regime dependence, our own data contradicts the fast variant.
Paper test: monthly cadence, liquid-only, frozen; forward track next to the weekly tracker.

## S5. Fixed-weight majors portfolio with periodic rebalancing (volatility harvesting)
Claim: e.g. 50/50 BTC/ETH (or 40/40/20 BTC/ETH/SOL), rebalanced weekly back to weights.
Evidence: "Rebalancing Premium in Cryptocurrencies" (SSRN abstract_id=3982120); INSEAD
"The Rebalancing Premium" (sites.insead.edu did=57836). The premium is real in volatile
sideways markets (sells high/buys low mechanically); it UNDERPERFORMS buy-and-hold in
strong trends. Not alpha - a disciplined compounding/risk method.
Risks: trend risk, fee drag if rebalanced too often, tracking error vs hold.
Paper test: frozen weights + weekly rebalance, forward track vs B&H and vs S3.

## Proposed forward program (paper only)
- S1: data track (yield accrual), no simulated trading needed.
- S2-S5: freeze one-page designs (rule, universe, costs, baseline) BEFORE any test, like
  the audited momentum design; forward paper track from a fixed start; weekly report.
- Every number reported with n of periods and regime caveats. Losses reported as-is.
- Nothing here authorizes spending; any future live consideration is a separate explicit
  user decision with risk disclosures.
