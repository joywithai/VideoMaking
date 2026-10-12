# 07 — OUTPUT PACKAGING: ফাইলনাম, ডেলিভারি, ফাইনাল চেকলিস্ট

## ফাইলনাম (কঠোর)
সব কিছু `output/`-এ, `{topic}` প্রিফিক্সসহ (topic = videoDetails.txt `[topic]`, ছোট ইংরেজি slug):

```
output/{topic}Audio.mp3          # ভয়েসওভার
output/{topic}Audio.srt          # word-accurate subtitle
output/{topic}Script.txt         # হুবহু narration
output/{topic}Video.html         # মোশন-গ্রাফিক্স ভিডিও (ব্রাউজারে চলবে)
output/{topic}Thumbnail_1.png    # ১২৮০×৭২০
output/{topic}Thumbnail_2.png
output/{topic}Thumbnail_3.png
output/{topic}UploadDetails.txt  # YouTube + Facebook metadata
```

পুরোনো টেমপ্লেট নাম (`video.html`, `script.txt`, `uploadDetails.txt`, `Thumbnail_1.png`)
কখনো ডেলিভারি নাম হবে না — সবসময় `{topic}` প্রিফিক্স (M-এর পাঠ)।
build-এর মাঝের কাজচিত্র (video_data.json ইত্যাদি) `output/`-এ রাখবে না; লাগলে gitignore-এর বাইরে টেম্প লোকেশনে।

## ফাইনাল চেকলিস্ট (প্রতিটা build শেষে — বাধ্যতামূলক)
1. [ ] ৮টা ফাইলই উপরের নামে আছে; অডিও চলছে; থাম্বনেইল ১২৮০×৭২০।
2. [ ] `skills/tools/validate_output.py {topic}` → `RESULT: PASS ✅`।
3. [ ] SRT লেখা == Script লেখা (শব্দ ও ক্রম); শব্দগুলো অডিওতে শোনা যায়।
4. [ ] প্রতিটা visual element সঠিক শব্দের সময়ে আসে (semantic binding — skills/04)।
5. [ ] কোনো overlap নেই; সব card-এ লেখা পূর্ণ padding সহ ভেতরে (M4/M5/M7 — স্ক্রিনে নিজে দেখে নিন)।
6. [ ] UploadDetails: description ১৯০০+ শব্দ, timestamp নেই, tags ৪০+, FB hashtag ১০।
7. [ ] ভয়েস একই কণ্ঠ (NewsAudio.mp3 মিল); আলাদা ভিন্ন voice নয়।
8. [ ] build-এ যেকোনো ভুল হয়েছিল → `skills/mistakes.md`-তে সাথে সাথে লেখা হয়েছে (self-learning)।

## ডেলিভারি
- রিপোর্টে উল্লেখ করবে: ফাইল তালিকা, দৈর্ঘ্য, cue/beat সংখ্যা, যাচাই ফল, নতুন mistake এন্ট্রি (থাকলে)।
- ইউজার চাইলে branch/PR বানাতে পারে; না চাইলে সরাসরি পুশ।
