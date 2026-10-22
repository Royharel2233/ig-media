"""YouTube Shorts: upload a vertical video (up to 3 minutes counts as a Short) as PRIVATE.
Roy reviews it in YouTube Studio and makes it public. Unaudited API projects can only upload private videos anyway.
Secrets: YT_CLIENT_ID, YT_CLIENT_SECRET (Google OAuth "Desktop app" client) and YT_REFRESH_TOKEN_<PAGE>."""
import json, os, re, urllib.parse, urllib.request, urllib.error

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"


def _call(req, timeout=600):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r, r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"YouTube {req.full_url.split('?')[0]} -> HTTP {e.code}: {e.read()[:400]!r}")


def access_token(secret_name):
    rt = os.environ.get(secret_name, "")
    cid, sec = os.environ.get("YT_CLIENT_ID", ""), os.environ.get("YT_CLIENT_SECRET", "")
    if not (rt and cid and sec):
        raise RuntimeError(f"YouTube not configured: need YT_CLIENT_ID, YT_CLIENT_SECRET and {secret_name}")
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": sec, "refresh_token": rt, "grant_type": "refresh_token"}).encode()
    _, raw = _call(urllib.request.Request(TOKEN_URL, data=body), 60)
    r = json.loads(raw)
    if "access_token" not in r:
        raise RuntimeError(f"YouTube token refresh failed: {r}. If the Google app is still in Testing mode, sign-ins expire after 7 days: switch it to In production and reconnect.")
    return r["access_token"]


def _clean(text, limit):
    text = text.replace("<", "").replace(">", "")       # YouTube rejects angle brackets in title and description
    return text[:limit]


def upload_private(video_path, caption, secret_name):
    tok = access_token(secret_name)
    first = next((l for l in caption.splitlines() if l.strip()), "how.it.works")
    title = _clean(re.sub(r"\s*#\S+", "", first).strip() or "how.it.works", 100)
    meta = {"snippet": {"title": title, "description": _clean(caption, 5000), "categoryId": "28"},
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}}
    size = os.path.getsize(video_path)
    init = urllib.request.Request(UPLOAD_URL, data=json.dumps(meta).encode(), method="POST", headers={
        "Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/*", "X-Upload-Content-Length": str(size)})
    resp, _ = _call(init, 60)
    location = resp.headers["Location"]
    with open(video_path, "rb") as f:
        data = f.read()
    put = urllib.request.Request(location, data=data, method="PUT", headers={
        "Authorization": f"Bearer {tok}", "Content-Type": "video/*", "Content-Length": str(size)})
    _, raw = _call(put, 900)
    vid = json.loads(raw)["id"]
    return {"video_id": vid, "privacy": "private", "studio": f"https://studio.youtube.com/video/{vid}/edit"}
