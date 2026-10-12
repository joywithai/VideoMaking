#!/usr/bin/env python3
"""3টা থাম্বনেইল — videoDetails.md §৬ ব্রিফ অনুযায়ী।

repo টুল skills/tools/make_thumbnails.py বদলানো হয়নি: make() ইমপোর্ট করে ৩ বার
আলাদা subject দিয়ে কল, তারপর ব্রিফের "অতিরিক্ত" chip টা নিচে আঁকা (ডান কলামের
ফাঁকা জায়গা y≈548-626; লাইন২ ের ink ৫০০px-এর ওপরেই শেষ হয়)।
Hind Siliguri Bold-এ ≠ আছে কিন্তু কোনো emoji glyph নেই — তাই chip-৩ এর ✅ বাদ।
"""
import os
import shutil
import sys

sys.path.insert(0, 'skills/tools')
from PIL import Image, ImageDraw  # noqa: E402
import make_thumbnails as mt      # noqa: E402

# ফন্ট আগেই আছে — নেটওয়ার্ক ডাউনলোড এড়াতে tools/fonts-এ কপি (gitignored)
os.makedirs('skills/tools/fonts', exist_ok=True)
dst = 'skills/tools/fonts/HindSiliguri-Bold.ttf'
if not os.path.exists(dst):
    shutil.copy('/home/user/work/fonts/HindSiliguri-Bold.ttf', dst)
FONT = mt.ensure_font('HindSiliguri-Bold.ttf')

BRIEF = [
    (1, 'src/AICode_anchor.png',       '৩০% বেশি কোড',  'কাজ বাড়ে না!',   'Harvard Study'),
    (2, 'src/AICode_chef.png',         'review শিখুন',   'নইলে দেরি!',     'AI ≠ শেষ কথা'),
    (3, 'src/AICode_robot_coder.png',  'Harvard যা বলল', 'AI সত্যিটা',     'চাকরি যায়নি!'),
]
CHIP_Y, CHIP_H, CHIP_X = 548, 78, 650


def add_chip(out, text):
    im = Image.open(out).convert('RGB')
    d = ImageDraw.Draw(im)
    f = mt.fit_text(d, text, FONT, 500, 40, 24)
    tw = d.textlength(text, font=f)
    pad = 26
    w = int(tw + pad * 2)
    box = [CHIP_X, CHIP_Y, CHIP_X + w, CHIP_Y + CHIP_H]
    d.rounded_rectangle(box, radius=20, fill=(18, 14, 12), outline=mt.ORANGE, width=4)
    d.text((CHIP_X + pad, CHIP_Y + CHIP_H / 2), text, font=f, fill=(255, 255, 255), anchor='lm')
    im.save(out)
    return box


def audit(out, box):
    """M4/M7: টেক্সট clip হয়নি, কিনারা ছোঁয়নি, chip আর লাইন২ overlap করে না।

    BG পুরো ক্যানভাস ঢাকে, তাই ink মাপা হয় শুধু টেক্সট-থ্রেশহোল্ডে (>120):
    সাদা (255) ও কমলা (255,122,26 → lum≈151) দুটোই ধরা পড়ে, blend-করা ডার্ক BG পড়ে না।
    """
    im = Image.open(out).convert('L')
    px = im.load()
    W, H = im.size
    ink = lambda x, y: px[x, y] > 120
    col = [(x, y) for x in range(620, W) for y in range(0, H) if ink(x, y)]
    top = min(y for _, y in col); bot = max(y for _, y in col)
    lft = min(x for x, _ in col); rgt = max(x for x, _ in col)
    above = max((y for x, y in col if y < box[1] - 2), default=-1)
    bgmax = max(px[x, y] for x in range(0, W, 7) for y in range(0, H, 7) if not ink(x, y))
    return dict(size=im.size, text_bbox=(lft, top, rgt, bot), bg_max_lum=bgmax,
                edge_clear=(lft > 620 and top > 20 and rgt < W - 20 and bot < H - 20),
                line2_bottom=above, gap_to_chip=box[1] - above)


for i, subject, l1, l2, chip in BRIEF:
    out = f'output/AICodeThumbnail_{i}.png'
    mt.make('materials/BG.jpg', subject, out, l1, l2)
    box = add_chip(out, chip)
    r = audit(out, box)
    print(f"  thumb{i}: size={r['size']} text_bbox={r['text_bbox']} edge_clear={r['edge_clear']} "
          f"line2_bottom={r['line2_bottom']} gap_to_chip={r['gap_to_chip']}px bg_max={r['bg_max_lum']} "
          f"chip={box} {os.path.getsize(out)//1024}KB")
    assert r['size'] == (1280, 720) and r['edge_clear'] and r['gap_to_chip'] > 12, f"thumb{i} layout fail"
print("3 thumbnails OK")
