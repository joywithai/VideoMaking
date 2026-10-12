#!/usr/bin/env python3
"""build_video.py (AICode) — skills/template-video.html থেকে output/AICodeVideo.html বানায়।
repo root থেকে চালাতে হবে:  python3 skills/tools/builds/AICode/build_video.py [video_data.json]

ইঞ্জিন (JS/CSS) অপরিবর্তিত; শুধু DATA + BEATS + topic-স্ট্রিং বদলায় (skills/04)।
Binding কখনো মেমোরি থেকে নয় — প্রতিটা data-w video_data.json থেকে resolve হয় (M8)।
placeholder:  @@W:cueIdx:wordOffset@@  -> সেই শব্দের global index
              @@T:cueIdx:wordOffset@@  -> সেই শব্দের সময় (সেকেন্ড)
              @@KIN:cueIdx@@           -> ওই cue-র সব শব্দ word-by-word kinetic span
              @@TXT:cueIdx:wordOffset@@-> সেই শব্দের লেখা (data থেকে)
"""
import json
import re
import sys

import os
_DEFAULT_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AICode_video_data.json')
DATA = json.load(open(sys.argv[1] if len(sys.argv) > 1 else _DEFAULT_DATA, encoding='utf-8'))
CUES, WORDS = DATA['cues'], DATA['words']
CUE_G = {}
for gi, w in enumerate(WORDS):
    CUE_G.setdefault(w[3], []).append(gi)

def W(c, k=0):
    g = CUE_G[c]
    return g[min(k, len(g) - 1)]

def TXT(c, k=0):
    return CUES[c]['w'][min(k, len(CUES[c]['w']) - 1)][0]

def KIN(c):
    return ' '.join(f'<i class="el kw" data-w="{gi}">{w[0]}</i>' for gi, w in zip(CUE_G[c], CUES[c]['w']))

def resolve(h):
    h = re.sub(r'@@W:(\d+):(\d+)@@', lambda m: str(W(int(m.group(1)), int(m.group(2)))), h)
    h = re.sub(r'@@T:(\d+):(\d+)@@', lambda m: f"{WORDS[W(int(m.group(1)), int(m.group(2)))][1]:.2f}", h)
    h = re.sub(r'@@TXT:(\d+):(\d+)@@', lambda m: TXT(int(m.group(1)), int(m.group(2))), h)
    h = re.sub(r'@@KIN:(\d+)@@', lambda m: KIN(int(m.group(1))), h)
    return h

G = lambda s: f'<div class="gbox glass el pop" data-w="{s[0]}"' + (f' data-t="{s[1]}"' if len(s) > 1 else '') + '>'
IMG = ('<img src="../src/{n}" alt="" onerror="this.style.display=\'none\'" '
       'style="width:{w}px;height:{h}px;object-fit:cover;border-radius:26px;'
       'border:1px solid rgba(255,255,255,.22);box-shadow:0 24px 60px rgba(0,0,0,.55)">')

B = []  # (c0, c1, html)
def beat(c0, c1, h):
    B.append((c0, c1, h))

G = lambda w, ic, t1, t2, extra='', dt='': (
    f'<div class="gbox glass el pop" data-w="{w}"' + (f' data-t="{dt}"' if dt else '') + f'{extra}>'
    f'<div class="ic">{ic}</div><div class="t1">{t1}</div><div class="t2">{t2}</div></div>')
IMG = ('<img class="el pop" data-w="{w}" src="../src/{n}" alt="" onerror="this.style.display=\'none\'" '
       'style="width:{s}px;height:{s}px;object-fit:cover;border-radius:{r};'
       'border:1px solid rgba(255,255,255,.22);box-shadow:0 24px 60px rgba(0,0,0,.55)">')
def img(w, n, s=400, r='26px', dt=''):
    t = IMG.format(w=w, n=n, s=s, r=r)
    return t.replace('<img ', f'<img data-t="{dt}" ', 1) if dt else t

# ── 1 (cue 0) hook: reaction + compare card ─────────────────────────────
beat(0, 0, '''<div class="bmid">
  <div class="wm el pop" data-w="@@W:0:0@@" style="font-size:112px"><span class="o">বাপ</span><span>রে বাপ!</span></div>
  <div class="row" style="gap:38px">
    ''' + G('@@W:0:5@@', '⌨️', 'কোড <span style="color:#28c878">+৩০%</span>', 'AI লেখে অনেক বেশি কোড') + '''
    <div class="neq el" data-w="@@W:0:9@@" data-t="0.2">≠</div>
    ''' + G('@@W:0:10@@', '📦', 'সফটওয়্যার <span style="color:#FF7A1A">বাড়ে না</span>', 'শেষ হওয়া কাজ প্রায় একই', ' hot', '0.15') + '''
  </div>
</div>''')

