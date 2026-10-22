"""TikTok: upload a video to the creator's TikTok inbox as a draft (Content Posting API, video.upload scope).
Roy opens TikTok, adds a sound if he wants, and publishes. Drafts need no app audit and no domain verification.
Secrets per page: TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET (the developer app), TIKTOK_REFRESH_TOKEN_<PAGE>."""
import json, os, subprocess, time, urllib.parse, urllib.request, urllib.error
from common import log

API = "https://open.tiktokapis.com/v2"
MIN_CHUNK, MAX_CHUNK = 5 * 1024 * 1024, 64 * 1024 * 1024


def _req(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TikTok {url.split('?')[0]} -> HTTP {e.code}: {e.read()[:400]!r}")


def access_token(secret_name):
    """Exchanges the stored refresh token for a 24h access token. TikTok may rotate the refresh token;
    when it does and GH_SECRETS_PAT is available, the new one is saved back to the repo secret."""
    rt = os.environ.get(secret_name, "")
    key, sec = os.environ.get("TIKTOK_CLIENT_KEY", ""), os.environ.get("TIKTOK_CLIENT_SECRET", "")
    if not (rt and key and sec):
        raise RuntimeError(f"TikTok not configured: need TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET and {secret_name}")
    body = urllib.parse.urlencode({"client_key": key, "client_secret": sec, "grant_type": "refresh_token", "refresh_token": rt}).encode()
    r = _req(f"{API}/oauth/token/", body, {"Content-Type": "application/x-www-form-urlencoded"})
    if "access_token" not in r:
        raise RuntimeError(f"TikTok token refresh failed: {r.get('error_description') or r}")
    new_rt = r.get("refresh_token")
    if new_rt and new_rt != rt and os.environ.get("GH_TOKEN"):
        subprocess.run(["gh", "secret", "set", secret_name, "--body", new_rt, "-R", os.environ["GITHUB_REPOSITORY"]], check=False)
        log("TikTok refresh token rotated and saved")
    return r["access_token"]


def upload_draft(video_path, secret_name):
    tok = access_token(secret_name)
    size = os.path.getsize(video_path)
    if size <= MAX_CHUNK:
        chunk, count = size, 1
    else:
        chunk = 10 * 1024 * 1024
        count = size // chunk          # the last chunk absorbs the remainder (TikTok allows up to 128MB for it)
    auth = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8"}
    body = json.dumps({"source_info": {"source": "FILE_UPLOAD", "video_size": size, "chunk_size": chunk, "total_chunk_count": count}}).encode()
    r = _req(f"{API}/post/publish/inbox/video/init/", body, auth)
    if r.get("error", {}).get("code") not in (None, "ok"):
        raise RuntimeError(f"TikTok init failed: {r['error']}")
    up, pid = r["data"]["upload_url"], r["data"]["publish_id"]
    with open(video_path, "rb") as f:
        for i in range(count):
            start = i * chunk
            end = size - 1 if i == count - 1 else start + chunk - 1
            f.seek(start); part = f.read(end - start + 1)
            _req(up, part, {"Content-Type": "video/mp4", "Content-Length": str(len(part)),
                            "Content-Range": f"bytes {start}-{end}/{size}"}, method="PUT")
    for _ in range(40):                 # wait until TikTok has it in the inbox
        st = _req(f"{API}/post/publish/status/fetch/", json.dumps({"publish_id": pid}).encode(), auth)
        status = st.get("data", {}).get("status")
        if status in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE"):
            return {"publish_id": pid, "status": status}
        if status == "FAILED":
            raise RuntimeError(f"TikTok upload failed: {st['data'].get('fail_reason')}")
        time.sleep(6)
    return {"publish_id": pid, "status": "PROCESSING"}
