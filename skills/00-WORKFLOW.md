# 00 — WORKFLOW: এই agent কীভাবে একটা ভিডিও বানায়

> এই file পড়া বাধ্যতামূলক। এরপর skills/ folder-এর **সব** .md file এবং mistakes.md পড়বে,
> তারপর তবে কোনো কাজ শুরু করবে। কোনো skill skip করা যাবে না।

## Agent-এর কাজ
এই repo একটা **reusable video-making agent**। ইউজার প্রতিবার শুধু `videoDetails.md` ভরে দেয়,
বাকি সব — voiceover, SRT, motion-graphics video.html, thumbnails, upload metadata — agent নিজে বানায়।

## ধাপ ০ — videoDetails.md তৈরি (কাজের আগে — ইউজার/প্রযোজনা AI)
`videoDetails.md` আসে দুই পথে: ইউজার নিজে ভরে, অথবা রিপোতে `start` comment দিলে
**টেক লবন প্রযোজনা AI** (`root/systemPrmpt.txt` system prompt দিয়ে) ইন্টারঅ্যাক্টিভ
সেটআপ (MODE/category/count/duration/age/style) করে, স্ক্রিপ্ট+প্ল্যান বানিয়ে
videoDetails.md draft দেয় → ইউজার যাচাই/edit করে "ok" দেয়।
- প্রযোজনা AI-র output হুবহু videoDetails.md ফরম্যাট (১-৯ অংশ: সেটিংস, Script,
  Scene Plan, Asset Plan, **Download List** ({topic} প্রিফিক্স নাম, watermark-ছাড়া),
  Thumbnail Brief, Upload Brief, Growth, Extra Rules)।
- Agent কাজ শুরুর আগে যাচাই করবে: script আছে, topic slug আছে, Download List-এর
  ফাইল নামগুলো src/-এ আছে কিনা (না থাকলে ইউজারকে বলবে)।

## সম্পূর্ণ ধাপ (এই ক্রমেই, কোনো ধাপ বাদ নয়)

1. **পড়ো** — `videoDetails.md` পুরো মনোযোগ দিয়ে পড়ো। topic slug, script, scene plan,
   asset/download plan, thumbnail brief, upload brief, extra rules — সব নোট করো।
   কিছু অস্পষ্ট থাকলে কাজ শুরুর আগে জিজ্ঞাসা করো।
2. **পড়ো** — `skills/` এর সব .md (`00` থেকে `07`) + `skills/mistakes.md`।
   mistakes.md মানে "এই ভুলগুলো কোনোদিন কোরো না"।
3. **প্রস্তুতি** — `materials/` ও `src/` যাচাই করো (কোন ছবি/gif/logo/script-নির্দিষ্ট অ্যাসেট আছে)।
   videoDetails.md-এর Download List/Asset Plan অনুযায়ী ছবি mapping করো
   (নাম মিলিয়ে; যেগুলো নেই সেগুলোর জন্য ইউজারকে বলো বা AI-art/সাজানো ডিজাইন দাও)।
4. **পরিবেশ** — `/home/user/.venv` না থাকে তৈরি করো:
   `python3 -m venv /home/user/.venv && /home/user/.venv/bin/pip install numpy soundfile pillow`
   (ffmpeg নেই; mp3 encode লাগলে `lameenc` ব্যবহার করো। সবসময় `/home/user/.venv/bin/python`।)
5. **Script** — `output/{topic}Script.txt` বানাও (skill 02)।
   videoDetails.md-এ script দেওয়া থাকলে সেটাই ব্যবহার করো, কখনো নিজে থেকে লেখা পাল্টে দেবে না।
6. **Voiceover** — `output/{topic}Audio.mp3` (skill 01)। materials/NewsAudio.mp3-এর **একই কণ্ঠে**।
   প্রতিটা sentence/line আলাদা chunk-এ generate করো + chunk দৈর্ঘ্য সংরক্ষণ করো (skill 03)।
7. **SRT** — `output/{topic}Audio.srt` (skill 02)। cue time আসবে chunk boundary থেকে (হুবহু exact)।
8. **Word align** — `skills/tools/align_words.py` চালিয়ে word-level `video_data.json` বানাও (skill 03)।
9. **video.html** — `skills/template-video.html` কপি করে beats/bindings বানাও (skill 04)।
   **প্রতিটা visual বলা শব্দের সময়েই আসবে**। সব text card-এর ভেতরে padding নিয়ে, কোনো overlap নয়।
10. **Thumbnails** — `output/{topic}Thumbnail_1/2/3.png` (skill 05)।
11. **Upload details** — `output/{topic}UploadDetails.txt` (skill 06)।
12. **Package + Validate** — skill 07 এর checklist চালাও: `skills/tools/validate_output.py`।
    সব সবুজ না হওয়া পর্যন্ত থামবে না।
13. **সেলফ-চেক** — নিজে নিজে ধরো: screenshot/QA মানসম্মত কি না (skill 04/05 এর QA ধাপ)।
14. **mistakes.md আপডেট** — এই build-এ যেকোনো ভুল হয়েছে (ইউজার ধরালে বা নিজে ধরা পড়েছে)
    সাথে সাথে `skills/mistakes.md`-তে যোগ করো (নিচের "সেলফ-লার্নিং" নিয়ম দেখো)।
15. **Commit + Push** এবং ইউজারকে রিপোর্ট (কী বানানো হলো, checklist ফলাফল, নতুন mistake যোগ হলে সেটা)।

## সেলফ-লার্নিং (বাধ্যতামূলক feature)
যখনই কোনো ভুল ধরা পড়ে — ইউজার feedback থেকে, validation থেকে, বা নিজের যাচাইতে —
**ঠিক তখনই, কাজ চালিয়ে যাওয়ার আগে**, `skills/mistakes.md`-তে entry যোগ করবে
(entry format ওই ফাইলে দেওয়া আছে)। উদ্দেশ্য: পরের কোনো build একই ভুল দ্বিতীয়বার না করা।

## নিয়ম
- সব output যাবে `output/` তে, নাম `{topic}` prefix দিয়ে (skill 07)। অন্য কোথাও নয়।
- মাঝপথে কোনো transform কখনো নিজের input file-এর উপর লিখবে না (mistakes.md #1)।
- যেকোনো সিদ্ধান্ত যা skill-এ নেই এবং risky — আগে জিজ্ঞেস করবে।
- কাজ শেষে সবসময় git commit + push (স্যান্ডবক্স রিসেট হলে কাজ যেন না হারায়)।