# ── 2 (cue 1) open loop ────────────────────────────────────────────────
beat(1, 1, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:1:0@@" style="font-size:44px;padding:34px 56px">এই বাড়তি কোড যায় <span class="k">কোথায়?</span> ❓</div>
  <div class="row" style="gap:26px;margin-top:8px">
    <div class="arrow el" data-w="@@W:1:3@@" data-t="0.3">⬇</div>
    ''' + G('@@W:1:3@@', '🔒', 'উত্তর লক করা', 'ভিডিওর শেষে খুলবে', ' hot', '0.45') + '''
  </div>
</div>''')

# ── 3 (cue 2) Harvard ─────────────────────────────────────────────────
beat(2, 2, '''<div class="bmid">
  <div class="vpanel glass el pop" data-w="@@W:2:0@@" style="width:940px">
    <div class="ic">🎓</div>
    <div class="vt">Harvard University-র দুই গবেষক</div>
    <div class="row" style="gap:20px;margin-top:6px">
      <div class="minipart el" data-w="@@W:2:5@@" data-t="0.1">Fiona Chen</div>
      <div class="minipart hot el" data-w="@@W:2:8@@" data-t="0.2">James Stratton</div>
    </div>
    <div class="vs2 el" data-w="@@W:2:1@@" data-t="0.3" style="margin-top:20px">নতুন working paper — সফটওয়্যার উৎপাদনের bottleneck</div>
  </div>
</div>''')

# ── 4 (cue 3) 718 firms ───────────────────────────────────────────────
beat(3, 3, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:3:0@@" style="font-size:30px">তাঁরা দেখেছেন একটা কোম্পানির না —</div>
  <div style="text-align:center" class="el pop" data-w="@@W:3:2@@" data-t="0.15">
    <div class="counter" style="font-size:190px">৭১৮</div>
    <div class="bigtext el" data-w="@@W:3:3@@" data-t="0.2" style="font-size:40px;margin-top:6px">সফটওয়্যার <b>কোম্পানি</b></div>
  </div>
</div>''')

# ── 5 (cue 4) scale chips ─────────────────────────────────────────────
beat(4, 4, '''<div class="bmid">
  <div class="grid" style="gap:30px">
    <div class="claim glass el pop" data-w="@@W:4:0@@" style="min-width:390px">
      <div class="c1">৭,২৫,৯৩৮</div><div class="c2">কর্মীর ডেটা</div></div>
    <div class="claim glass el pop" data-w="@@W:4:5@@" data-t="0.15" style="min-width:390px">
      <div class="c1">৩০ কোটি</div><div class="c2">work event</div></div>
    <div class="claim glass el pop" data-w="@@W:4:9@@" data-t="0.3" style="min-width:390px">
      <div class="c1">২০২১ → মার্চ ২০২৬</div><div class="c2">সময়কাল</div></div>
  </div>
</div>''')

# ── 6 (cue 5) shock number + kinetic ──────────────────────────────────
beat(5, 5, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:5:0@@" style="font-size:32px">শুনেন শুনেন — সংখ্যাটা আবার পড়ুন</div>
  <div class="wm el pop" data-w="@@W:5:3@@" style="font-size:200px"><span class="o">৩০</span><span>কোটি!</span></div>
</div>
<div class="kin">@@KIN:5@@</div>''')

# ── 7 (cues 6-7) bar chart — আনুপাতিক উচ্চতা ───────────────────────────
BAR = lambda w, pct, col, lab, sub, dt='': f'''<div style="text-align:center;width:250px" class="el pop" data-w="{w}"{f' data-t="{dt}"' if dt else ''}>
      <div style="font:700 44px 'JetBrains Mono',monospace;color:{col}">+{pct}</div>
      <div style="width:170px;height:{int(pct.rstrip('%'))*10}px;margin:12px auto 0;border-radius:20px 20px 0 0;
        background:linear-gradient(180deg,{col}dd,{col}33);border:1px solid {col}88"></div>
      <div style="font-size:27px;color:#fff;margin-top:16px;line-height:1.4">{lab}</div>
      <div style="font-size:19px;color:rgba(255,255,255,.6);margin-top:4px">{sub}</div></div>'''
beat(6, 6, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:6:0@@" style="font-size:30px">AI coding agent ঢোকার পর কোড বেড়েছে</div>
  <div class="row" style="align-items:flex-end;gap:48px;margin-top:10px">
    ''' + BAR('@@W:6:5@@', '৩০%', '#28c878', 'লাইন অফ কোড', 'গড়ে') + '''
  </div>
</div>''')

