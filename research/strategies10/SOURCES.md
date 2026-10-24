# Ten additional strategies - source registry v3 (24 Oct 2026)
All URLs fetched today; excerpts verbatim from primary text. The File page (v3) shows ten methods WITH positive backtest evidence; rejected candidates are in a separate exclusions appendix.


> v4 (24 אוקטובר 2026, ~11:37 IDT): עודכן בעקבות ביקורת v3. שמונה שיטות במקום עשר (ניסיון כפול כובס: תיזמון MA נכלל במשפחת המומנטום, סקיונס ב-MAX). פרטי מדגם OOS של Guidolin-Ionta חולצו מהטקסט הפתוח (ינואר 2018 - אפריל 2025, 382 תצפיות, 40 מטבעות, מדד ייחוס CMBI10); הגדלים המספריים בטבלאות אינם ניתנים לחילוץ טקסט בעותק הפתוח וסומנו כלא-מאומתים מספרית.


## THE TEN (positive backtest evidence)
1. Weekly reversal - Kozlowski, Puleo & Zhou, Applied Economics Letters 28(11) 2021. https://digitalcommons.fairfield.edu/cgi/viewcontent.cgi?article=1249&context=business-facultypubs
   "Analyzing a set of 200 cryptocurrencies over the period from 2015 to 2019, we document a significant return reversal effect that holds at the daily, weekly, and monthly rebalancing frequencies and is robust to controls for differences in size, turnover, and illiquidity."
   Caveats: effect strongest in illiquid tail; L-S needs shorting small caps; long-only liquid version untested; Zaremba et al. IRFA 2021 (3600+ coins) found daily MOMENTUM in the largest liquid coins.
2. MAX effect - Financial Innovation 7, 2021 (open). https://link.springer.com/article/10.1186/s40854-021-00291-9
   17-523 coins >$5M, Jan 2014-Sep 2020. Weekly high-minus-low MAX decile: 3.03% RAW return difference; 1.99% three-factor regression alpha (risk-adjusted; NEITHER nets trading costs). t=4.10/3.72. Sign opposite equities. Conflicts: Grobys & Junttila 2021 (20 coins) negative.
3. Sentiment + on-chain factors (OOS) - Guidolin & Ionta, JIFMIM 107 (2026) 102285 (open). https://iris.unibocconi.it/retrieve/ca0d5636-301d-4177-b28c-1e88a6b6cdb1/Guidolin%20and%20Ionta%20JIFMIM%202026.pdf
   "three weekly factor-mimicking portfolios based on network activity (active users), computing intensity (hashrate), and a sentiment measure from Google search trends. Using an out-of-sample forecasting framework, we find that all three predictors show strong performance across 40 cryptocurrencies. The certainty equivalent returns are often well above the risk-free rate." Sample Aug 2015-Apr 2025.
4. Price-to-MA ratio timing (OOS) - Detzel, Liu, Strauss, Zhou & Zhu, Financial Management 50(1) 2021. https://ideas.repec.org/a/bla/finmgt/v50y2021i1p107-137.html
   "ratios of prices to their moving averages forecast daily Bitcoin returns in and out of sample. Trading strategies based on these ratios generate an economically significant alpha and Sharpe ratio gains relative to a buy-and-hold position." Family note: adjacent to trend/momentum.
5. Higher moments / skewness - Jia, Liu & Yan, FRL 39, 2021. https://ideas.repec.org/a/eee/finlet/v39y2021ics1544612320303135.html
   "volatility and kurtosis are positively related to future returns while the return predictability of skewness is negative... cryptocurrency investors have lottery-type preferences." 84 coins, intraday data.
