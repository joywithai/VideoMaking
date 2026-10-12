# 01 — VOICE: একই কণ্ঠে (NewsAudio.mp3) voiceover তৈরি

## উদ্দেশ্য
প্রতিটা ভিডিওতে **একই কণ্ঠ** — নতুন কোনো ভিন্ন voice gen হবে না।
`materials/NewsAudio.mp3` হলো সেই canonical voice reference (বাংলা news-পাঠের সুর, স্পষ্ট, মাঝারি গতি)।
`materials/NewsScript.txt` সেই sample-এর লেখা — tone/pace মিলিয়ে দেখার জন্য।

## নিয়ম
1. **একই voice:** যে TTS/voice-clone টুলই ব্যবহার হোক, প্রথমে NewsAudio.mp3 শুনে/মিলিয়ে সেই কণ্ঠ
   নির্বাচন করবে (Timbre: পরিষ্কার বাংলা উপস্থাপনা, hype কম, সমান গতি)।
   Arena-র `generate_speech` ব্যবহার হলে: একবার voice select করে **পুরো ভিডিওতে সেই একই voice_id** ব্যবহার করবে —
   মাঝপথে কখনো voice বদলাবে না। যে voice_id ব্যবহার হয়েছে সেটা রিপোর্টে উল্লেখ করবে।
2. **গতি/সুর:** ~২.১–২.৪ শব্দ/সেকেন্ড; বিরাম যুক্তিসঙ্গত (কমা/দাঁড়িতে ছোট পজ); অতিরিক্ত নাটকীয়তা নয়।
3. **English tech term** ইংরেজিই থাকবে (JWT, Header, Payload, Signature, HS256… বাংলা উচ্চারণে বিকৃত নয়)।
4. **CHUNK-BY-CHUNK generate (অত্যন্ত জরুরি):** পুরো script একসাথে নয় — **প্রতিটা ভবিষ্যৎ SRT cue
   আলাদা chunk-এ** বলাবে/generate করবে। প্রতিটা chunk-এর দৈর্ঘ্য (সেকেন্ড) নোট রাখবে।
   এতে cue time হুবহু exact পাওয়া যায় (skill 02/03) — অ্যালাইন কষ্ট নেই।
5. **Format:** MP3, 160 kbps, mono, স্যাম্পলরেট ৪৪.১kHz (লাগলে `lameenc`), প্রয়োজনে WAV থেকে encode।
   সম্পূর্ণ দৈর্ঘ্য স্ক্রিপ্ট অনুযায়ী (JWT উদাহরণ: ৭২ cue ≈ ৪মি৪৭সে)।
6. **concat:** chunk গুলো back-to-back জোড়া হবে (অতিরিক্ত silence নয়)। chunk সীমাই হবে cue সীমা।
7. **নিজের যাচাই:** তৈরি mp3 দৈর্ঘ্য vs script শব্দসংখ্যা অনুপাত যাচাই (~0.4–0.5s/শব্দ স্বাভাবিক);
   উল্লেখযোগ্য ব্যবধান হলে আবার generate।

## টুল/পরিবেশ
- `/home/user/.venv/bin/python` + `numpy`, `soundfile` (mp3 decode এর জন্য), `lameenc` (encode)।
- ffmpeg **নেই** — চেষ্টা করবে না।
- স্যান্ডবক্স রিসেট হলে venv আবার বানাতে হবে (00-WORKFLOW ধাপ ৪)।

## উদাহরণ (JWT)
`output/JWTAudio.mp3` — ৪মি৪৭সে, ১৬০kbps mono, voice-00 একই কণ্ঠে ৭২ chunk,
chunk boundary থেকেই SRT cue time এসেছে।