# ── 8 (cue 7) commit + PR bars ─────────────────────────────────────────
beat(7, 7, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:7:0@@" style="font-size:30px">একই সময়ে বেড়েছে —</div>
  <div class="row" style="align-items:flex-end;gap:48px;margin-top:10px">
    ''' + BAR('@@W:7:0@@', '২০%', '#8ecbff', 'commit', 'সেভ পয়েন্ট') + BAR('@@W:7:3@@', '২৩%', '#FF7A1A', 'pull request', 'কোড জমার আবেদন', '0.2') + '''
  </div>
</div>''')

# ── 8 (cue 8) coding agent definition + robot art + kinetic ────────────
beat(8, 8, '''<div class="bmid">
  <div class="row" style="gap:44px;align-items:center">
    ''' + img('@@W:8:0@@', 'AICode_robot_coder.png') + '''
    <div class="vpanel glass el" data-w="@@W:8:0@@" data-t="0.2" style="width:780px;text-align:left">
      <div class="vt" style="font-size:38px">AI coding agent মানে —</div>
      <div class="vs2" style="font-size:29px">যে <span style="color:#ff8c33;font-weight:700">AI</span> নিজেই কোড লিখে<br>জমা দিয়ে দেয় — শুধু সাহায্য করে না</div>
    </div>
  </div>
</div>
<div class="kin">@@KIN:8@@</div>''')

# ── 9 (cue 9) commit = save point ─────────────────────────────────────
beat(9, 9, '''<div class="bmid">
  ''' + G('@@W:9:1@@', '💾', 'commit = কোডের <span style="color:#ff8c33">সেভ পয়েন্ট</span>', 'কাজের একেকটা সংরক্ষিত ধাপ', ' style="max-width:640px"') + '''
</div>''')

# ── 10 (cue 10) PR definition + kinetic ───────────────────────────────
beat(10, 10, '''<div class="bmid">
  <div class="vpanel glass el pop" data-w="@@W:10:0@@" style="width:1020px">
    <div class="ic">📥</div>
    <div class="vt">pull request (PR) মানে —</div>
    <div class="vs2 el" data-w="@@W:10:6@@" data-t="0.1">একটা আবেদন: <span style="color:#ff8c33;font-weight:700">"চেক করে যোগ করুন"</span></div>
  </div>
</div>
<div class="kin">@@KIN:10@@</div>''')

# ── 11 (cue 11) chef analogy intro ────────────────────────────────────
beat(11, 11, '''<div class="bmid">
  <div class="row" style="gap:44px;align-items:center">
    ''' + img('@@W:11:1@@', 'AICode_chef.png', s=420) + '''
    <div class="vpanel glass el" data-w="@@W:11:0@@" data-t="0.15" style="width:720px;text-align:left">
      <div class="vt" style="font-size:38px">ধরেন একটা রেস্টুরেন্ট 🍽️</div>
      <div class="vs2 el" data-w="@@W:11:2@@" data-t="0.2" style="font-size:29px">বাবুর্চি নতুন একটা <b style="color:#ff8c33">রেসিপি</b> বানালেন<br>= ডেভেলপার নতুন কোড লিখলেন</div>
    </div>
  </div>
</div>''')

# ── 12 (cue 12) chef checks → approve → menu ──────────────────────────
STEP = lambda w, ic, t, s, dt='': G(w, ic, t, s, ' style="min-width:330px;max-width:390px"', dt)
beat(12, 12, '''<div class="bmid">
  <div class="row" style="gap:24px;align-items:center">
    ''' + STEP('@@W:12:0@@', '🔍', 'head chef পরীক্ষা করেন', 'কোড review করা') + '''
    <div class="arrow el" data-w="@@W:12:4@@" data-t="0.15">➜</div>
    ''' + STEP('@@W:12:4@@', '✅', 'approve করলে', 'ঠিক থাকলে তবেই', '0.2') + '''
    <div class="arrow el" data-w="@@W:12:7@@" data-t="0.15">➜</div>
    ''' + STEP('@@W:12:7@@', '📖', 'মেনুতে ওঠে', 'production-এ যায়', '0.3') + '''
  </div>
</div>''')

# ── 13 (cue 13) code review label ─────────────────────────────────────
beat(13, 13, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:13:0@@" style="font-size:29px">সেই পরীক্ষা করাই হলো —</div>
  <div class="formula glass el pop" data-w="@@W:13:4@@" data-t="0.15" style="font-size:56px;padding:44px 66px">
    পরীক্ষা করাই = <b>code review</b></div>
</div>''')

# ── 14 (cue 14) no significant change + kinetic ───────────────────────
beat(14, 14, '''<div class="bmid">
  <div class="vpanel glass el pop" data-w="@@W:14:1@@" style="width:960px">
    <div class="ic">📋</div>
    <div class="vt">শেষ হওয়া টাস্কের হার</div>
    <div class="row" style="gap:22px;margin-top:4px">
      <div class="minipart el" data-w="@@W:14:3@@" data-t="0.2">resolved: ৩.৬৭ → ৩.৭৯</div>
      <div class="minipart hot el" data-w="@@W:14:5@@" data-t="0.35">statistically significant নয়</div>
    </div>
    <div class="vs2" style="margin-top:18px">Jira issue ও epic — পরিবর্তন প্রায় শূন্য</div>
  </div>
</div>
<div class="kin">@@KIN:14@@</div>''')

