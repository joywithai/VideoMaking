#!/usr/bin/env python3
"""AICodeUploadDetails.txt — videoDetails.md §৭ থেকে extraction করে JWT-ফরম্যাটে লেখা।

হাতে টাইপ না করে regex দিয়ে নিই, যেন approved brief আর ফাইল হুবহু এক থাকে।
Validator: 【 DESCRIPTION 】→【 TAGS 】 এর মধ্যে ≥১৫০০ শব্দ; 【 TAGS 】→পরের খালি লাইন ≥৪০ tags।
"""
import re
import textwrap

md = open('videoDetails.md', encoding='utf-8').read()
sec7 = md[md.index('## ৭.'):md.index('## ৮.')]

def fence_after(marker):
    i = sec7.index(marker)
    m = re.search(r'```\s*\n(.*?)\n\s*```', sec7[i:], re.S)
    return textwrap.dedent(m.group(1)).strip()

desc = fence_after('**📋 DESCRIPTION')
tags = fence_after('**🏷️ TAGS')
pinned = fence_after('**📌 Pinned comment')

titles = re.findall(r'^\s+\d+\.\s+`([^`]+)`', sec7[sec7.index('TITLE OPTIONS'):sec7.index('DESCRIPTION')], re.M)
fb = sec7[sec7.index('**📘 FACEBOOK'):]
fb_title = re.search(r'\*\*Title:\*\*\s+`([^`]+)`', fb).group(1)
fb_hash = re.search(r'\*\*HASHTAGS \(10\):\*\*\s+`([^`]+)`', fb).group(1)
fb_tags = re.search(r'\*\*TAGS \(10\):\*\*\s+`([^`]+)`', fb).group(1)

assert len(titles) == 3, titles
BAR = '──────────────────────────────────────────'
EQ = '═' * 64
out = f"""{EQ}
UPLOAD DETAILS — AI Coding Agent / Harvard Study Video (Bangla)
{EQ}


{BAR}
YOUTUBE
{BAR}

【 TITLE OPTIONS (3) 】

1. {titles[0]}

2. {titles[1]}

3. {titles[2]}


【 DESCRIPTION 】

{desc}


【 TAGS 】

{tags}


{BAR}
FACEBOOK
{BAR}

【 TITLE 】

{fb_title}

【 HASHTAGS (10) 】

{fb_hash}

【 TAGS (10) 】

{fb_tags}


{BAR}
PINNED COMMENT (ready to paste)
{BAR}

{pinned}
"""
open('output/AICodeUploadDetails.txt', 'w', encoding='utf-8').write(out)

# — স্ব-যাচাই (validator-এর নিয়ম আগাম) —
d = out[out.index('【 DESCRIPTION 】') + len('【 DESCRIPTION 】'):out.index('【 TAGS 】')]
t = out[out.index('【 TAGS 】') + len('【 TAGS 】'):]
t = t.strip().split('\n')[0]
dw, tn = len(d.split()), len([x for x in t.split(',') if x.strip()])
print(f"description words: {dw} (need ≥1500) {'✅' if dw >= 1500 else '❌'}")
print(f"tags: {tn} (need ≥40) {'✅' if tn >= 40 else '❌'}")
print("titles:", len(titles), "| fb hashtags:", len(fb_hash.split()), "| fb tags:", len(fb_tags.split(',')))
