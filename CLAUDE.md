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
| `paper_daily` | 1paper | Claude picks the paper and writes it with the `one-paper-carousel` skill (see below) | separate scheduled Claude run at 07:15, posted at 08:00 Israel |
| `reels_daily` | howitworks | Roy, ready-made video + caption | Action `reels-daily`, 18:00 Israel. Claude does nothing for this page. |

## News run (08:00, 13:00, 19:00 Asia/Jerusalem): pages with mode `news_carousels` only
The slot is the run time rounded to the hour: `YYYY-MM-DD_0800`, `_1300`, `_1900` (Israel date).

For each enabled page with mode `news_carousels`:
1. `git pull`. Read every `.txt` in `inbox/<page>/<slot>/`. If the folder or text is missing, skip that page and say so in the report. Never invent content.
2. Read `history/<page>.md` (stories already published). Skip anything already covered.
3. Follow the `hebrew-news-carousel` skill for globalnews: verify every story with web search, drop what is unverified or old news presented as new, pick 2-3 singles (tech, AI, economy; no sports or tragedies as singles) and one summary carousel of the remaining verified stories (skip the summary if too few). Covers: hook of at most 8 words, a number or a question. Last slide: CTA + source line. No em dashes. Write "דולר", not $. Every caption (singles and summary) ends with the follow line "עקבו אחרי @globalnews.il לחדשות מהעולם כל יום", placed after the source line and before the hashtags.
4. Write `jobs/<page>/<slot>/queries.json` (schema below), commit, push. Wait for `candidates.json` (poll `git pull` every 30 s, up to 10 min; if it never arrives, check the `photos` Action run and report).
5. Open every `candidates/sheet_<post>.jpg` and choose photos by the skill's photo rules (no wrong brands, no identifiable random faces, no wrong country, no dark covers, no photo reused in the same slot). The id is printed under each thumbnail. The renderer darkens the lower ~60% of each slide under the text, so the subject of a cover photo must sit in the upper half of the frame (a car at the bottom of a street photo disappears).
6. Write `jobs/<page>/<slot>/job.json`, append the published headlines to `history/<page>.md`, commit, push.
7. Wait for `result.json` with `"complete": true` (poll every 60 s, up to 30 min). Report to Roy: what was published (permalinks), what was dropped and why, sources, and any errors.

Roy authorized automatic publishing without per-post approval for these scheduled runs (2026-10-22). Publishing rules from the skill still apply: only verified stories.

## 1paper daily run (07:15 Asia/Jerusalem, posted at 08:00): mode `paper_daily`
No inbox: Claude chooses the paper.
1. `git pull`. Read `history/1paper.md` and never repeat a paper.
2. Choose the paper with step 0 of the `one-paper-carousel` skill ("Choose the paper"): candidates from the last 7 days that people are already sharing (Reddit, Hacker News, Hugging Face trending, big general outlets), virality scorecard with a 12/18 gate, and a pillar balance. Never pick a paper by Anthropic or OpenAI without stating the conflict of interest in the report.
3. Follow the `one-paper-carousel` skill exactly (read the primary source, fact list, true hook, `check.py` must print ALL CHECKS PASSED, `render.py` must report `Overflow: none`, look at the contact sheet). Its rule about asking before publishing is replaced here: Roy authorized automatic daily publishing (2026-10-22).
4. Convert the Instagram PNGs (`out/en/ig/<id>/`) to JPEG quality 92 and commit them to `media/1paper/<YYYY-MM-DD>/<id>/01.jpg ... 08.jpg`.
5. Write `jobs/1paper/<YYYY-MM-DD>/job.json` and push it together with the media and the new line in `history/1paper.md`:
```json
{"page": "1paper", "slot": "2026-10-23", "stories": false, "publish_after": "2026-10-23T08:00:00+03:00",
 "posts": [{"name": "18-ai-example", "type": "single", "caption": "...",
            "images": ["media/1paper/2026-10-23/18-ai-example/01.jpg", "..."]}]}
```
`publish_after` is 08:00 Israel time today with the correct UTC offset (+03:00 in summer time, +02:00 in winter). The `publish` Action renders nothing for pre-rendered posts and waits until that time. If preparation runs past 08:00, set `publish_after` to now.
6. Wait for `result.json` `"complete": true` (poll every 60 s, up to 90 min), then report: the paper, why it was picked, the hook, the permalink, and sources.

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
- Threads (globalnews only, `pages.json` > `threads`): every feed post is cross-posted to Threads as the same slides plus a text of at most 500 characters (emojis count as several). Write `"threads_text"` for each post: the hook, the 1-3 key facts and the source line, no hashtags, same verification rules as the caption. For the summary, list only as many stories as fit and end with "(ההמשך בתמונות)". Without `threads_text` the caption is trimmed automatically by whole lines. Result keys: `threads:<post>`.

## Secrets (repo Settings > Secrets and variables > Actions)
`IG_TOKEN_GLOBALNEWS`, `IG_TOKEN_1PAPER`, `IG_TOKEN_HOWITWORKS`, `THREADS_TOKEN_GLOBALNEWS` (created by the `threads-connect` Action; refreshed with the Instagram tokens), and optionally `GH_SECRETS_PAT` (fine-grained, Secrets read/write on this repo only) for the bi-weekly token refresh.
