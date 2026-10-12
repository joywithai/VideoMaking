# 🎬 VideoMaking — AI Video Agent

এই রিপোজিটরি একটা **পুনঃব্যবহারযোগ্য AI video agent**। একবার সাজানো হয়েছে — এরপর প্রতিটা
নতুন ভিডিওর জন্য শুধু `videoDetails.md` পূরণ করলেই এজেন্ট পুরো প্যাকেজ তৈরি করে দেয়:
ভয়েসওভার, SRT, HTML মোশন-গ্রাফিক্স ভিডিও, ৩টা থাম্বনেইল, এবং YouTube/Facebook upload details।
`videoDetails.md` বানাতে পারেন নিজে, অথবা **`start` comment** দিলে টেক লবন প্রযোজনা AI
(`systemPrmpt.txt` সিস্টেম প্রম্পট দিয়ে) আপনার সাথে কথা বলে বানিয়ে দেবে।

## 🗂 গঠন

```
VideoMaking/
├── README.md            ← এই টিউটোরিয়াল
├── systemPrmpt.txt      ← টেক লবন প্রযোজনা AI-র সিস্টেম প্রম্পট (videoDetails বানায়)
├── videoDetails.md      ← প্রতিটা ভিডিওর ইনপুট (আপনি/প্রযোজনা AI পূরণ করবে)
├── materials/           ← স্থায়ী উপাদান
│   ├── BG.jpg              (ভিডিও/থাম্বনেইল ব্যাকগ্রাউন্ড)
│   ├── NewsAudio.mp3       (voice reference — প্রতিটা ভিডিওতে এই একই কণ্ঠ)
│   └── NewsScript.txt      (সেই voice sample-এর লেখা)
├── src/                 ← প্রতিটা ভিডিওর নিজস্ব ছবি/GIF/logo (ঐচ্ছিক)
├── skills/              ← এজেন্টের জ্ঞানভাণ্ডার (কাজের আগে সব পড়বে)
│   ├── 00-WORKFLOW.md       (পুরো পাইপলাইন — ১৫ ধাপ)
│   ├── 01-VOICE.md          (একই কণ্ঠে ভয়েসওভার)
│   ├── 02-SCRIPT-SRT.md     (script ও SRT cue)
│   ├── 03-AUDIO-ALIGN.md    (word-level timing)
│   ├── 04-VIDEO-ENGINE.md   (HTML মোশন-গ্রাফিক্স — সম্পূর্ণ spec)
│   ├── 05-THUMBNAILS.md     (৩টা থাম্বনেইল)
│   ├── 06-UPLOAD-DETAILS.md (YouTube/Facebook metadata)
│   ├── 07-OUTPUT-PACKAGING.md (ফাইলনাম/ডেলিভারি/চেকলিস্ট)
│   ├── mistakes.md          (অতীত ভুল — কখনো পুনরাবৃত্তি হবে না; নতুন ভুল এখানেই যোগ হয়)
│   ├── template-video.html  (ভিডিও ইঞ্জিন টেমপ্লেট)
│   └── tools/               (align_words.py, validate_output.py, make_thumbnails.py)
└── output/              ← ডেলিভারি ({topic} প্রিফিক্সসহ)
    └── JWT...               (সম্পূর্ণ উদাহরণ প্যাকেজ — দেখে নিন কেমন আউটপুট আশা করা যায়)
```

## 🚀 নতুন ভিডিও বানানোর ধাপ

1. **`videoDetails.md` তৈরি করুন — দুইভাবে:**
   - **সহজ পথ:** রিপোতে **`start` comment** দিন → টেক লবন প্রযোজনা AI (`systemPrmpt.txt`)
     খবর/ক্যাটাগরি/সময়/স্টাইল জিজ্ঞেস করবে → স্ক্রিপ্ট সহ সম্পূর্ণ `videoDetails.md`
     draft দেবে → আপনি যাচাই/edit করুন (মূল script প্লেইন টেক্সটে) → **"ok"** দিন।
   - **নিজে হাতে:** নিচের ফরম্যাট অনুযায়ী নিজেই ভরুন।
2. **`videoDetails.md`-এর Download List অনুযায়ী ছবি `src/`-এ রাখুন** (watermark-ছাড়া,
   ফাইল নাম হুবহু — যেমন `{Topic}_anchor.png`)।
3. **এজেন্টকে বলুন:** "videoDetails.md অনুযায়ী ভিডিও বানাও"।
   এজেন্ট `skills/`-এর সব ফাইল পড়বে → কাজ করবে → `output/`-এ পূর্ণ প্যাকেজ দেবে →
   নিজে যাচাই করবে → নতুন কোনো ভুল পেলে সাথে সাথে `skills/mistakes.md`-তে লিখে রাখবে।
4. **ফলাফল:** `output/{topic}Audio.mp3`, `{topic}Audio.srt`, `{topic}Script.txt`,
   `{topic}Video.html`, `{topic}Thumbnail_1/2/3.png`, `{topic}UploadDetails.txt`।
   `{topic}Video.html` ব্রাউজারে খুলুন — প্লে চাপলে অডিওর সাথে সিঙ্ক মোশন-গ্রাফিক্স চলবে
   (ভিডিও রেন্ডার করে আপলোড করুন, অথবা সরাসরি screen-record করুন)।

> **videoDetails.md ফরম্যাট:** ১ সেটিংস · ২ মূল Script (প্লেইন, এক লাইন = এক cue) ·
> ৩ Scene Plan · ৪ ছবি/Asset Plan · ৫ ⬇️ Download List · ৬ Thumbnail Brief ·
> ৭ Upload Brief · ৮ Growth Notes · ৯ Extra Rules — বিস্তারিত ফাইলটিতেই লেখা আছে।

## 📐 মান নিয়ম (সংক্ষেপে)

- ভিজ্যুয়াল **বলা শব্দের সময়েই** আসবে (≤১ সেকেন্ড, লক্ষ্য ≤০.২সে)।
- কোনো লেখা/এলিমেন্ট **একে অন্যের ওপর পড়বে না**; card-এর লেখা কখনো কিনারা ছোঁয়াবে/ছেঁড়া হবে না।
- যে লেখার কোনো ভালো card নেই — সেটা নিচে word-by-word kinetic সাবটাইটেলে আসবে (কিছুই মিস নয়)।
- **প্রতিটা ভিডিওতে একই কণ্ঠ** (materials/NewsAudio.mp3 অনুযায়ী)।
- SRT-এর লেখা = script-এর লেখা (হুবহু); English tech term ইংরেজিই থাকবে।
- থাম্বনেইল: ডার্ক BG, subject বামে, ডানে ২-লাইন bold লেখা (সাদা + কমলা)।

সব বিস্তারিত নিয়ম `skills/`-এ টপিক অনুযায়ী ভাগ করা আছে; অতীতের ভুলগুলো `skills/mistakes.md`-তে।

## 🛠 টেকনোট (এজেন্টের জন্য)

- Python venv: `/home/user/.venv` (numpy, soundfile, lameenc, pillow) — বিস্তারিত `skills/00-WORKFLOW.md`।
- যাচাই: `skills/tools/validate_output.py {topic}` — প্রতিটা build শেষে চালাতে হবে।
- উদাহরণ প্যাকেজ `output/JWT*` — কাঠামো/মান মিলিয়ে দেখুন।
