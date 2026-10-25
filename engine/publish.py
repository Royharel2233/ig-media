"""Stage B: for every jobs/<page>/<slot>/job.json whose result.json is not complete:
download the chosen Pexels photos, render, push the media to this public repo,
then publish carousels and stories to Instagram. Safe to re-run: finished items are skipped."""
import datetime, glob, json, os, subprocess, sys, time, traceback
from common import ROOT, PAGES, pexels_image, ig, wait_container, raw_url, wait_public, log
import render
import threads

MAX_SLIDES = 10


def git_pull():
    """Rebase local commits onto the latest remote. On a conflict our version of the file wins
    (in a rebase, -X theirs means the commit being replayed, i.e. this run's result.json)."""
    if subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "rebase", "--abort"], cwd=ROOT)
    subprocess.run(["git", "pull", "-q", "--rebase", "-X", "theirs"], cwd=ROOT, check=True)


def git_push(msg):
    subprocess.run(["git", "add", "-A", "media", "jobs"], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT, check=True)
    for _ in range(4):
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            return
        git_pull()
    raise RuntimeError("git push failed 4 times")


def load_result(resfile):
    try:
        return json.load(open(resfile))
    except (FileNotFoundError, ValueError):
        return {"done": {}, "errors": []}


def already_on_instagram(page, caption, hours=36):
    """Last line of defence against double posts: is a post with this exact caption already live?"""
    try:
        items = ig(page, "GET", "me/media", fields="caption,timestamp,permalink", limit=15).get("data", [])
    except Exception as e:
        log("duplicate check failed (continuing)", e); return None
    now = datetime.datetime.now(datetime.timezone.utc)
    for m in items:
        ts = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if (m.get("caption") or "").strip() == caption.strip() and (now - ts).total_seconds() < hours * 3600:
            return {"media_id": m["id"], "permalink": m.get("permalink"), "note": "already live, not re-posted"}
    return None


def validate(job):
    errs = []
    if job["page"] not in PAGES:
        errs.append(f"unknown page {job['page']}")
    elif not PAGES[job["page"]].get("enabled"):
        errs.append(f"page {job['page']} is not enabled in pages.json")
    for p in job["posts"]:
        cap = p.get("caption", "")
        if len(cap) > 2200: errs.append(f"{p['name']}: caption {len(cap)} chars")
        if cap.count("#") > 5: errs.append(f"{p['name']}: more than 5 hashtags")
        n = len(p["images"]) if "images" in p else len(p.get("slides", []))
        if not 2 <= n <= MAX_SLIDES: errs.append(f"{p['name']}: {n} slides")
        if p.get("type") not in ("single", "summary"): errs.append(f"{p['name']}: type must be single or summary")
        if threads.weight(p.get("threads_text", "")) > threads.LIMIT: errs.append(f"{p['name']}: threads_text over {threads.LIMIT}")
        for img in p.get("images", []) + p.get("story_images", []):
            if not img.lower().endswith((".jpg", ".jpeg")): errs.append(f"{p['name']}: {img} must be JPEG (Instagram rejects PNG)")
            elif not os.path.exists(os.path.join(ROOT, img)): errs.append(f"{p['name']}: missing {img}")
    if errs:
        raise RuntimeError("job.json invalid: " + "; ".join(errs))


def build(job, media_rel):
    """Download photos and render every post. Returns {post: {feed: [...], story: [...]}} (repo-relative paths)."""
    media = os.path.join(ROOT, media_rel)
    ids = {s["photo"] for p in job["posts"] if "images" not in p for s in p["slides"]}
    for pid in ids:
        dest = os.path.join(media, "photos", f"{pid}.jpg")
        if not os.path.exists(dest):
            pexels_image(pid, dest)
    brand = PAGES[job["page"]]["brand"]
    out = {}
    for p in job["posts"]:
        if "images" in p:   # pre-rendered by Claude (e.g. 1paper): publish the given JPEGs as they are
            out[p["name"]] = {"feed": p["images"], "story": p.get("story_images", [])}
            continue
        slides = [dict(s, photo=os.path.join(media, "photos", f"{s['photo']}.jpg")) for s in p["slides"]]
        pdir = os.path.join(media, p["name"])
        render.run(slides, pdir, brand)
        n = len(slides)
        out[p["name"]] = {
            "feed": [f"{media_rel}/{p['name']}/feed_4x5/{i:02d}.jpg" for i in range(1, n + 1)],
            "story": [f"{media_rel}/{p['name']}/story_9x16/{i:02d}.jpg" for i in range(1, n + 1)],
        }
    return out


