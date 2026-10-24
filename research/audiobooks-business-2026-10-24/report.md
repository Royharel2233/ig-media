# Audiobooks as a business — deep research report
Date: 2026-10-24. Prepared for Roy Harel's side-business evaluation.

## One-paragraph answer

Audiobooks as a standalone, agent-run business under Roy's constraints (max 1,000 ILS loss, <=10 min/day, 90%+ automation, no marketing/outreach) is **not viable as a new business today**. The technical pipeline (AI narration + wide distribution from Israel) exists and is cheap, but the demand side is decisive: AI-narrated titles were 0.03% of US audiobook sales in 2025 (Audio Publishers Association), listener willingness to try AI narration is *falling*, and field evidence shows AI-narrated audiobooks sell near-zero even when the same book's ebook edition is a top-2,000 Kindle title. Audiobooks extend a book that already sells; they do not create demand. Roy has no narrative ebook catalog (puzzle books do not translate to audio), so this "business" is really "become an English-language book publisher first" — a much bigger, marketing-driven venture that conflicts with the constraints. The only scenario where AI audio makes sense for Roy: as a cheap add-on *if* a future book of his already sells in text form.

## Verdict against each constraint

| Constraint | Fit |
|---|---|
| Max loss 1,000 ILS | Fits. One book costs ~$22-99 in ElevenLabs credits (or $0 via KDP Virtual Voice / Google auto-narration where available). |
| <=10 min/day of Roy's time | Fits for production. Does NOT fit for what actually drives sales (ongoing marketing, review building, platform optimization). |
| 90%+ automation | Production: yes. Demand generation: no. |
| No sales/outreach | Fails in practice: discoverability without marketing is near zero (evidence below). |
| Free/local first | Partly: KDP Virtual Voice and Google auto-narration are free but have eligibility barriers (below); quality free local TTS on M3 exists but is weaker and needs production work. |

## What the research established (with sources)

### 1. Market is big and growing — and flooded
- US audiobook sales $2.43B in 2025, +9% YoY; 750,000 active titles, +43% in one year. (Publishers Weekly / APA, 2026-06-08)
- **AI-narrated audiobooks were 0.03% of 2025 sales.** Willingness to try AI-narrated titles fell from 70% (2025) to 61% (2026); only 16% of listeners have tried one. (same source)
- Spotify expanding audiobooks from 22 to 180+ markets by end of 2026, incl. Israel as a *listening* market (Spotify newsroom, 2026-10-07).

### 2. Demand evidence for AI-narrated indie titles is brutal
- Manual sample of 7 bestselling Kindle books with Virtual Voice audio editions: audio editions ranked ~70,000-370,000 in Audiobooks while ebooks ranked top-2,000-50,000; of 6 reviews mentioning the AI narration, 5 were 1-star. (r/selfpublish, 2026-01-10 — informal sample, not official statistics)
- Authors report purchased AI-narrated copies being returned quickly; multiple authors pulled them before review damage. (same thread)
- Counter-evidence exists but is conditional: authors *with existing readership* report audio adding sales (one reports audio = 1/3 of purchases via free KDP Virtual Voice; an established author claims some Virtual Voice titles above his earning $600+/day). Pattern: audio monetizes existing demand, doesn't create it.
- Indie earnings thread: without an existing reader base, "even great audiobooks just sit there"; typical outcomes $0-30/month without marketing; ROI periods of 6-24 months even for a 50+ title backlist. (r/selfpublish, 2025-04-22)

