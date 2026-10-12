# 04 — VIDEO ENGINE: video.html motion-graphics (সম্পূর্ণ spec)

## উদ্দেশ্য
`output/{topic}Video.html` — ১৯২০×১০৮০ stage, audio-সিঙ্ক মোশন-গ্রাফিক্স।
`skills/template-video.html` কপি করে শুধু DATA + BEATS বদলাবে। ইঞ্জিন (JS) অপরিবর্তিত রাখতে হবে।

## স্থাপত্য
- `#stage` 1920×1080, `fit()` দিয়ে viewport-এ স্কেল (letterbox)। নিচে `#playerBar` (কন্ট্রোল — stage-এর বাইরে/নিচে)।
- `const DATA = {duration, cues[], words[]}` — skill 03 এর video_data.json থেকে embed (compact JSON)।
- `const BEATS = [{c0, c1, h}, ...]` — প্রতিটা beat কিছু cue জুড়ে একটা ভিজ্যুয়াল দৃশ্য (HTML `h`)।
- ইঞ্জিন: প্রতিটা `.el` element-এর `data-w` (global word index, প্রাধান্য) বা `data-c` (cue) + `data-t` (offset) থাকে;
  `triggerAt()` = `WORDS[data-w].s - 0.12` (kinetic শব্দ ছাড়া সব ০.১২s আগে আসে)।
- Beat বদল: fade ০.৩s; element entry ০.২৮s। প্রতিটা beat enter-এ `.el` reset।
- Audio: `src="{topic}Audio.mp3"` + fallback `output/{topic}Audio.mp3`; ভুল হলে error box।

## বিট ডিজাইন নিয়ম (কঠোর)
1. **সিঙ্ক:** প্রতিটা visual/text trigger হবে সংশ্লিষ্ট বাক্যের **শুরুর শব্দে** (clause-start word index),
   কখনো মাঝ/শেষের শব্দে নয় (M6)। binding বানানোর ধাপ:
   a. video_data.json থেকে word table প্রিন্ট (`[idx]word@time`);
   b. প্রতিটা element-এর জন্য বাক্যের প্রথম প্রাসঙ্গিক শব্দ বেছে নাও;
   c. **semantic check:** প্রতিটা `data-w` এর শব্দটি element-এর সাথে মিলছে কি না মিলিয়ে দেখো
      (স্ক্রিপ্ট দিয়ে validate_output.py করে)।
2. **লেআউট band (overlap নিষিদ্ধ — M5):**
   - `.bmid` = সম্পূর্ণ stage-এ কেন্দ্রীভূত স্ট্যাক (pill + content); `.beat.has-kin .bmid` নিচে ২৫০px সংরক্ষণ।
   - `.kin` = নিচের band (top:852px) — শুধু kinetic সাবটাইটেল।
   - একটা লেখা/এলিমেন্ট অন্যের ওপর পড়লে গ্রহণযোগ্য নয়; প্রতিটা বিটের layout যাচাই করবে।
3. **Card padding (M4/M7):** সব card (gbox/claim/vpanel/slab/step/machine/pill/code) block-layout,
   ৩২px+ padding, child-এর margin, `line-height ≥1.4`, `text-wrap:balance`, `overflow-wrap:break-word`।
   template-এর self-heal JS (scrollHeight>clientHeight → paddingBottom বাড়ায়) সবসময় রাখবে।
   **CSS selector লেখার পর byte-মিল যাচাই করবে** (M4: `.g\boxed`-এর মতো escape টাইপো নয়)।
4. **Kinetic fallback (ইউজার নিয়ম):** যে line-এর জন্য কোনো ভালো card নেই — সেই লেখার প্রতিটা শব্দ
   নিচের band-এ word-by-word pop করবে (`.el.kw[data-w]`), যেন কিছুই miss না যায়।
   দীর্ঘ/বহু-খণ্ডের বাক্যে kinetic রাখা ভালো। Stage-তে স্থায়ী caption/logo/scene-chip নিষিদ্ধ।
5. **আইকন:** সাধারণ emoji (👤 🖥️ 🔐 🛡️ …) — জটিল/bitmap emoji এড়াবে (render টুটতে পারে)।
6. **দ্রুততা:** entry ≤০.৩s; ট্রিগার ০.১২s lead; কোনো animation >১s নয় (count-up ছাড়া)।

## থিম (Liquid Glass)
কালো/ডার্ক BG (`materials/BG.jpg` — template fallback: `BG.jpg` → `../materials/BG.jpg`),
glass card (`backdrop-filter` blur + সাদা হালকা border + shadow), accent `#FF6B00`,
Hind Siliguri (Bengali) + JetBrains Mono (code), হালকা particle/kb-zoom।

## যাচাই (build শেষে — বাধ্যতামূলক)
1. `node --check` এর জন্য `<script>` বের করে চালাও — সিনট্যাক্স পরিষ্কার।
2. ৪১+ beat সংখ্যা; প্রতিটা cue exactly-once beat range-এ পড়েছে।
3. প্রতিটা `data-w < len(words)`; প্রতিটা trigger সময় তার beat-এর cue span-এর ভেতরে।
4. প্রতিটা `data-w` এর শব্দ মিলে যায় element-এর অর্থের সাথে (semantic)।
5. kinetic span ক্রমানুসারিতা ঠিক।
6. সব CSS selector match করছে (M4) + self-heal JS আছে।
`skills/tools/validate_output.py` এই যাচাইগুলো চালায়।

## উদাহরণ
`output/JWTVideo.html` — ৪১ beat, ১৭৬ word trigger, ৮ kinetic block; সব যাচাই পাস করা।