# ── 15 (cue 15) 12% ruled out gauge ───────────────────────────────────
beat(15, 15, '''<div class="bmid">
  <div class="pill glass bad el" data-w="@@W:15:0@@" style="font-size:30px">গবেষকরা যা উড়িয়েই দিয়েছেন</div>
  <div class="el pop" data-w="@@W:15:1@@" data-t="0.2" style="width:1080px;text-align:center">
    <div style="position:relative;height:64px;border-radius:999px;background:linear-gradient(90deg,rgba(40,200,120,.55),rgba(255,255,255,.14));border:1px solid rgba(255,255,255,.22)">
      <div style="position:absolute;left:12%;top:-18px;bottom:-18px;width:6px;background:#ff4d4d;box-shadow:0 0 22px rgba(255,77,77,.9)"></div>
      <div style="position:absolute;left:12%;top:-64px;transform:translateX(-50%);font:700 30px 'JetBrains Mono',monospace;color:#ff4d4d">১২%</div>
    </div>
    <div class="bigtext el" data-w="@@W:15:3@@" data-t="0.25" style="font-size:34px;margin-top:26px">১২%-এর বেশি লাভ <b>অসম্ভব</b> ধরা হয়েছে</div>
  </div>
</div>''')

# ── 16 (cue 16) funnel image ──────────────────────────────────────────
beat(16, 16, '''<div class="bmid">
  <div class="row" style="gap:44px;align-items:center">
    <div class="vpanel glass el" data-w="@@W:16:0@@" style="width:660px;text-align:left">
      <div class="vt" style="font-size:40px">তাহলে সময় গেল <span style="color:#FF7A1A">কোথায়?</span></div>
      <div class="vs2 el" data-w="@@W:16:4@@" data-t="0.15" style="font-size:34px;font-weight:700;color:#ff8c33">code review-তে!</div>
    </div>
    ''' + img('@@W:16:4@@', 'AICode_funnel.png', dt='0.2') + '''
  </div>
</div>''')

# ── 17 (cue 17) timeline 7 → 10.5 days ────────────────────────────────
beat(17, 17, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:17:0@@" style="font-size:31px">আগে PR merge হতে সময় লাগত</div>
  <div class="timelineWrap el" data-w="@@W:17:1@@" data-t="0.2" style="margin-top:22px">
    <div class="timeline"></div>
    <div class="tmark" style="left:15%"><i></i><span class="el" data-w="@@W:17:4@@" data-t="0.25">৭ দিন</span><small>আগে</small></div>
    <div class="tmark" style="left:80%"><i style="background:#ff4d4d;box-shadow:0 0 20px rgba(255,77,77,.9)"></i><span class="el" data-w="@@W:17:8@@" data-t="0.25" style="color:#ff8c33">সাড়ে ১০ দিন</span><small>এখন</small></div>
  </div>
  <div class="formula glass hot el pop" data-w="@@W:17:11@@" data-t="0.2" style="font-size:44px">+৪৯% সময়</div>
</div>''')

# ── 18 (cue 18) comments +35%, returns ~2x ────────────────────────────
beat(18, 18, '''<div class="bmid">
  <div class="grid" style="gap:36px">
    <div class="claim glass el pop" data-w="@@W:18:3@@" style="min-width:450px">
      <div class="c1">+৩৫%</div><div class="c2">প্রতি PR-তে review কমেন্ট</div></div>
    <div class="claim glass hot el pop" data-w="@@W:18:8@@" data-t="0.2" style="min-width:450px">
      <div class="c1">≈২ গুণ</div><div class="c2">ফেরত পাঠানোর হার<br>("একটু ঠিক করে আনেন")</div></div>
  </div>
</div>''')

# ── 19 (cue 19) reviewers +14% ────────────────────────────────────────
beat(19, 19, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:19:0@@" style="font-size:30px">কোম্পানিগুলো তখন কী করল?</div>
  <div class="vpanel glass el pop" data-w="@@W:19:2@@" data-t="0.2" style="width:920px">
    <div class="ic">🧑‍💻🧑‍💻🧑‍💻<span style="color:#ff8c33">🧑‍💻</span></div>
    <div class="vt">review-তে আরও মানুষ বসাল</div>
    <div class="vs2 el" data-w="@@W:19:6@@" data-t="0.2" style="font-size:34px;font-weight:700;color:#ff8c33">reviewer বেড়েছে +১৪%</div>
  </div>
</div>''')

