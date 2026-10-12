# 🎬 VideoDetails — {ভিডিওর শিরোনাম}

> **কী এটি:** একটা ভিডিওর সব ইনপুট এই ফাইলেই থাকে।
> **কীভাবে বানাবেন:** রিপোতে `start` comment দিন → Tech Lobon প্রযোজনা AI
> (`systemPrmpt.txt` সিস্টেম প্রম্পটসহ) সব প্রশ্ন করে নিয়ে এই ফাইলের draft
> দেবে → আপনি যাচাই/edit করুন → **"ok"** বলুন → ফাইলটি এখানে রাখুন/কমিট করুন →
> বিল্ড এজেন্ট `skills/` ফলো করে `output/`-এ পুরো প্যাকেজ বানাবে।
> **নোট:** মূল Script (অংশ ২) সবসময় প্লেইন টেক্সটে রাখুন — যেন আপনি নিজে
> সহজে edit করতে পারেন। যেকোনো অংশ নিজে হাতে লিখেও ভরা যায়।

**topic slug:** `{Topic}` ← ছোট ইংরেজি (JWT, PythonTips…) — সব আউটপুট
ফাইলের প্রিফিক্স হবে: {Topic}Audio.mp3, {Topic}Video.html ইত্যাদি

---

## ১. ⚙️ ভিডিও সেটিংস

| বিষয় | মান |
|---|---|
| ক্যাটাগরি | {AI / Gadgets / Mobile …} |
| খবর/গল্প সংখ্যা | {১-৫} |
| সময় লক্ষ্য | {যেমন ২:০০-২:২০ প্রতি খবর} |
| স্টাইল | {HYPE / TEACH / MIXED / DRAMA} |
| খবরের বয়সসীমা | {সর্বোচ্চ X দিন} |
| ভয়েস | একই কণ্ঠ (materials/NewsAudio.mp3 অনুযায়ী) |

---

## ২. 📝 মূল Script (narration — সম্পূর্ণ, এডিটেবল)

> নিয়ম: **এক লাইন = এক বাক্য/এক cue**। English tech term ইংরেজিই থাকবে।
> expression bracket যেমন [উত্তেজিত] রাখা যায়। এটাই ভয়েসওভার ও SRT-তে যাবে।

```
{এখানে সম্পূর্ণ script — hooks, খবর ১…N, outro}
{প্রতি লাইনে এক বাক্য}
```

---

## ৩. 🎬 Scene Plan (visual map)

> binding phrase = script-এর সেই শব্দগুলো **হুবহু**, যেগুলো বলার সময় visual
> আসবে (ভিডিও word-level sync)। যে line-এর জন্য কিছু ভাবা যায় না, সেখানে
> visual কলামে **"kinetic"** লিখুন — সেই লেখা word-by-word নিচে আসবে।

| # | কোন লেখার সাথে (binding phrase) | স্ক্রিনে কী আসবে |
|---|---|---|
| 1 | {script-এর শব্দগুলো} | {card/demo/kinetic…} |

---

## ৪. 🖼️ ছবি/Asset Plan — কার pic কোথায় লাগবে

| ছবি (ফাইল নাম) | কী/কার ছবি (expression/ভঙ্গি) | কোথায় লাগবে |
|---|---|---|
| {Topic}_anchor.png | {anchor, অবাক ভঙ্গি} | {Thumbnail 1 subject} |

---

## ৫. ⬇️ Download List (ডাউনলোড করে `src/`-এ রাখুন)

> ⚠️ সব ছবি **watermark-ছাড়া (মার্কা-ছাড়া)** হতে হবে।
> ফাইল নাম **হুবহু** নিচের মতো রাখবেন ({Topic} প্রিফিক্সসহ) — নাম মিললে
> বিল্ড এজেন্ট নিজেই বসিয়ে দেবে।

| ফাইল নাম | কী জিনিস/কার ছবি | কোথায় লাগবে | কী লিখে খুঁজবেন / লিংক |
|---|---|---|---|
| {Topic}_thumb1_subject.png | {product/face…} | Thumbnail ১ | {search keyword/link} |

---

## ৬. 🖼️ Thumbnail Brief (৩টা)

> বিল্ড এজেন্ট বানাবে: ডার্ক BG · subject বামে · ডানে ২-লাইন bold (সাদা +
> কমলা)। ৩টা আলাদা hook — ① প্রশ্ন/উদ্দীপনা ② আহ্বান ③ সত্য-ফাঁক ঢঙে।

### Thumbnail ১
- **MAIN_TEXT:** {২-৪ শব্দ} · **SUB_TEXT:** {১-২ শব্দ}
- **Subject/ছবি:** {কী থাকবে — {Topic}_…png বা AI-art} · **Mood:** {shock/pride…}

### Thumbnail ২
- **MAIN_TEXT:** … · **SUB_TEXT:** …
- **Subject/ছবি:** … · **Mood:** …

### Thumbnail ৩
- **MAIN_TEXT:** … · **SUB_TEXT:** …
- **Subject/ছবি:** … · **Mood:** …

---

## ৭. 🚀 Upload Brief

- **🎯 TITLE OPTIONS (3):**
  1. {…}
  2. {…}
  3. {…}
- **📋 DESCRIPTION (≈2000 শব্দ, timestamp ছাড়া):**
  ```
  {সম্পূর্ণ description draft}
  ```
- **🏷️ TAGS (40+):** {tag1, tag2, …}
- **📘 FACEBOOK:** Title: {…} · HASHTAGS (10): {…} · TAGS (10): {…}
- **📌 Pinned comment:** {রেডি টু ইউজ}

---

## ৮. 📈 Growth Notes (ঐচ্ছিক)

- **Shorts idea:** {৩০-৪৫সে — hook + duration + কোন অংশ}
- **Upload slot:** {যেমন সন্ধ্যা ৭-৯ BST, শুক্র/শনি}
- **CTR/engagement tip:** {…}

---

## ৯. 📌 Extra Rules (ইউজারের বিশেষ চাহিদা)

- {যেমন: "শুরুতে ৫ সেকেন্ড intro", "শেষে subscribe CTA card"}
