#!/usr/bin/env python3
"""make_thumbnails.py — 3 YouTube thumbnails, 1280x720, subject-left / 2-line Bengali text-right.

Usage:
  make_thumbnails.py --subject art.png --bg ../materials/BG.jpg --outdir .. \
    --topic JWT \
    --t1 "JWT কীভাবে কাজ করে?" "Header · Payload · Signature" \
    --t2 "নিজেই বুঝে ফেলো!" "JSON Web Token সহজ ভাষায়" \
    --t3 "decode = verify নয়!" "JWT-এর গোপন সত্য!"

Writes {outdir}/{topic}Thumbnail_1/2/3.png. Subject art: pass the path; if the
subject file has no alpha, its near-black background is keyed out. Fonts are
fetched from google/fonts via api.github.com (raw.githubusercontent blocked) to
skills/tools/fonts/ and reused.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
API = "https://api.github.com/repos/google/fonts/contents/ofl/hindsiliguri/"
W, H = 1280, 720
ORANGE = (255, 122, 26)
WHITE = (255, 255, 255)


def ensure_font(name):
    os.makedirs(FONT_DIR, exist_ok=True)
    p = os.path.join(FONT_DIR, name)
    if os.path.exists(p):
        return p
    req = urllib.request.Request(API + name, headers={"Accept": "application/vnd.github.raw+json",
                                                      "User-Agent": "videomaking"})
    data = urllib.request.urlopen(req, timeout=60).read()
    if data[:4] == b"\x00\x01\x00\x00" or len(data) > 10000:
        open(p, "wb").write(data)
    else:  # JSON response with b64
        j = json.loads(data)
        open(p, "wb").write(base64.b64decode(j["content"]))
    return p


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
    out = img.copy()
    out.putalpha(mask)
    return out


def key_black(im):
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r + g + b < 60:
                px[x, y] = (r, g, b, 0)
    return im


def fit_text(draw, text, font_path, max_w, start=130, minv=48):
    s = start
    while s > minv:
        f = ImageFont.truetype(font_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 4
    return ImageFont.truetype(font_path, minv)


def make(bg_path, subject_path, out, line1, line2):
    base = Image.open(bg_path).convert("RGB").resize((W, H))
    # darken/blur bg
    base = base.filter(ImageFilter.GaussianBlur(6))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    base = Image.blend(base, dark, 0.62)

    # subject left
    if subject_path and os.path.exists(subject_path):
        sub = Image.open(subject_path)
        sub = sub.convert("RGBA")
        if sub.getchannel("A").getextrema()[0] == 255:  # no transparency → key black
            sub = key_black(sub)
        sub = sub.resize((520, 520))
        sub = rounded(sub, 40)
        base.paste(sub, (60, 110), sub)
        # orange glow strip
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([10, 60, 620, 660], fill=(255, 110, 20, 70))
        glow = glow.filter(ImageFilter.GaussianBlur(40))
        base = Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")

    draw = ImageDraw.Draw(base)
    font_path = ensure_font("HindSiliguri-Bold.ttf")
    max_w = 560
    f1 = fit_text(draw, line1, font_path, max_w, 124)
    f2 = fit_text(draw, line2, font_path, max_w, 116)
    x = 650
    y1, y2 = 200, 360
    for text, font, y, col, stroke in ((line1, f1, y1, WHITE, 10), (line2, f2, y2, ORANGE, 10)):
        # shadow
        for dx, dy in ((4, 5), (2, 3)):
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0))
    base.save(out)
    print("saved", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--bg", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--t1", nargs=2, required=True)
    ap.add_argument("--t2", nargs=2, required=True)
    ap.add_argument("--t3", nargs=2, required=True)
    a = ap.parse_args()
    for i, pair in enumerate((a.t1, a.t2, a.t3), 1):
        make(a.bg, a.subject, os.path.join(a.outdir, f"{a.topic}Thumbnail_{i}.png"), pair[0], pair[1])


if __name__ == "__main__":
    main()