# ── 20 (cue 20) pattern interrupt ─────────────────────────────────────
beat(20, 20, '''<div class="bmid">
  <div class="slab glass on el pop" data-w="@@W:20:0@@" style="width:660px;min-height:300px">
    <div class="num">PATTERN INTERRUPT</div>
    <div class="name" style="font-size:74px">একটু থামুন! ✋</div>
    <div class="hint">AI কি তাহলে কাজের না?</div>
  </div>
  <div class="pill glass bad el" data-w="@@W:20:6@@" data-t="0.25" style="font-size:38px">না ভাই — মোটেও না ❌</div>
</div>''')

# ── 21 (cue 21) accent quote ──────────────────────────────────────────
beat(21, 21, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:21:0@@" style="font-size:29px">গবেষকদের নিজের সিদ্ধান্ত</div>
  <div class="code glass hot el pop" data-w="@@W:21:3@@" data-t="0.2" style="font-size:46px;line-height:1.5;max-width:1500px;text-align:center">
    <span class="str">"code review becomes<br>the bottleneck"</span></div>
</div>''')

# ── 22 (cue 22) question pill ─────────────────────────────────────────
beat(22, 22, '''<div class="bmid">
  <div class="vpanel glass el pop" data-w="@@W:22:0@@" style="width:940px">
    <div class="ic">🤖</div>
    <div class="vt">AI তো নিজেই review করতে পারে!</div>
    <div class="vs2">তাহলে সমস্যাটা মিটল না কেন?</div>
  </div>
</div>''')

# ── 23 (cue 23) donut 80% ─────────────────────────────────────────────
beat(23, 23, '''<div class="bmid">
  <div class="row" style="gap:52px;align-items:center">
    <div class="vpanel glass el" data-w="@@W:23:0@@" style="width:680px;text-align:left">
      <div class="vt" style="font-size:38px">মার্চ ২০২৬ নাগাদ</div>
      <div class="vs2 el" data-w="@@W:23:5@@" data-t="0.2" style="font-size:28px">AI code review টুল ব্যবহার করছে</div>
    </div>
    <div class="el pop" data-w="@@W:23:3@@" data-t="0.15" style="width:360px;height:360px;border-radius:50%;
      background:conic-gradient(#FF6B00 0 80%, rgba(255,255,255,.13) 80% 100%);display:flex;align-items:center;justify-content:center">
      <div style="width:242px;height:242px;border-radius:50%;background:#0b0b0f;display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div style="font:700 68px 'JetBrains Mono',monospace;color:#ff8c33">৮০%</div>
        <div style="font-size:19px;color:rgba(255,255,255,.66);text-align:center;line-height:1.4">কোম্পানি</div></div>
    </div>
  </div>
</div>''')

# ── 24 (cue 24) AI review share + kinetic ─────────────────────────────
beat(24, 24, '''<div class="bmid">
  <div class="pill glass bad el" data-w="@@W:24:0@@" style="font-size:30px">কিন্তু কাজের অংশটা দেখুন</div>
  <div class="grid" style="gap:34px;margin-top:6px">
    <div class="claim glass el pop" data-w="@@W:24:4@@" data-t="0.15" style="min-width:440px">
      <div class="c1">মাত্র ২৩%</div><div class="c2">review কমেন্ট লিখেছে AI</div></div>
    <div class="claim glass hot el pop" data-w="@@W:24:8@@" data-t="0.3" style="min-width:440px">
      <div class="c1">মাত্র ১১%</div><div class="c2">PR-তে AI-এর একটা কমেন্ট পড়েছে</div></div>
  </div>
</div>
<div class="kin">@@KIN:24@@</div>''')

# ── 25 (cue 25) human owns the gate ───────────────────────────────────
beat(25, 25, '''<div class="bmid">
  <div class="vpanel glass hot el pop" data-w="@@W:25:1@@" style="width:900px">
    <div class="ic">🚪</div>
    <div class="vt">👤 গেটটা এখনো মানুষের হাতেই</div>
    <div class="vs2">human still owns the gate</div>
  </div>
</div>''')

# ── 26 (cue 26) price $20 ─────────────────────────────────────────────
beat(26, 26, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:26:0@@" style="font-size:30px">এই গেটের দাম কত?</div>
  <div class="row" style="gap:26px;margin-top:8px">
    <div class="minipart el" data-w="@@W:26:3@@" data-t="0.1">Cursor</div>
    <div class="minipart el" data-w="@@W:26:5@@" data-t="0.2">Claude Code</div>
  </div>
  <div class="formula glass hot el pop" data-w="@@W:26:9@@" data-t="0.15" style="font-size:58px">মাসে ২০ ডলার</div>
</div>''')

# ── 27 (cue 27) BDT ───────────────────────────────────────────────────
beat(27, 27, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:27:0@@" style="font-size:29px">আমাদের টাকায় (১ USD ≈ ৳১২৩)</div>
  <div style="text-align:center" class="el pop" data-w="@@W:27:3@@" data-t="0.15">
    <div class="counter" style="font-size:170px">৳২,৪৬০</div>
    <div class="bigtext" style="font-size:36px">প্রতি <b>মাসে</b></div>
  </div>
</div>''')

# ── 28 (cue 28) client pays for features + kinetic ────────────────────
beat(28, 28, '''<div class="bmid">
  <div class="vs" style="gap:44px">
    <div class="vpanel glass el pop" data-w="@@W:28:4@@" style="width:620px">
      <div class="ic">❌</div>
      <div class="vt" style="font-size:38px">লাইনের সংখ্যা</div>
      <div class="vs2">এটা গুনে লাভ নেই</div></div>
    <div class="neq el" data-w="@@W:28:5@@" data-t="0.2">≠</div>
    <div class="vpanel glass el pop" data-w="@@W:28:7@@" data-t="0.25" style="width:620px;background:rgba(40,200,120,.12);border:2px solid rgba(60,220,140,.38)">
      <div class="ic">✅</div>
      <div class="vt" style="font-size:38px">শেষ হওয়া ফিচার</div>
      <div class="vs2">ক্লায়েন্ট এটারই টাকা দেয়</div></div>
  </div>
</div>
<div class="kin">@@KIN:28@@</div>''')

# ── 29 (cue 29) BD angle ──────────────────────────────────────────────
beat(29, 29, '''<div class="bmid">
  <div class="vpanel glass hot el pop" data-w="@@W:29:0@@" style="width:1040px">
    <div class="ic">🇧🇩</div>
    <div class="vt">বাংলাদেশের লাখ লাখ ফ্রিল্যান্সার</div>
    <div class="row" style="gap:20px;margin-top:6px">
      <div class="minipart el" data-w="@@W:29:3@@" data-t="0.2">Upwork</div>
      <div class="minipart el" data-w="@@W:29:3@@" data-t="0.3">Fiverr</div>
      <div class="minipart hot el" data-w="@@W:29:6@@" data-t="0.35">লোকাল সফটওয়্যার কোম্পানি</div>
    </div>
    <div class="vs2 el" data-w="@@W:29:6@@" data-t="0.5" style="margin-top:16px">এই কথাটাই বড়</div>
  </div>
</div>''')

# ── 30 (cue 30) 2am client message + kinetic ──────────────────────────
beat(30, 30, '''<div class="bmid">
  <div class="el pop" data-w="@@W:30:0@@" style="width:940px">
    <div style="display:flex;justify-content:space-between;font-size:23px;color:rgba(255,255,255,.6);margin-bottom:12px">
      <span class="mono">ক্লায়েন্ট চ্যাট</span><span class="mono el" data-w="@@W:30:1@@" data-t="0.15">🕑 রাত ০২:০০</span></div>
    <div class="glass el" data-w="@@W:30:5@@" data-t="0.2" style="padding:34px 40px;border-radius:26px 26px 26px 6px;text-align:left">
      <div style="font-size:40px;color:#fff;line-height:1.45;font-weight:600">"কাজটা কবে শেষ হবে?"</div></div>
    <div class="el" data-w="@@W:30:3@@" data-t="0.3" style="text-align:right;margin-top:14px;font-size:24px;color:rgba(255,255,255,.55)">review-তে আটকে আছে ⏳</div>
  </div>
</div>
<div class="kin">@@KIN:30@@</div>''')

# ── 31 (cue 31) good news: no job loss ────────────────────────────────
beat(31, 31, '''<div class="bmid">
  <div class="vpanel glass el pop" data-w="@@W:31:0@@" style="width:940px;background:rgba(40,200,120,.13);border:2px solid rgba(60,220,140,.4)">
    <div class="ic">✅</div>
    <div class="vt el" data-w="@@W:31:5@@" data-t="0.2">ভালো খবর — চাকরি কারও যায়নি!</div>
    <div class="vs2">এই study-তে কর্মী ছাঁটাইয়ের প্রমাণ মেলেনি</div>
  </div>
</div>''')

# ── 32 (cue 32) flat headcount line ───────────────────────────────────
beat(32, 32, '''<div class="bmid">
  <div class="vpanel glass el" data-w="@@W:32:0@@" style="width:1100px">
    <div class="vt" style="font-size:36px">কর্মীসংখ্যায় উল্লেখযোগ্য পতন নেই</div>
    <svg viewBox="0 0 900 150" style="width:900px;height:150px;margin-top:10px" class="el" data-w="@@W:32:1@@" data-t="0.2">
      <line x1="20" y1="75" x2="880" y2="75" stroke="#28c878" stroke-width="7" stroke-linecap="round"/>
      <line x1="20" y1="140" x2="880" y2="140" stroke="rgba(255,255,255,.18)" stroke-width="2"/>
    </svg>
    <div class="row" style="gap:20px;margin-top:12px">
      <div class="minipart el" data-w="@@W:32:4@@" data-t="0.3">Jellyfish × LinkedIn cross-check</div></div>
  </div>
</div>''')

# ── 33 (cue 33) AI isn't eating jobs — slow review is + kinetic ───────
beat(33, 33, '''<div class="bmid">
  <div class="row" style="gap:34px;align-items:center">
    ''' + G('@@W:33:2@@', '🙅', 'AI চাকরি <span style="color:#28c878">খাচ্ছে না</span>', 'গবেষণায় প্রমাণ মেলেনি') + '''
    <div class="arrow el" data-w="@@W:33:5@@" data-t="0.15">➜</div>
    ''' + G('@@W:33:7@@', '🐌', '<span style="color:#FF7A1A">ধীর যাচাই</span> খাচ্ছে', 'সময় নষ্ট হচ্ছে এখানেই', ' hot', '0.2') + '''
  </div>
</div>
<div class="kin">@@KIN:33@@</div>''')

# ── 34 (cue 34) solution 3 steps + kinetic ────────────────────────────
beat(34, 34, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:34:0@@" style="font-size:32px">সমাধান — গবেষকদের পরামর্শ</div>
  <div class="step glass el pop" data-w="@@W:34:1@@" data-t="0.15" style="width:1140px">
    <div class="chk">১</div><div class="txt">ছোট ছোট PR দিন<small>বড় বদল review করা কঠিন</small></div></div>
  <div class="step glass el pop" data-w="@@W:34:4@@" data-t="0.3" style="width:1140px">
    <div class="chk">২</div><div class="txt">review ব্যবস্থা আগে সাজান<small>টেস্ট ও automated check আগেভাগে</small></div></div>
  <div class="step glass el pop" data-w="@@W:34:6@@" data-t="0.45" style="width:1140px">
    <div class="chk">৩</div><div class="txt">শেষ হওয়া কাজ গুনুন<small>লাইন অফ কোড নয়</small></div></div>
</div>
<div class="kin">@@KIN:34@@</div>''')

# ── 35 (cue 35) caveat ────────────────────────────────────────────────
beat(35, 35, '''<div class="bmid">
  <div class="pill glass warn el" data-w="@@W:35:0@@" style="font-size:30px">⚠️ সতর্কতা — গবেষণার সীমাবদ্ধতা</div>
  <div class="grid" style="gap:30px;margin-top:6px">
    <div class="claim glass el pop" data-w="@@W:35:3@@" data-t="0.15" style="min-width:440px">
      <div class="c1" style="font-size:32px">observational study</div><div class="c2">কারণ প্রমাণ নয় — সহসম্বন্ধ</div></div>
    <div class="claim glass el pop" data-w="@@W:35:7@@" data-t="0.3" style="min-width:440px">
      <div class="c1" style="font-size:32px">মার্চ ২০২৬</div><div class="c2">এর পরের কোনো ডেটা নেই</div></div>
  </div>
</div>''')

# ── 36 (cue 36) prediction ────────────────────────────────────────────
beat(36, 36, '''<div class="bmid">
  <div class="vpanel glass hot el pop" data-w="@@W:36:0@@" style="width:1040px">
    <div class="ic">🔮</div>
    <div class="vt">আগামী এক বছরে লড়াই হবে —</div>
    <div class="vs2 el" data-w="@@W:36:7@@" data-t="0.2" style="font-size:34px;font-weight:700;color:#ff8c33">কে দ্রুত যাচাই করতে পারে</div>
  </div>
</div>''')

# ── 37 (cues 37-38) comment trigger + প্রতিশ্রুতি একসাথে ─────────────
beat(37, 38, '''<div class="bmid">
  <div class="pill glass el" data-w="@@W:37:0@@" style="font-size:32px">এবার বলুন তো —</div>
  <div class="pill glass warn el" data-w="@@W:37:3@@" data-t="0.2" style="font-size:38px">আপনার <span class="k">review</span> কে করে?</div>
  <div class="row" style="gap:34px;margin-top:4px">
    ''' + G('@@W:37:7@@', '🧑‍💻', 'আপনি নিজে?', 'নিজের কোড নিজে পড়েন', '', '0.15') + '''
    <div class="neq el" data-w="@@W:37:8@@" data-t="0.2" style="font-size:44px">নাকি</div>
    ''' + G('@@W:37:9@@', '🤖', 'AI টুল?', 'AI দিয়ে review করান', ' hot', '0.3') + '''
  </div>
  <div class="pill glass good el" data-w="@@W:38:0@@" style="font-size:31px">💬 কমেন্টে লিখুন — এক এক করে সব পড়ব</div>
</div>''')

# ── 39 (cue 39) like / share ──────────────────────────────────────────
beat(39, 39, '''<div class="bmid">
  <div class="row" style="gap:40px">
    ''' + G('@@W:39:2@@', '👍', 'লাইক দিন', 'ভালো লাগলে') + '''
    ''' + G('@@W:39:6@@', '🔗', 'শেয়ার করুন', 'ডেভেলপার বন্ধুদের সাথে', ' hot', '0.2') + '''
  </div>
</div>''')

# ── 40 (cue 40) subscribe ─────────────────────────────────────────────
beat(40, 40, '''<div class="bmid">
  <div class="vpanel glass hot el pop" data-w="@@W:40:1@@" style="width:1040px">
    <div class="ic">🔔</div>
    <div class="vt">Tech Lobon</div>
    <div class="vs2 el" data-w="@@W:40:4@@" data-t="0.2" style="font-size:30px">subscribe করে বেল আইকন চালু রাখুন</div>
    <div class="row" style="gap:18px;margin-top:14px">
      <div class="minipart hot el" data-w="@@W:40:0@@" data-t="0.1">আপনাদের চ্যানেল</div></div>
  </div>
</div>''')

# ── 41 (cue 41) outro ─────────────────────────────────────────────────
beat(41, 41, '''<div class="bmid">
  <div class="row" style="gap:40px;align-items:center">
    ''' + img('@@W:41:0@@', 'AICode_anchor.png', s=300,
              r='50%;border:3px solid rgba(255,107,0,.55);box-shadow:0 0 60px rgba(255,107,0,.35)') + '''
    <div style="text-align:left">
      <div class="bigtext el pop" data-w="@@W:41:0@@" data-t="0.15" style="font-size:62px;text-align:left">টেক নিউজ <b>মজার ঢঙে!</b></div>
      <div class="pill glass el" data-w="@@W:41:5@@" data-t="0.3" style="font-size:34px;margin-top:20px">আবার দেখা হবে — বাই বাই 👋</div>
    </div>
  </div>
</div>''')

# ── assemble ──
html = open('skills/template-video.html', encoding='utf-8').read()
beats_js = ',\n'.join('{{c0:{}, c1:{}, h:`{}`}}'.format(a, b, resolve(h).replace('`', '\\`').replace('${', '\\${'))
                    for a, b, h in B)
data_js = json.dumps({"duration": DATA["duration"], "cues": DATA["cues"], "words": DATA["words"]},
                     ensure_ascii=False, separators=(',', ':'))

# DATA block
html = re.sub(r'const DATA = \{.*?\};\n', lambda m: 'const DATA = ' + data_js + ';\n',
              html, count=1, flags=re.S)
# BEATS block (from 'const BEATS = [' to the closing '];')
html = re.sub(r'const BEATS = \[.*?\n\];', lambda m: 'const BEATS = [\n' + beats_js + '\n];', html, count=1, flags=re.S)
# topic strings / overlays / audio
html = html.replace('<title>template-video — {topic}</title>',
                    '<title>AICode Video — AI কোড লেখে ৩০% বেশি, সফটওয়্যার বানায় না | Tech Lobon</title>')
html = html.replace('<h1>JWT — <b>JSON Web Token</b></h1>',
                    '<h1>AI কোড লেখে <b>৩০% বেশি</b></h1>')
html = html.replace('<p>প্রতি line-এর word অনুযায়ী synced motion-graphics<br>clean board · Liquid Glass · SRT-accurate</p>',
                    '<p>Harvard study: ৭১৮ কোম্পানির ডেটা বলছে<br>আসল bottleneck কোড লেখা নয় — <b>code review</b></p>')
html = html.replace('<p>decode মানে verify নয় — Signature এবং claims যাচাই বাধ্যতামূলক</p>',
                    '<p>বেশি কোড লেখা মানেই বেশি কাজ শেষ করা নয়<br>আসল দক্ষতা এখন — দ্রুত ও নির্ভুল যাচাই করা</p>')
html = html.replace('JWTAudio.mp3', 'AICodeAudio.mp3')
html = html.replace("audio.src = 'news/AICodeAudio.mp3';", "audio.src = '../output/AICodeAudio.mp3';")
html = html.replace('/* asset fallbacks (paths relative to this file) */',
                    '/* asset fallbacks (paths relative to this file) — AICode build v1 */')
open('output/AICodeVideo.html', 'w', encoding='utf-8').write(html)
print(f"beats: {len(B)}  cues covered: {sum(b - a + 1 for a, b, _ in B)} / {len(CUES)}")
print("kinetic cues:", [i for i in range(len(CUES)) if '@@KIN' in ''.join(h for a, b, h in B if a <= i <= b)])
print("written output/AICodeVideo.html", len(html), "bytes")
