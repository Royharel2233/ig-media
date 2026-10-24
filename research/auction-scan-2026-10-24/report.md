# Auction scan — 2026-10-24 (v6, verified)

Scan executed 2026-10-24, verified through 12:50 IDT. Sources: il.bidspirit.com portal (109 auction links enumerated), cars.bidspirit.com receiver portal (236 vehicles), govil house page, kones.co.il (via web_fetch; Cloudflare blocks the cloud browser). **Coverage: 12 catalogs in Roy's categories parsed in full (4,059 lots, data/all_catalog_lots.csv) — not the whole portal.**

## Verified terms and rates (24.10)

- Commissions, verified on each house's lot pages: masoret 10% + VAT (when paying within 3 days; standard terms text says 15%; +1.5% for credit card), gallery74 19% + VAT, empire 20% + VAT.
- VAT is 18% on the commission only (masoret lot-page note + gov.il decision 1270, 18% from 2025).
- All-in multipliers on the hammer: masoret ×1.118, gallery74 ×1.2242, empire ×1.236.
- Dealer payout benchmark: goldtrade.co.il live calculator pays ₪2,152 for 10g of 14K = 92.3% of its own melt table → ~$69.2/g for 14K, ~$88.6/g for 18K. USD/ILS ₪3.11 (their table, 24.10). Gold ~$3,996/oz corroborated by the same table; silver $53.92/oz is exa.ai-only (not an owning source).
- Bidspirit mechanics: a "leading bid" below the opening price is a non-winning absentee-bid artifact. Effective floor = max(opening, lead).
- masoret freezes early bids on Shabbat/holidays; bidding resumes Saturday night.
- masoret catalog 82241 carries a house banner about **item 15 only** (winner chooses the item or $1,000 cash offset; item 15 opens live at $10; no early bids on that item). Verified on the lot pages of items 106/107/108: the banner is catalog-wide boilerplate, the special terms apply to item 15 only. Our watch lots are ordinary early-bid lots.

## Headline (coverage-scoped)

Within the 12 catalogs checked, no sale closing this weekend shows a verified gap below melt. Four lots closing Nov 1–2 are on the watch list below. Nothing here is a confirmed bargain: all weights/purity are seller claims, photos cannot verify gold, and no margin is confirmed without physical inspection.

## Watch list — break-even framing (closes Nov 1–2)

Break-even = verified grams of gold needed for scrap payout alone to return the current all-in cost, before inspection/pickup costs. Seller gross weight is shown separately; it includes movement, glass, stones, pearls, strap. Unknown case construction/authenticity → no confirmed margin at any of these.

| Sale | Closes | Lot | Item (seller claims) | Lead now | All-in now | Break-even verified gold | Seller gross weight |
|---|---|---|---|---|---|---|---|
| masoret 82241 | Mon 2.11, site shows 18:00 * | #106 | 14K white-gold antique pocket watch | $130 | $145 | ~2.1g 14K | 57.39g |
| masoret 82241 | Mon 2.11, site shows 18:00 * | #107 | Omega pocket watch + 14K rope chain (worked, stopped) | $240 | $268 | ~3.9g 14K | 28.5g |
| masoret 82241 | Mon 2.11, site shows 18:00 * | #108 | 14K Exactus wristwatch, working | $80 | $89 | ~1.3g 14K | 9.4g |
| empire 81753 | Sun 1.11, site shows 18:00 * | #205 | 18K MARVIN mechanical, working | $325 | $402 | ~4.5g 18K | 13g |

