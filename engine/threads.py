"""Threads publishing (cross-post of Instagram feed posts).

Enabled per page in pages.json:
  "threads": {"token_secret": "THREADS_TOKEN_GLOBALNEWS", "since": "2026-10-25_1300",
              "format": "carousel", "topic_tag": "חדשות"}
- format "carousel": the same rendered slides + a short text (Threads limit 500).
- format "text": text only.
- since: jobs with an older slot are never cross-posted (keeps old unfinished jobs from posting late).
The post text is the post's optional "threads_text" in job.json, otherwise the Instagram caption
without hashtags, trimmed at line boundaries."""
import datetime, os, re, time, unicodedata, urllib.parse
from common import PAGES, http, raw_url, wait_public, log

TH = "https://graph.threads.com/v1.0"
LIMIT = 500


def config(page):
    return PAGES.get(page, {}).get("threads")


def token(page):
    return os.environ.get(config(page)["token_secret"], "")


def enabled_for(page, slot):
    """Cross-post this job? Needs config, a token, and a slot not older than 'since'."""
    c = config(page)
    if not c:
        return False
    if not token(page):
        log(f"threads: secret {c['token_secret']} not set, skipping Threads for {page}")
        return False
    return slot >= c.get("since", "")


def call(page, method, path, **params):
    params["access_token"] = token(page)
    if method == "GET":
        return http(f"{TH}/{path}?{urllib.parse.urlencode(params)}")
    return http(f"{TH}/{path}", method="POST", data=params)


def weight(s):
    """Threads counts emojis by their UTF-8 bytes; letters (Hebrew too) count as one."""
    return sum(len(ch.encode("utf-8")) if ord(ch) > 0xFFFF or unicodedata.category(ch) == "So" or ch == "\ufe0f"
               else 1 for ch in s)


def make_text(post, limit=LIMIT):
    """threads_text if given, else the caption without hashtag lines, trimmed by whole lines.
    The last 'מקור' line is kept when possible."""
    src = post.get("threads_text") or post.get("caption", "")
    lines = [l.rstrip() for l in src.split("\n")]
    lines = [re.sub(r"(^|\s)#\S+", "", l).rstrip() if "#" in l else l for l in lines]
    while lines and not lines[-1].strip():
        lines.pop()
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    if weight(text) <= limit:
        return text
    src_line = next((l for l in reversed(lines) if l.startswith("מקור")), "")
    more = "(ההמשך בתמונות)"   # lines were dropped; the slides still carry every story
    budget = limit - (weight(src_line) + 2 if src_line else 0) - weight(more) - 1
    out = []
    for l in lines:
        if l == src_line:
            continue
        cand = "\n".join(out + [l]).strip()
        if weight(cand) > budget:
            break
        out.append(l)
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    if body:
        body += "\n" + more
    else:   # a single very long line: hard cut
        body = text[: max(0, budget - 1)].rstrip() + "…"
    return (body + "\n\n" + src_line).strip() if src_line else body


def wait(page, cid, max_s=300):
    t = time.time()
    while True:
        st = call(page, "GET", cid, fields="status,error_message")
        s = st.get("status")
        if s in ("FINISHED", "PUBLISHED"):
            return
        if s in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"threads container {cid} {s}: {st.get('error_message')}")
        if time.time() - t > max_s:
            raise RuntimeError(f"threads container {cid} still {s} after {max_s}s")
        time.sleep(5)


def already_on_threads(page, text, hours=36):
    """Same idea as the Instagram check: skip if a post with this exact text is already live."""
    try:
        items = call(page, "GET", "me/threads", fields="text,timestamp,permalink", limit=15).get("data", [])
    except Exception as e:
        log("threads duplicate check failed (continuing)", e); return None
    now = datetime.datetime.now(datetime.timezone.utc)
    for m in items:
        ts = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if (m.get("text") or "").strip() == text.strip() and (now - ts).total_seconds() < hours * 3600:
            return {"media_id": m["id"], "permalink": m.get("permalink"), "note": "already live, not re-posted"}
    return None


def publish(page, post, image_paths):
    c = config(page)
    text = make_text(post)
    dup = already_on_threads(page, text)
    if dup:
        log("threads: skip, already live:", dup); return dup
    fmt = c.get("format", "carousel")
    imgs = image_paths[:20] if fmt == "carousel" else []

    def container(text, tag):
        extra = {"topic_tag": tag} if tag else {}
        if len(imgs) >= 2:
            kids = []
            for path in imgs:
                url = raw_url(path); wait_public(url)
                kids.append(call(page, "POST", "me/threads", media_type="IMAGE", image_url=url, is_carousel_item="true")["id"])
            for k in kids:
                wait(page, k)
            return call(page, "POST", "me/threads", media_type="CAROUSEL", children=",".join(kids), text=text, **extra)["id"]
        return call(page, "POST", "me/threads", media_type="TEXT", text=text, **extra)["id"]

    try:
        cid = container(text, c.get("topic_tag"))
    except RuntimeError as e:
        # Unknown length counting or a rejected topic tag: retry once, stricter (UTF-8 bytes) and without the tag.
        log("threads: container failed, retrying stricter:", e)
        lim, strict = LIMIT, make_text(post)
        while len(strict.encode("utf-8")) > LIMIT and lim > 50:
            lim = int(lim * LIMIT / len(strict.encode("utf-8"))) - 5
            strict = make_text(post, limit=lim)
        cid = container(strict, None)
    wait(page, cid)
    mid = call(page, "POST", "me/threads_publish", creation_id=cid)["id"]
    try:
        link = call(page, "GET", mid, fields="permalink").get("permalink")
    except Exception:
        link = None
    return {"media_id": mid, "permalink": link}
