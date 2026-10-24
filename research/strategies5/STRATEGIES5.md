# Five candidate strategies - corrected shortlist v2 (2026-10-24)
Research only. No trades, no accounts, no spending. Supersedes v1 (removed unverifiable
probability labels and unsourced numbers; added verified primary-source checks).
Requested by Roy (WhatsApp 2026-10-24 09:42, verified original). Roy's context: ~$1,000
budget, Israel, research/paper-testing only.

## What "evidence" means here
Two tiers, kept separate:
- TIER A - published/external evidence exists (cited with verified URLs). This does NOT
  mean verified by us, does not establish any probability of future profit, and past
  backtests - especially single-author ones - overstate live results.
- TIER B - untested rules: our own hypotheses to paper-test under frozen designs.
Nothing below is a recommendation to trade. Roy authorized research and the existing
momentum paper watch only.

## S1. Tokenized T-bill yield (e.g. OUSG) - TIER A evidence, NOT FEASIBLE for Roy
Verified at primary source (https://ondo.finance/ousg, fetched 2026-10-24): OUSG requires
"Accredited Investor / Qualified Purchaser" onboarding; minimums $5,000 (instant) and
$100,000/$50,000 (standard invest/redeem). That excludes a ~$1,000 retail account, so this
is NOT an actionable method for Roy regardless of its yield (~3.5-4% APY per
https://app.rwa.xyz/assets/OUSG and https://bitcoinyield.co/assets/ousg). Retail stablecoin
"earn" products exist on exchanges but carry counterparty/platform risk and were NOT
verified here - no claim made about them.

## S2. Perpetual funding-rate carry (delta-neutral) - TIER A, single-source, leveraged
One paper: Chan (June 2025), "Leveraged BTC Funding Carry Algorithm"
(https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5292305 - verified): 3x leveraged
long-spot/short-perp, backtested on "three years of high-resolution tick-level data",
reported annualized 16.0%, Sharpe 6.1, max drawdown <2%. Caveats: single-author backtest,
not independently replicated; 3x leverage; results depend on funding staying positive and
on execution quality. Practitioner writeup: Presto Research,
https://www.prestolabs.io/research/optimizing-funding-fee-arbitrage (verified reachable).
Feasibility for Roy: operationally the hardest candidate - perp account, leverage,
liquidation management; on ~$1,000, fees and minimum sizes eat the carry. Paper-testing
from public funding histories is feasible; live use is a separate question entirely.

## S3. Long-horizon trend following on BTC/ETH - TIER A (multi-year horizon)
"A Decade of Evidence of Trend Following Investing in Cryptocurrencies"
(https://ar5iv.labs.arxiv.org/html/2009.12155 - verified) finds trend rules added value
across a decade of crypto data. Also "Dynamic time series momentum of cryptocurrencies"
(https://www.sciencedirect.com/science/article/abs/pii/S1062940821000590 - verified
reachable). These are multi-MONTH/year horizon results. Our own audited 30-day test showed
the FAST variant (7-day SMA) does not beat buy-and-hold. Feasibility: simple to paper-test
forward (frozen 200d-MA monthly rule); needs months before any reading.

## S4. Slow cross-sectional momentum, liquid names, monthly - TIER A with mixed evidence
"Momentum in the Cryptocurrency Market: A Comprehensive Analysis under Realistic
Assumptions", Oxford Review of Asset Pricing Studies
(https://academic.oup.com/raps/advance-article/doi/10.1093/rapstu/raag011/8914819 -
verified). Counterpoint: "Cryptocurrency momentum has (not) its moments", Springer 2025
(https://link.springer.com/article/10.1007/s11408-025-00474-9 - verified) finds the effect
regime-dependent. Our own audit: weekly top-3 momentum was +38.37% descriptively over one
month, driven by one token (ex-QNT -14.77%, liquid-20 -12.24%). Feasibility: paper-testable
at monthly cadence; the weekly variant is already in forward paper tracking.

## S5. Fixed-weight majors portfolio with periodic rebalancing - TIER A, conditional
Hanicova & Vojtko (Dec 2021), "Rebalancing Premium in Cryptocurrencies"
(https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3982120 - verified): daily/monthly
rebalancing of a 27-crypto portfolio improved return, volatility and drawdowns vs
buy-and-hold in their sample. The AUTHORS' OWN caveat: the premium depends on no single
asset consistently outperforming the others; otherwise "rebalancing might not be as
profitable". Costs and baseline choice matter (frequent rebalancing adds fees).
Feasibility: trivially paper-testable (frozen weights, weekly rebalance, vs B&H baseline).

## Bottom line (no padding)
- Actionable-and-evidence-backed under Roy's constraints: S3, S4, S5 as forward PAPER
  tests only. S2 as a data-only paper study if exchange access is irrelevant to the test.
- S1 is real but inaccessible (qualified purchaser, $5K+ minimums).
- None of the five is established as likely-profitable for the next 30 days; anyone who
  promises that is selling something. The honest deliverable is the frozen paper tests.
- No new watches started for S2-S5. Existing watches unchanged: forward weekly momentum
  (first entry 2026-10-24 UTC close), memecoin n=25 tracker.