def with_retry(fn, tries=4, wait=20):
    """Instagram sometimes fails to fetch a raw.githubusercontent URL (error 2207052). Retry those."""
    for i in range(tries):
        try:
            return fn()
        except RuntimeError as e:
            if "2207052" not in str(e) or i == tries - 1:
                raise
            log(f"media fetch failed, retry {i + 1} in {wait}s"); time.sleep(wait)


def publish_carousel(page, paths, caption):
    kids = []
    for path in paths:
        url = raw_url(path); wait_public(url)
        kids.append(with_retry(lambda: ig(page, "POST", "me/media", image_url=url, is_carousel_item="true"))["id"])
    for k in kids:
        wait_container(page, k)
    cid = ig(page, "POST", "me/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"]
    wait_container(page, cid)
    mid = ig(page, "POST", "me/media_publish", creation_id=cid)["id"]
    link = ig(page, "GET", mid, fields="permalink").get("permalink")
    return {"media_id": mid, "permalink": link}


def publish_story(page, path):
    url = raw_url(path); wait_public(url)
    cid = with_retry(lambda: ig(page, "POST", "me/media", media_type="STORIES", image_url=url))["id"]
    wait_container(page, cid)
    return {"media_id": ig(page, "POST", "me/media_publish", creation_id=cid)["id"]}


def run_job(jobfile):
    jobdir = os.path.dirname(jobfile)
    rel = os.path.relpath(jobdir, ROOT)                      # jobs/<page>/<slot>
    resfile = os.path.join(jobdir, "result.json")
    res = load_result(resfile)
    if res.get("complete"):
        return
    job = json.load(open(jobfile, encoding="utf-8"))
    validate(job)
    page = job["page"]
    media_rel = "media/" + rel.split("/", 1)[1]               # media/<page>/<slot>
    files = build(job, media_rel)
    git_push(f"render {rel}")

    # Optional scheduled publish time, e.g. "2026-10-23T08:00:00+03:00" (prepared early, posted on time).
    if job.get("publish_after"):
        wait = (datetime.datetime.fromisoformat(job["publish_after"]) - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
        if wait > 0:
            if wait > 100 * 60:
                raise RuntimeError(f"publish_after is {wait/60:.0f} min away; jobs may be pushed at most 100 min early")
            log(f"waiting {wait/60:.1f} min until {job['publish_after']}"); time.sleep(wait)

    # Re-read the latest result.json right before publishing: another run may have finished this job meanwhile.
    git_pull()
    res = load_result(resfile)
    if res.get("complete"):
        log(f"{rel} already complete, nothing to publish"); return

    def post(p):
        dup = already_on_instagram(page, p["caption"])
        if dup:
            log("skip, already live:", dup); return dup
        return publish_carousel(page, files[p["name"]]["feed"], p["caption"])

    plan = []
    for p in job["posts"]:
        plan.append(("post:" + p["name"], lambda p=p: post(p)))
    if threads.enabled_for(page, job.get("slot", "")):   # cross-post to Threads after the Instagram feed posts
        for p in job["posts"]:
            plan.append(("threads:" + p["name"], lambda p=p: threads.publish(page, p, files[p["name"]]["feed"])))
    if job.get("stories", True):
        for p in job["posts"]:
            st = files[p["name"]]["story"]
            frames = st[:1] if p["type"] == "single" else st[:-1]   # summary: every slide except the CTA
            for i, path in enumerate(frames, 1):
                plan.append((f"story:{p['name']}:{i}", lambda path=path: publish_story(page, path)))

    q = ig(page, "GET", "me/content_publishing_limit", fields="quota_usage,config").get("data", [{}])[0]
    left = q.get("config", {}).get("quota_total", 100) - q.get("quota_usage", 0)
    log(f"quota left {left}, planned {len(plan)}")

    for key, fn in plan:
        if key in res["done"]:
            continue
        try:
            res["done"][key] = fn(); log("published", key, res["done"][key])
        except Exception as e:
            res["errors"].append(f"{key}: {e}"); log("FAILED", key, e)
        json.dump(res, open(resfile, "w"), indent=1)
    res["complete"] = all(k in res["done"] for k, _ in plan)
    json.dump(res, open(resfile, "w"), indent=1)
    git_push(f"result {rel}")


def main():
    failed = False
    for jf in sorted(glob.glob(os.path.join(ROOT, "jobs", "*", "*", "job.json"))):
        try:
            run_job(jf)
        except Exception:
            failed = True
            err = traceback.format_exc(); log(err)
            rf = os.path.join(os.path.dirname(jf), "result.json")
            subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)
            r = load_result(rf)
            r["errors"].append(err.strip().splitlines()[-1]); json.dump(r, open(rf, "w"), indent=1)
            git_push(f"error {os.path.relpath(os.path.dirname(jf), ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
