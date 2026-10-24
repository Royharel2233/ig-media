# Ten additional strategies - source registry with primary-text excerpts (v2, 24 Oct 2026)

All URLs fetched today; excerpts are verbatim from the fetched primary text (abstracts/full text where open).
Classification: CANDIDATE = defensible frozen forward paper-test candidate under Roy's constraints (~$1,000, near-passive, research-only). DOCUMENTED = real backtest evidence, not a candidate (reason given). EXCLUDED = not counted as a strategy.

## 1. Weekly reversal - CANDIDATE
Kozlowski, S.E., Puleo, M.R., Zhou, J., "Cryptocurrency return reversals", Applied Economics Letters 28(11), 2021, 887-893.
Open copy: https://digitalcommons.fairfield.edu/cgi/viewcontent.cgi?article=1249&context=business-facultypubs
Excerpt (abstract): "Analyzing a set of 200 cryptocurrencies over the period from 2015 to 2019, we document a significant return reversal effect that holds at the daily, weekly, and monthly rebalancing frequencies and is robust to controls for differences in size, turnover, and illiquidity... we find reversals are most pronounced [in small/illiquid coins]"
Caveats: in-sample ending 2019; effect concentrated in illiquid tail; L-S form needs shorting small caps; long-only liquid version untested; Zaremba et al. (IRFA 2021, below) found daily MOMENTUM in the largest liquid coins; runs opposite to the tracked weekly momentum.
Counter-evidence link: Zaremba et al., "Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets", Int. Review of Financial Analysis, Nov 2021. https://www.sciencedirect.com/science/article/pii/S1057521921002349
Excerpt: "Based on daily prices of more than 3600 coins... the cryptocurrencies with low last day's return significantly outperform their counterparts... the pattern is cross-sectionally dependent on liquidity, and the handful of largest and most tradeable coins exhibit daily momentum rather than a reversal."

## 2. MAX effect - CANDIDATE (weaker; literature split)
"Lottery-like preferences and the MAX effect in the cryptocurrency market", Financial Innovation 7, 2021 (open access). https://link.springer.com/article/10.1186/s40854-021-00291-9
Excerpt (abstract): "weekly average raw and risk-adjusted return differences between portfolios of cryptocurrencies with the highest and lowest MAX deciles are 3.03% and 1.99%, respectively. The results are robust with respect to the differences in size, price, momentum, short-term reversal, liquidity, volatility, skewness, and investor sentiment."
Sample: all coins >$5M cap, 17 growing to 523, Jan 2014 - Sep 2020; t-stats 4.10 / 3.72 (from full text). Sign OPPOSITE to equities.
Conflicts (from the paper itself): Grobys & Junttila (2021, 20 coins) found a negative relation; Jia et al. (2020, 84 coins) negative for positive extreme returns. L-S needs shorting hundreds of coins; long-only liquid version untested.

## 3. Pairs trading - DOCUMENTED, not candidate (intraday, 3-month in-sample)
"Pairs trading in cryptocurrency markets: A comparative study of statistical methods", Investment Analysts Journal 53(2), online Dec 2023. https://www.tandfonline.com/doi/full/10.1080/10293523.2023.2268386
Excerpt (abstract): "We utilise intraday data from 30 cryptocurrencies on the Binance exchange during a three-month period from 1 January 2022 to 31 March 2022... Distance performs well at all three frequencies of 1 minute, 5 minutes, and 60 minutes, with a total return of 208.12%, 236.31%, and 210.36%, respectively."
Note: v1's "documented out-of-sample decay" claim was unsupported by this paper - removed.

## 4. Cross-exchange arbitrage - DOCUMENTED, feasibility UNVERIFIED
Makarov & Schoar, "Trading and Arbitrage in Cryptocurrency Markets", JFE 135(2), 2020. Open copy: https://researchonline.lse.ac.uk/id/eprint/100409/1/Cryptocurrency_Markets_JFE_final_v4.pdf
Excerpt (full text): "the daily average price ratio between the US and Korea from December 2017 until the beginning of February 2018 was more than 15% and reached 40% for several days... the average price difference between Japan and the US was around 10%, and between US and Europe about 3%... the price deviations between exchanges in the same country typically do not exceed 1%... The daily amount of potential arbitrage profits was often more than $75 million."
Data: tick data, 34 exchanges, 19 countries. Paper attributes deviations to capital segmentation (capital controls). Whether capturable at ~$1,000 from Israel: NOT checked against a current venue - left open, not asserted infeasible.

## 5. Listing effect - DOCUMENTED, capture unverified
Li, Luo, Wang & Wei, "Cryptocurrency Listings on Cryptocurrency Exchanges", SSRN 4715718. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4715718
Excerpt (abstract): "cryptocurrency listings on both exchanges see significantly positive short-term returns, the more regulated Coinbase sees significantly higher listing returns than the less regulated Binance... we further construct an exchange regulation index on a larger sample of 80 qualified exchanges, and confirm the relation between stricter exchange regulations and higher short-term listing returns"
Capture requires entry at/before announcement; consistent with our prior front-run-trap finding. Not verified against a current venue.