6. Low-volatility tilt - Pyo & Jang, "Revisiting the low-volatility anomaly in cryptocurrency markets", FRL 97, 2026. https://ideas.repec.org/a/eee/finlet/v97y2026ics1544612326003818.html
   "we document a statistically and economically meaningful low-volatility premium in the post-2017 period... robust to controlling for market-wide cryptocurrency exposure, excluding extreme Bitcoin market episodes, and restricting the sample to a fixed cohort of pre-2019 listed assets."
   CONFLICT disclosed: Burggraf et al. FRL 2021 (1,000 coins, Apr 2013-Nov 2019): "we find no evidence of a significant low volatility premium... popular low volatility strategies do not work in cryptocurrency markets, and even worse, generate negative return." Zhang & Li RIBAF 2020: ivol POSITIVELY related to returns. Era-split per 2026 paper's market-maturation interpretation. Worker verified Burggraf against an independent reviewer who initially inferred support from the title; reviewer confirmed worker right.
7. Size factor - Liu, Tsyvinski & Wu, NBER w25882 (JF 2022). https://www.nber.org/system/files/working_papers/w25882/w25882.pdf
   "three factors - cryptocurrency market, size, and momentum - capture the cross sectional expected cryptocurrency returns... Nine cryptocurrency factors form successful long-short strategies." 1,707 coins >$1M, 2014-2018. Applicability: our memecoin tracker sample differs (universe/horizon/cadence/era) - no contradiction, no equivalence.
8. Pairs trading - Investment Analysts Journal 53(2), online Dec 2023. https://www.tandfonline.com/doi/full/10.1080/10293523.2023.2268386
   "intraday data from 30 cryptocurrencies on the Binance exchange during... 1 January 2022 to 31 March 2022... Distance performs well at all three frequencies of 1 minute, 5 minutes, and 60 minutes, with a total return of 208.12%, 236.31%, and 210.36%, respectively." 3-month in-sample; intraday execution.
9. Intraday BTC predictability - Bouri, Lau, Saeed, Wang & Zhao, IRFA 76, 2021. https://centaur.reading.ac.uk/97607/1/Bitcoin_Functional_Accepted.pdf
   "the results provide evidence of profitable trading opportunities based on intraday trading strategies, which confronts the efficient market hypothesis." Intraday execution; episodic predictability.
10. Listing effect - Li, Luo, Wang & Wei, SSRN 4715718. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4715718
    "cryptocurrency listings on both exchanges see significantly positive short-term returns, the more regulated Coinbase sees significantly higher listing returns than the less regulated Binance." Capture unverified (front-run trap finding).

## EXCLUSIONS APPENDIX (not counted in the ten)
- Illiquidity premium - Fitz, Utah State 2021 (Plan B report, not peer-reviewed). https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=2640&context=gradreports - "the average returns on the most illiquid cryptocurrencies are larger than those on the most liquid" (372 coins, 2014-2021). Tier too weak for the ten.
- Cross-exchange arbitrage - Makarov & Schoar JFE 2020. Documented phenomenon (Kimchi >15% avg, peak 40%; within-country <1%), not a strategy backtest; capture unverified.
- Futures basis carry - "Crypto Carry", Management Science 2026 (>40% p.a. at times). Same economic family as prior-five S2 funding carry - variant.
- Covered calls - Anchorage vendor only; no verified primary-text numbers; access unverified. Reviewer-verified working URL: https://www.anchorage.com/insights/synthetic-yield-on-bitcoin-implementation-discipline-and-performance-boundaries-of-systematic-covered-call-writing (the v1/v2 link slug was wrong).
- Day-of-week effect - FRL 2019 documented; FRL 2024 revisit (500 coins): not robust, gone after 2015. Dead anomaly.
- Volatility-scaled sizing - SSRN 5090097. Risk overlay on existing methods (strongest on momentum portfolios), not a strategy.
- DCA vs lump-sum - Vanguard, equities/bonds. Not crypto.

## Forward-confidence statement
Eight of ten are in-sample only; only 3 and 4 have out-of-sample evidence. No live track records. Historical success rate is not a future success probability; no numeric probability is supportable.
