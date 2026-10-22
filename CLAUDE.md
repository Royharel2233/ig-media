# ig-media: automated Instagram pipeline

This repo is public. It holds the input texts, the jobs Claude writes, the rendered media
(Instagram fetches media from raw.githubusercontent.com) and the GitHub Actions that publish.

## Who does what
| Step | Who | Where |
|---|---|---|
| Put the digest text | Roy | `inbox/<page>/<YYYY-MM-DD_HHMM>/news.txt` |
| Verify, choose stories, write slides and captions | Claude (scheduled run) | `jobs/<page>/<slot>/queries.json`, then `job.json` |
| Contact sheets of the candidate photos | Action `photos` | `jobs/<page>/<slot>/candidates/` |
| Download photos, render, publish posts and stories | Action `publish` | `media/<page>/<slot>/`, `jobs/<page>/<slot>/result.json` |

Pages are defined in `pages.json`. Only pages with `"enabled": true` are processed. Each page has a `mode`:
| mode | Page | Who makes the content | When |
|---|---|---|---|
| `news_carousels` | globalnews | Claude, from the digest in the inbox (this file) | scheduled Claude runs |
| `paper_carousels` | 1paper | Claude, with the `one-paper-carousel` skill (see below) | scheduled Claude runs, only if its inbox slot has input |
| `reels_daily` | howitworks | Roy, ready-made video + caption | Action `reels-daily`, 18:00 Israel. Claude does nothing for this page. |

## Scheduled run (08:00, 13:00, 19:00 Asia/Jerusalem)
The slot is the run time rounded to the hour: `YYYY-MM-DD_0800`, `_1300`, `_1900` (Israel date).

For each enabled page:
1. `git pull`. Read every `.txt` in `inbox/<page>/<slot>/`. If the folder or text is missing, skip that page and say so in the report. Never invent content.
2. Read `history/<page>.md` (stories already published). Skip anything already covered.
3. Follow the `hebrew-news-carousel` skill for globalnews: verify every story with web search, drop what is unverified or old news presented as new, pick 2-3 singles (tech, AI, economy; no sports or tragedies as singles) and one summary carousel of the remaining verified stories (skip the summary if too few). Covers: hook of at most 8 words, a number or a question. Last slide: CTA + source line. No em dashes. Write "דולר", not $.
4. Write `jobs/<page>/<slot>/queries.json` (schema below), commit, push. Wait for `candidates.json` (poll `git pull` every 30 s, up to 10 min; if it never arrives, check the `photos` Action run and report).
5. Open every `candidates/sheet_<post>.jpg` and choose photos by the skill's photo rules (no wrong brands, no identifiable random faces, no wrong country, no dark covers, no photo reused in the same slot). The id is printed under each thumbnail.
6. Write `jobs/<page>/<slot>/job.json`, append the published headlines to `history/<page>.md`, commit, push.
7. Wait for `result.json` with `"complete": true` (poll every 60 s, up to 30 min). Report to Roy: what was published (permalinks), what was dropped and why, sources, and any errors.

Roy authorized automatic publishing without per-post approval for these scheduled runs (2026-10-22). Publishing rules from the skill still apply: only verified stories.

## 1paper (mode paper_carousels)
Input: `inbox/1paper/<slot>/` with a text file listing one or more paper links or notes.
For each paper follow the `one-paper-carousel` skill exactly (fact list, check.py must pass, render.py with `Overflow: none`, look at the contact sheet).
Then convert the Instagram PNGs to JPEG (quality 92; Instagram rejects PNG) and commit them to
`media/1paper/<slot>/<post-id>/01.jpg ... 08.jpg`. Write `jobs/1paper/<slot>/job.json` with pre-rendered images (no queries.json, no Pexels):
```json
{"page": "1paper", "slot": "2026-10-23_0800", "stories": false,
 "posts": [{"name": "18-ai-example", "type": "single", "caption": "...",
            "images": ["media/1paper/2026-10-23_0800/18-ai-example/01.jpg", "..."]}]}
```
Commit the media and job.json in the same push. Append the paper title to `history/1paper.md`.

## queries.json (candidate photos)
Pexels no longer issues API keys, so Claude finds candidates itself: run WebSearch with
`allowed_domains: ["pexels.com"]` and a concrete English query (e.g. "courtroom gavel photo").
Photo pages look like `https://www.pexels.com/photo/black-wooden-gavel-5668484/`; the number at the end is the id.
Search pages returned in those results (`https://www.pexels.com/search/gavel/`) may then be read with WebFetch for more ids.
Collect 8-15 ids per post (2-4 queries), then write:
```json
{"posts": {"single1_meta": [5668484, 34817075, 37732186], "summary": [10628030, 7567223]}}
```
Post names: `single1_<slug>`, `single2_<slug>`, `single3_<slug>`, `summary`.

## job.json
```json
{
  "page": "globalnews",
  "slot": "2026-10-23_0800",
  "stories": true,
  "posts": [
    {"name": "single1_meta", "type": "single", "caption": "...",
     "slides": [
       {"kind": "cover", "photo": 5668882, "kicker": "Meta · בית משפט", "head": "...", "sub": ["..."]},
       {"photo": 5668484, "head": "...", "sub": ["...", "..."]},
       {"kind": "cta", "photo": 5668882, "blur": 14, "head": "...", "sub": ["כתבו בתגובות."], "source": "מקורות: ..."}
     ]}
  ]
}
```
- `photo` is a Pexels id that appears in `candidates.json` (its thumbnail was on a contact sheet). The CTA slide reuses the cover photo with `blur: 14`.
- 2-10 slides per post. Caption under 2,200 characters, at most 5 hashtags.
- Stories (automatic): first slide of every single, and every summary slide except the last (CTA).
- Feed posts are published in the order of `posts`, then the stories.

## Secrets (repo Settings > Secrets and variables > Actions)
`IG_TOKEN_GLOBALNEWS`, `IG_TOKEN_1PAPER`, `IG_TOKEN_HOWITWORKS`, and optionally `GH_SECRETS_PAT` (fine-grained, Secrets read/write on this repo only) for the bi-weekly token refresh.
