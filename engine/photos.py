"""Stage A: for every jobs/<page>/<slot>/queries.json without candidates.json,
search Pexels and write candidates.json + one contact sheet per post for Claude to review."""
import glob, json, os, sys
from PIL import Image, ImageDraw, ImageFont
from common import ROOT, pexels, download, log

FONT = os.path.join(os.path.dirname(__file__), "fonts", "Heebo.ttf")


def sheet(items, dest):
    W, H, cols = 240, 320, 6
    rows = (len(items) + cols - 1) // cols or 1
    img = Image.new("RGB", (cols * W, rows * (H + 34)), "white")
    d = ImageDraw.Draw(img); f = ImageFont.truetype(FONT, 22)
    for k, it in enumerate(items):
        try:
            im = Image.open(it["_thumb"]).convert("RGB"); im.thumbnail((W, H))
            x, y = (k % cols) * W, (k // cols) * (H + 34)
            img.paste(im, (x, y)); d.text((x + 4, y + H + 4), str(it["id"]), fill="black", font=f)
        except Exception as e:
            log("thumb fail", it["id"], e)
    img.save(dest, quality=82)


def main():
    done = 0
    for q in sorted(glob.glob(os.path.join(ROOT, "jobs", "*", "*", "queries.json"))):
        jobdir = os.path.dirname(q)
        if os.path.exists(os.path.join(jobdir, "candidates.json")):
            continue
        spec = json.load(open(q, encoding="utf-8"))
        out, tmp = {}, os.path.join("/tmp", "thumbs")
        for post, queries in spec["posts"].items():
            seen, items = set(), []
            for query in queries:
                res = pexels("search", query=query, orientation="portrait", per_page=6)
                for p in res.get("photos", []):
                    if p["id"] in seen:
                        continue
                    seen.add(p["id"])
                    thumb = download(p["src"]["medium"], os.path.join(tmp, f"{p['id']}.jpg"))
                    items.append({"id": p["id"], "query": query, "alt": p.get("alt", ""),
                                  "photographer": p.get("photographer", ""), "_thumb": thumb})
            os.makedirs(os.path.join(jobdir, "candidates"), exist_ok=True)
            sheet(items, os.path.join(jobdir, "candidates", f"sheet_{post}.jpg"))
            out[post] = [{k: v for k, v in it.items() if not k.startswith("_")} for it in items]
            log(post, len(items), "candidates")
        json.dump(out, open(os.path.join(jobdir, "candidates.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        done += 1
    log("jobs processed:", done)


if __name__ == "__main__":
    sys.exit(main())
