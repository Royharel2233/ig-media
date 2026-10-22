"""Stage B: for every jobs/<page>/<slot>/job.json whose result.json is not complete:
download the chosen Pexels photos, render, push the media to this public repo,
then publish carousels and stories to Instagram. Safe to re-run: finished items are skipped."""
import glob, json, os, subprocess, sys, traceback
from common import ROOT, PAGES, pexels, download, ig, wait_container, raw_url, wait_public, log
import render

MAX_SLIDES = 10


def git_push(msg):
    subprocess.run(["git", "add", "-A", "media", "jobs"], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT, check=True)
    for _ in range(4):
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            return
        subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT, check=True)
    raise RuntimeError("git push failed 4 times")


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
        if not 2 <= len(p["slides"]) <= MAX_SLIDES: errs.append(f"{p['name']}: {len(p['slides'])} slides")
        if p.get("type") not in ("single", "summary"): errs.append(f"{p['name']}: type must be single or summary")
    if errs:
        raise RuntimeError("job.json invalid: " + "; ".join(errs))


def build(job, media_rel):
    """Download photos and render every post. Returns {post: {feed: [...], story: [...]}} (repo-relative paths)."""
    media = os.path.join(ROOT, media_rel)
    ids = {s["photo"] for p in job["posts"] for s in p["slides"]}
    for pid in ids:
        dest = os.path.join(media, "photos", f"{pid}.jpg")
        if not os.path.exists(dest):
            info = pexels(f"photos/{pid}")
            download(info["src"]["large2x"], dest)
    brand = PAGES[job["page"]]["brand"]
    out = {}
    for p in job["posts"]:
        slides = [dict(s, photo=os.path.join(media, "photos", f"{s['photo']}.jpg")) for s in p["slides"]]
        pdir = os.path.join(media, p["name"])
        render.run(slides, pdir, brand)
        n = len(slides)
        out[p["name"]] = {
            "feed": [f"{media_rel}/{p['name']}/feed_4x5/{i:02d}.jpg" for i in range(1, n + 1)],
            "story": [f"{media_rel}/{p['name']}/story_9x16/{i:02d}.jpg" for i in range(1, n + 1)],
        }
    return out


def publish_carousel(page, paths, caption):
    kids = []
    for path in paths:
        url = raw_url(path); wait_public(url)
        kids.append(ig(page, "POST", "me/media", image_url=url, is_carousel_item="true")["id"])
    for k in kids:
        wait_container(page, k)
    cid = ig(page, "POST", "me/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"]
    wait_container(page, cid)
    mid = ig(page, "POST", "me/media_publish", creation_id=cid)["id"]
    link = ig(page, "GET", mid, fields="permalink").get("permalink")
    return {"media_id": mid, "permalink": link}


def publish_story(page, path):
    url = raw_url(path); wait_public(url)
    cid = ig(page, "POST", "me/media", media_type="STORIES", image_url=url)["id"]
    wait_container(page, cid)
    return {"media_id": ig(page, "POST", "me/media_publish", creation_id=cid)["id"]}


def run_job(jobfile):
    jobdir = os.path.dirname(jobfile)
    rel = os.path.relpath(jobdir, ROOT)                      # jobs/<page>/<slot>
    resfile = os.path.join(jobdir, "result.json")
    res = json.load(open(resfile)) if os.path.exists(resfile) else {"done": {}, "errors": []}
    if res.get("complete"):
        return
    job = json.load(open(jobfile, encoding="utf-8"))
    validate(job)
    page = job["page"]
    media_rel = "media/" + rel.split("/", 1)[1]               # media/<page>/<slot>
    files = build(job, media_rel)
    git_push(f"render {rel}")

    plan = []
    for p in job["posts"]:
        plan.append(("post:" + p["name"], lambda p=p: publish_carousel(page, files[p["name"]]["feed"], p["caption"])))
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
            r = json.load(open(rf)) if os.path.exists(rf) else {"done": {}, "errors": []}
            r["errors"].append(err.strip().splitlines()[-1]); json.dump(r, open(rf, "w"), indent=1)
            git_push(f"error {os.path.relpath(os.path.dirname(jf), ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
