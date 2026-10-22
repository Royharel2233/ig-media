"""Slide renderer (approved v2 look). Slide kinds: cover / fact / cta.
Each slide: {kind, photo (local path), kicker, head, sub[], source, blur}."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance, ImageFont, features

assert features.check("raqm"), "Pillow needs libraqm for Hebrew layout"
FONT = os.path.join(os.path.dirname(__file__), "fonts", "Heebo.ttf")
RED = (235, 40, 50)
SIZES = {"cover": (120, 50), "fact": (90, 50), "cta": (88, 48)}
FIX = lambda t: t.replace('"AI', '‏"AI')


def font(size, weight):
    f = ImageFont.truetype(FONT, size, layout_engine=ImageFont.Layout.RAQM)
    f.set_variation_by_name(weight)
    return f


def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for wd in text.split(" "):
        test = wd if not cur else cur + " " + wd
        if draw.textlength(test, font=f, direction="rtl", language="he") <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def bg(path, w, h, text_top, blur=0):
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.4))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    im = ImageEnhance.Color(im).enhance(0.85)
    grad = Image.new("L", (1, h))
    start = text_top - 380
    for y in range(h):
        if y < start:
            a = 60
        elif y < text_top - 40:
            a = 60 + int(170 * ((y - start) / (text_top - 40 - start)) ** 1.3)
        else:
            a = 232
        grad.putpixel((0, y), a)
    grad = grad.resize((w, h))
    return Image.composite(Image.new("RGB", (w, h), (8, 10, 18)), im, grad)


def render(s, idx, w, h, bottom_safe, top_safe, outdir, brand):
    kind = s.get("kind", "fact")
    head = FIX(s["head"]); subs = [FIX(p) for p in s.get("sub", [])]
    kicker = s.get("kicker"); source = s.get("source")
    d = ImageDraw.Draw(Image.new("RGB", (w, h)))
    margin = 84; maxw = w - margin * 2 - 30; brand_h = 90
    avail = h - top_safe - bottom_safe - brand_h
    hs, ps = SIZES[kind]
    while True:
        hf = font(hs, "Black" if kind == "cover" else "ExtraBold"); pf = font(ps, "Regular")
        hl = wrap(d, head, hf, maxw); hlh = int(hs * 1.18)
        pls = [wrap(d, p, pf, maxw) for p in subs]; plh = int(ps * 1.42)
        kf = font(36, "Bold"); klh = 62 if kicker else 0
        sf = font(30, "Regular"); sls = wrap(d, FIX(source), sf, maxw) if source else []
        slh = (34 + len(sls) * 42) if source else 0
        total = klh + len(hl) * hlh + sum(30 + len(p) * plh for p in pls) + slh
        if total <= avail * 0.7 or hs <= 44:
            break
        hs -= 4; ps = max(34, ps - 1)
    right = w - margin
    y = h - bottom_safe - brand_h - total - 30
    img = bg(s["photo"], w, h, y, s.get("blur", 0)); d = ImageDraw.Draw(img)
    if kicker:
        d.text((right, y), kicker, font=kf, fill=RED, anchor="ra", direction="rtl", language="he"); y += klh
    d.rectangle([right + 14, y + int(hlh * .16), right + 22, y + len(hl) * hlh - int(hlh * .16)], fill=RED)
    for line in hl:
        d.text((right, y), line, font=hf, fill=(255, 255, 255), anchor="ra", direction="rtl", language="he"); y += hlh
    for p in pls:
        y += 30
        for line in p:
            d.text((right, y), line, font=pf, fill=(228, 228, 232), anchor="ra", direction="rtl", language="he"); y += plh
    if source:
        y += 34
        for line in sls:
            d.text((right, y), line, font=sf, fill=(165, 168, 178), anchor="ra", direction="rtl", language="he"); y += 42
    by = h - bottom_safe - 40; bf = font(34, "Black")
    tw = d.textlength(brand, font=bf, direction="rtl", language="he")
    d.text((right, by), brand, font=bf, fill=(255, 255, 255), anchor="rm", direction="rtl", language="he")
    cx = right - tw - 22
    d.ellipse([cx - 9, by - 9, cx + 9, by + 9], fill=RED)
    d.line([margin, by, cx - 26, by], fill=(255, 255, 255), width=2)
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, f"{idx:02d}.jpg"), quality=92)


def run(slides, out, brand):
    """Renders every slide in both formats: feed 4:5 and story/reel 9:16."""
    for i, s in enumerate(slides, 1):
        render(s, i, 1080, 1350, 70, 120, os.path.join(out, "feed_4x5"), brand)
        render(s, i, 1080, 1920, 420, 260, os.path.join(out, "story_9x16"), brand)
