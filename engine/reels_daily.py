"""Daily reels for pages with "mode": "reels_daily" (e.g. how.it.works.il).
Roy drops inbox/<page>/<YYYY-MM-DD>/ with a video (.mp4/.mov) and caption.txt (or <video-name>.txt).
At the page's publish hour (Israel time) every video in today's folder is published as a reel.
Safe to re-run: published videos are recorded in jobs/<page>/<date>/result.json and skipped."""
import datetime, glob, json, os, subprocess, sys, zoneinfo
from common import ROOT, PAGES, ig, wait_container, raw_url, wait_public, log
import tiktok

TZ = zoneinfo.ZoneInfo("Asia/Jerusalem")


def git_push(msg):
    subprocess.run(["git", "add", "-A", "jobs"], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT, check=True)
    for _ in range(4):
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            return
        subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT, check=True)


def caption_for(video):
    own = os.path.splitext(video)[0] + ".txt"
    shared = os.path.join(os.path.dirname(video), "caption.txt")
    for c in (own, shared):
        if os.path.exists(c):
            return open(c, encoding="utf-8").read().strip()
    raise RuntimeError(f"no caption .txt next to {os.path.basename(video)}")


def main():
    now = datetime.datetime.now(TZ)
    force = os.environ.get("FORCE") == "1"
    failed = False
    for page, cfg in PAGES.items():
        if not cfg.get("enabled") or cfg.get("mode") != "reels_daily":
            continue
        if not force and now.hour != cfg.get("publish_hour", 18):
            log(f"{page}: not {cfg.get('publish_hour', 18)}:00 in Israel (now {now:%H:%M}), skipping")
            continue
        day = now.strftime("%Y-%m-%d")
        src = os.path.join(ROOT, "inbox", page, day)
        videos = sorted(glob.glob(os.path.join(src, "*.mp4")) + glob.glob(os.path.join(src, "*.mov")))
        if not videos:
            log(f"{page}: no video in inbox/{page}/{day}"); continue
        resdir = os.path.join(ROOT, "jobs", page, day); os.makedirs(resdir, exist_ok=True)
        resfile = os.path.join(resdir, "result.json")
        res = json.load(open(resfile)) if os.path.exists(resfile) else {"done": {}, "errors": []}
        for v in videos:
            key = os.path.basename(v)
            if key in res["done"]:
                continue
            try:
                cap = caption_for(v)
                if len(cap) > 2200 or cap.count("#") > 30:
                    raise RuntimeError("caption over Instagram limits")
                url = raw_url(os.path.relpath(v, ROOT)); wait_public(url)
                cid = ig(page, "POST", "me/media", media_type="REELS", video_url=url, caption=cap, share_to_feed="true")["id"]
                wait_container(page, cid, max_s=900)
                mid = ig(page, "POST", "me/media_publish", creation_id=cid)["id"]
                res["done"][key] = {"media_id": mid, "permalink": ig(page, "GET", mid, fields="permalink").get("permalink")}
                log("published", page, key, res["done"][key])
            except Exception as e:
                failed = True; res["errors"].append(f"{key}: {e}"); log("FAILED", page, key, e)
            json.dump(res, open(resfile, "w"), indent=1)
        # TikTok: same videos as drafts in the TikTok app (Roy publishes them by hand).
        if cfg.get("tiktok_drafts"):
            for v in videos:
                key = "tiktok:" + os.path.basename(v)
                if key in res["done"]:
                    continue
                try:
                    res["done"][key] = tiktok.upload_draft(v, cfg["tiktok_secret"]); log("tiktok draft", page, key, res["done"][key])
                except Exception as e:
                    failed = True; res["errors"].append(f"{key}: {e}"); log("FAILED", page, key, e)
                json.dump(res, open(resfile, "w"), indent=1)
        git_push(f"reels {page} {day}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