Verified lot links (opened and title-checked 24.10):
- #106: https://il.bidspirit.com/ui/lotPage/masoret/source/catalog/auction/82241/lot/59039/%D7%A9%D7%A2%D7%95%D7%9F-%D7%9B%D7%99%D7%A1-%D7%9E%D7%96%D7%94%D7%91-14-%D7%9C%D7%91%D7%9F-%D7%A2%D7%AA%D7%99%D7%A7?lang=he
- #107: https://il.bidspirit.com/ui/lotPage/masoret/source/catalog/auction/82241/lot/59274/%D7%A9%D7%A2%D7%95%D7%9F-%D7%9B%D7%99%D7%A1-omega?lang=he
- #108: https://il.bidspirit.com/ui/lotPage/masoret/source/catalog/auction/82241/lot/59279/%D7%A9%D7%A2%D7%95%D7%9F-%D7%9E%D7%96%D7%94%D7%91-14?lang=he
- masoret catalog: https://il.bidspirit.com/ui/catalog/auction/masoret/82241?lang=he
- empire catalog: https://il.bidspirit.com/ui/catalog/auction/empireauctions/81753?lang=he

## Checked this weekend — status

- **rimon 80951 (silver, closes Mon 26.10):** all 360 parsed lots lead at 1.16–1.30x melt. Priced above metal. Out.
- **behrooz 80869 (closes Wed 28.10):** gold items lead at 0.80–0.98x melt before commission. Net margin after commission and payout is unverified — unresolved, not an established rejection.
- **gallery74 79495 #6533 (14K pendant with pearl + stones, 14g gross, closes Sun 25.10):** the $700 lead is a real bid. All-in $857. Break-even requires ~12.4g verified gold out of 14g gross including the pearl and stones. Neither confirmed nor ruled out — the pearl's weight is unknown. Unverified value gap, not an established rejection and not an opportunity.

## Timezone caveat (applies to every bidspirit time here)

Israel DST ends tonight (25.10). There is a display/timestamp conflict on bidspirit: fa-firm shows 10:00 while its own startDate 2026-10-25T07:00Z converts to 09:00 IST under Asia/Jerusalem zoneinfo (same one-hour gap on hob-cars, federlaw, cflaw). The evidence does not establish which reading the sale engine follows. Dates are consistent in both readings; exact hours are NOT verified. * Exact opening/closing hours must be confirmed with the auction house before participation; on closing days we watch from 16:00 and treat displayed-minus-1h as the earliest possible close. The kones tender deadline (28.10 12:00) is wall-time text on the kones page, not a UTC conversion.

## Receiver vehicles (asking-price anchors, not transactions)

12 live receiver sales, 236 vehicles, 91 from 2021+. No appraiser estimates in the API; openings effectively free-bid. Notable: fa-firm Sun 25.10 morning * (2024 BMW 318i יד2 34,929km — Yad2 price-list ₪186,500; 2025 Aygo X יד2 33,850km — asks 85k–108.9k), hob-cars Sun 25.10 morning * (2026 BMW X1 11,952km — carwiz ₪259,000; 2022 GLE400D יד3 98,253km — ₪329,750), federlaw Mon 26.10 morning * (2022 X6 יד1 140,512km — Yad2 list ₪379,800), cflaw Mon 26.10 morning * (59 cars). All anchors are asking prices.

## kones Sentra tender (verified on the tender page 24.10)

https://www.kones.co.il/cars/carinsidepageauction/6291 — Sentra SV 2023, on-road 05/2023, 2.0L auto, test valid to 05/2027. Current bid ₪25,000 vs Yad2 asking ~₪68,000. **Tender ends 28.10 12:00.** It is a PRELIMINARY tender: the sale requires seller approval even if won. Km not published, ownership count unknown, dealer-owned, carries a disabled badge that requires a licensing-office visit to cancel before ownership transfer.

## Channel status

- govil (מיטלטלין): no active tender; last ended 15.6.2025. Wakes when one appears.
- Galeria: no current verified sale — site unreachable from our channels, Bidspirit house dormant since Feb 2025. Not declared lapsed.

## User deliverable

Private Hebrew shortlist File (break-even framing, photos, verified links): https://files.instinct.com/3gqbvms8migm

## Standing watch

12h cadence (wake schedule active). Reports only on material findings: a watch-lot lead moving materially, a new catalog in Roy's categories with a verifiable gap, or channel reactivation. Roy bids himself; this work is research/ranking only — no bids, registrations, deposits, or seller contact.