## 6. Illiquidity premium - DOCUMENTED, weak tier
Fitz, W., "A Reexamination of the Illiquidity Premium in Cryptocurrencies", Utah State University Plan B report, 2021 (NOT peer-reviewed). https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=2640&context=gradreports
Excerpt (abstract): "I examine the illiquidity premium amongst the 372 most actively traded cryptocurrencies from September 2014 to May 2021. I find that the average returns on the most illiquid cryptocurrencies are larger than those on the most liquid cryptocurrencies. My results are robust to different weighting mechanisms for the market index and to various asset pricing model specifications."

## 7. Size factor - DOCUMENTED, in-sample factor; applicability caveat
Liu, Tsyvinski & Wu, "Common Risk Factors in Cryptocurrency", NBER w25882 (pub. Journal of Finance 2022). https://www.nber.org/system/files/working_papers/w25882/w25882.pdf
Excerpt (abstract): "three factors - cryptocurrency market, size, and momentum - capture the cross sectional expected cryptocurrency returns... Nine cryptocurrency factors form successful long-short strategies that generate sizable and statistically significant excess returns." Universe: 1,707 coins >$1M cap.
Applicability: our n=25 new-graduation Solana memecoin tracker (hours-days horizon, Oct 2026) neither contradicts nor confirms - different universe, horizon, cadence, era.

## 8. Futures basis carry - DOCUMENTED; VARIANT of prior-five S2
Schmeling, Schrimpf & Todorov, "Crypto Carry", Management Science, online 6 May 2026. https://pubsonline.informs.org/doi/10.1287/mnsc.2024.05069
Excerpt (abstract): "it can reach exceptionally high levels, sometimes exceeding 40% per annum, with significant variation over time... demand from smaller, trend-chasing investors seeking leveraged exposure and... the limited deployment of arbitrage capital because of regulatory and margin frictions."
Same economic family as S2 funding-rate carry (spot-vs-derivative spread); futures margin/contract requirements not verified.

## 9. Day-of-week effect - DOCUMENTED, anomaly no longer robust
A: "The day of the week effect in the cryptocurrency market", Finance Research Letters 2019. https://www.sciencedirect.com/science/article/pii/S1544612318304240
Excerpt: "The only exception is BitCoin, for which returns on Mondays are significantly higher... most of these results are not significantly different from the random ones and therefore cannot be seen as conclusive evidence against market efficiency."
B: "Revisiting seasonality in cryptocurrencies", Finance Research Letters 2024. https://www.sciencedirect.com/science/article/pii/S1544612324004598
Excerpt: "The evidence on seasonality in cryptocurrency returns is not robust. Although the positive Monday effect for Bitcoin is internally valid, it does not persist in data after 2015... robust across 500 different coins."

## 10. Covered calls on BTC - DOCUMENTED, vendor tier only, access unverified
Anchorage Research, "How to generate bitcoin yield with covered calls". https://www.anchorage.com/insights/how-to-generate-bitcoin-yield-with-covered-calls
Vendor backtest only; no independent academic source found; backtest metrics not verified against primary text; options access/minimum size at ~$1,000 not verified.

## EXCLUDED (not counted)
- Volatility-scaled sizing - overlay, not a strategy: Habeli, Barakchian & Motavasseli, "Adaptive Risk Allocation in Crypto Markets", SSRN 5090097 (Dec 2024). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5090097
  Excerpt: "Volatility scaling increases Sharpe ratios and generates abnormal returns in certain strategies, particularly momentum-based strategies... volatility scaling does not systematically benefit all strategies, and the strongest effects occur in momentum portfolios."
- Low-volatility tilt - CONTRADICTED by its own sources:
  Zhang & Li, "Is idiosyncratic volatility priced in cryptocurrency markets?", Research in International Business and Finance, Dec 2020. https://www.sciencedirect.com/science/article/abs/pii/S0275531920301926
  Excerpt (abstract): "idiosyncratic volatility is positively related to the expected returns of cryptocurrencies... robust to different weighting schemes, holding periods, and sample sizes."
  Burggraf et al., "Cryptocurrencies and the Low Volatility Anomaly", Finance Research Letters 40:101683, 2021. https://doi.org/10.1016/j.frl.2020.101683
  Excerpt (abstract): "Constructing long-short portfolios for a sample of 1,000 cryptocurrencies for the period April 28, 2013 - November 1, 2019, we find no evidence of a significant low volatility premium... popular low volatility strategies do not work in cryptocurrency markets, and even worse, generate negative return" (all 32 J-K buy-sell strategies significantly negative, e.g. 6m/9m -0.299, t=-22.62).
  Note: an independent audit claimed the FRL paper supports low-vol; the primary text above says the opposite. A cited 2026 FRL revisit (10.1016/j.frl.2026.109851) could not be fetched - unverified.
- DCA vs lump-sum - NOT CRYPTO: Vanguard, "Cost averaging: Invest now or temporarily hold your cash?" (equities/bonds). https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf

## Forward-confidence statement (all entries)
Every source is in-sample academic or vendor (samples ending 2018-2022), no live track records, no independent OOS crypto replications verified. No numeric probability of future success is supportable; qualitative tiers only.
