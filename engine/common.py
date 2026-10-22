"""Shared helpers: repo paths, page config, Pexels and Instagram API calls."""
import json, os, time, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = json.load(open(os.path.join(ROOT, "pages.json"), encoding="utf-8"))
REPO = os.environ.get("GITHUB_REPOSITORY", "Royharel2233/ig-media")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
IG = "https://graph.instagram.com/v26.0"


def log(*a):
    print(*a, flush=True)


def http(url, method="GET", data=None, headers=None, timeout=60):
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return json.loads(raw) if raw[:1] in (b"{", b"[") else raw
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {url.split('?')[0]} -> HTTP {e.code}: {e.read()[:500]!r}")


# ---------- Pexels ----------
def pexels(path, **params):
    key = os.environ["PEXELS_API_KEY"]
    return http(f"https://api.pexels.com/v1/{path}?{urllib.parse.urlencode(params)}", headers={"Authorization": key})


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ig-media-bot"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


# ---------- Instagram ----------
def ig_token(page):
    name = PAGES[page]["token_secret"]
    tok = os.environ.get(name, "")
    if not tok:
        raise RuntimeError(f"Missing secret {name} for page {page}. Add it in repo Settings > Secrets and variables > Actions.")
    return tok


_UID = {}


def ig(page, method, path, **params):
    """Graph call for a page. A leading 'me/' is replaced by the account's IG user id."""
    params["access_token"] = ig_token(page)
    if path.startswith("me/"):
        if page not in _UID:
            _UID[page] = http(f"{IG}/me?fields=user_id&access_token={params['access_token']}")["user_id"]
        path = str(_UID[page]) + path[2:]
    if method == "GET":
        return http(f"{IG}/{path}?{urllib.parse.urlencode(params)}")
    return http(f"{IG}/{path}", method="POST", data=params)


def wait_container(page, cid, max_s=300):
    t = time.time()
    while True:
        st = ig(page, "GET", cid, fields="status_code,status")
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {cid} {code}: {st.get('status')}")
        if time.time() - t > max_s:
            raise RuntimeError(f"container {cid} still {code} after {max_s}s")
        time.sleep(6)


def raw_url(path):
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{urllib.parse.quote(path)}"


def wait_public(url, tries=24):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=20) as r:
                if r.status == 200:
                    return
        except Exception:
            pass
        time.sleep(5)
    raise RuntimeError(f"not public yet: {url}")
