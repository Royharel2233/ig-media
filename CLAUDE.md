# ig-media: automated Instagram pipeline

This repo is public. It holds the input texts, the jobs Claude writes, the rendered media
(Instagram fetches media from raw.githubusercontent.com) and the GitHub Actions that publish.

## Who does what
| Step | Who | Where |
|---|---|---|
| Put the digest text | Roy | `inbox/<page>/<YYYY-MM-DD_HHMM>/news.txt` |
| Verify, choose stories, write slides and captions | Claude (scheduled run) | `jobs/<page>/<slot>/queries.json`, then `job.json` |
| Search Pexels, contact sheets | Action `photos` | `jobs/<page>/<slot>/candidates/` |
| Download photos, render, publish posts and stories | Action `publish` | `media/<page>/<slot>/`, `jobs/<page>/<slot>/result.json` |

Pages are defined in `pages.json`. Only pages with `"enabled": true` are processed.

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

## queries.json
```json
{"posts": {"single1_meta": ["courtroom gavel", "smartphone dark"], "summary": ["stock market screen", "laptop coding"]}}
```
Post names: `single1_<slug>`, `single2_<slug>`, `single3_<slug>`, `summary`. 2-4 queries per post, English, concrete objects.

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
- `photo` is a Pexels id from `candidates.json`. The CTA slide reuses the cover photo with `blur: 14`.
- 2-10 slides per post. Caption under 2,200 characters, at most 5 hashtags.
- Stories (automatic): first slide of every single, and every summary slide except the last (CTA).
- Feed posts are published in the order of `posts`, then the stories.

## Secrets (repo Settings > Secrets and variables > Actions)
`PEXELS_API_KEY`, `IG_TOKEN_GLOBALNEWS`, `IG_TOKEN_1PAPER`, `IG_TOKEN_HOWITWORKS`, and optionally `GH_SECRETS_PAT` (fine-grained, Secrets read/write on this repo only) for the bi-weekly token refresh.