### 3. Platform access from Israel (verified on official pages, 2026-10-24)
- **ACX (Audible direct): closed twice over.** AI narration prohibited on direct submission ("must be narrated by a human... unauthorized use of text-to-speech, AI or automated recordings is prohibited", ACX submission requirements, updated 2026-04-15, via audiopod.ai matrix); and ACX accounts limited to US/UK/Canada/Ireland residents.
- **Audible via distributors: effectively closed to third-party AI narration** (PublishDrive store table: Audible accepts AI only via Audible's own tool).
- **KDP Virtual Voice: free, 40% royalty on a la carte, but** Amazon's own TTS built from your eligible KDP *ebook*; US-marketplace beta (interest list); Amazon owns the audio file; English/Spanish/French/Italian voices; requires an eligible narrative ebook — Roy has paperbacks, not eligible ebooks.
- **Google Play Books: not available to Israeli sellers** — Israel is absent from the official seller sign-up and payments country table. Auto-narration also limited to listed countries. (support.google.com/books/partner/table/6052428)
- **Spotify: accepts digital voice narration** (ElevenLabs, Google Play Books providers), mandatory disclosure label, digital-voice titles not shared to referral partners (Spotify-only). Direct Spotify for Authors country availability for Israel unverified (page section unreadable), but the distributor route below bypasses this.
- **Voices by INaudio (ex-Findaway Voices, Spotify-owned): available to authors in ALL countries** (official support article). Pays monthly in USD; author keeps 80% of royalties received (retailers pay 40-50% of list ALC, 30-40% subscription, 25-45% revenue share → net to author roughly 32-40% of list on a sale). Accepts AI narration only as an unmodified LPF package from Google Play Books, ElevenLabs, or Spoken Press; ElevenLabs Studio has a built-in "Publish to Spotify" LPF export.
- **Kobo Writing Life: accepts AI narration** (list narrator as "Synthesised voice"), open to international authors, pays via EFT in USD (threshold CAD 50, 45 days after month end).
- **Apple Books: digital narration is Apple's own free program** (from your English ebook, via preferred partners Draft2Digital/PublishDrive/Ingram; selective; 1-2 months; English only). Apple also accepts third-party AI-narrated uploads via PublishDrive.
- **Public-domain shortcut is blocked/saturated**: Google Play no longer accepts public-domain content except from select partners; ACX public domain requires human narration via ACX (unavailable); classic titles are saturated everywhere else.

### 4. Unit economics
- Production (ElevenLabs): Creator $22/mo ≈ 121k credits ≈ ~2h audio; Pro $99/mo ≈ 600k ≈ ~10h. An 80k-word novel (~7.5h audio) ≈ one month of Pro (~$99) or ~4 months of Creator. A 2-hour short nonfiction ≈ $22. Failed generations burn credits (10-15% redo rate typical). Commercial license included from Starter ($6/mo). (texttolab.com breakdown, Oct 2026; elevenlabs.io/pricing)
- Spotify streaming payout: ~$0.011-0.019 per completed listening hour (ALLi forum data compiled by BookLaunch News, 2026-06) → a full 10-hour listen ≈ $0.15 gross, ~$0.12 to author. Audiobook sales via INaudio ≈ 32-40% of list price net.
- So: near-zero cost to produce, near-zero revenue without an audience. Break-even per book is trivially low (5-10 sales) but the expected number of sales for an unknown author with no marketing is ~0-10 lifetime.

### 5. Copyright/licensing notes
- AI narration of your own original text is fine; commercial license required on the TTS plan (ElevenLabs Starter+).
- Narrating others' books requires audiobook rights (not available cheaply); public domain mostly blocked or saturated (above).
- All platforms that accept AI narration require disclosure; hiding it risks post-publication removal.

### 6. Hebrew angle
- No meaningful open self-publish audiobook channel in Hebrew; Israeli market is small and served by production houses/publishers (Storytel/iCast, paid production services). Not a shortcut.

## The one scenario where this makes sense for Roy
If a future Clear Mind/Walter Hayes (or any) **ebook already sells** in text, adding an AI-narrated audio edition is nearly free (KDP Virtual Voice $0, or ~$22 ElevenLabs) and low-risk. Order of operations: prove the text first, then add audio. Audio is a multiplier on existing demand, not a business by itself.

## Cheapest possible test (if Roy insists on empirics)
~$22-30 total: one short English nonfiction ebook (must be written first — the real work), KDP ebook + free Virtual Voice for Audible, ElevenLabs Creator one month → LPF → INaudio → Spotify/Kobo. Expected revenue realistically $0-20. This tests the pipeline, not a business.

## Open gaps (unverified)
- Whether Spotify for Authors direct sign-up accepts Israeli accounts (the distributor route via INaudio works regardless).
- Exact INaudio payment-method options for Israeli bank accounts (USD payment; methods/thresholds set in Payment Profile; would need account creation to confirm).
- KDP Virtual Voice beta admission odds/timeline for a non-US author account.

## Bottom line for delivery
Don't start an audiobook business. The pipeline exists and is cheap, but every demand-side signal says AI-narrated titles without an existing readership sell ~nothing, the biggest store (Audible) is closed to outside AI narration, and Google Play seller access doesn't exist from Israel. Revisit only as an add-on to a book that already sells in text.
