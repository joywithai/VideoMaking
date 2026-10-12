# 02 — SCRIPT ও SRT: লেখা, cue split, টাইমিং

## script.txt (`output/{topic}Script.txt`)
- পুরো narration — videoDetails.md-এর script অংশ হুবহু ব্যবহার করবে (নিজে থেকে পাল্টাবে না)।
- English tech term ইংরেজিই থাকবে। এক লাইন = এক বাক্য/শ্বাস-গ্রুপ (cue-র সাথে মিলিয়ে)।
- SRT-এর শব্দ = script-এর শব্দ (ক্রম হুবহু) — **কখনো প্যারাফ্রেজ নয়** (mistakes.md M10)।

## cue split নিয়ম
1. এক cue = এক বাক্য বা শ্বাস-গ্রুপ; সাধারণত ২–৭ সেকেন্ড, ~৪–২২ শব্দ।
2. দীর্ঘ বাক্য হলে অর্থ-বিচ্ছিন্ন না করে কমায়/সংযোগে ভাগ করবে।
3. Wrap: প্রতিটা cue সর্বোচ্চ ২ লাইন, লাইনপ্রতি ~৪৫ অক্ষর, ভারসাম্যপূর্ণ wrap
   (এক লাইনে অর্ধেক কেটে দ্বিতীয় লাইনে ছোট টুকরো রাখবে না)।
4. Cue সংখ্যা স্ক্রিপ্ট লাইন অনুযায়ী — JWT: ৭২টি।

## SRT (`output/{topic}Audio.srt`)
- আদর্শ SRT: `n / HH:MM:SS,mmm --> HH:MM:SS,mmm / লেখা / খালি লাইন`।
- **Cue time আসবে TTS chunk boundary থেকে** (skill 01 chunking) — এটাই সবচেয়ে নির্ভুল।
  cue.s = chunk শুরু, cue.e = chunk শেষ (back-to-back concat হলে সঞ্চিত দৈর্ঘ্য)।
- যদি chunk দৈর্ঘ্য না থাকে, তবে speech activity (VAD island) দিয়ে যাচাই/সংশোধন করবে
  (skill 03) — কিন্তু cue সীমা বড়ভাবে নড়াবে না (M2)।
- SRT লেখা = script লেখা; শেষ যাচাই: `output/{topic}Audio.srt` এর সব শব্দ মিলিয়ে দেখবে
  `{topic}Script.txt`-এর সব শব্দের সাথে (সংখ্যা ও ক্রম)।

## যাচাই
- cue সংখ্যা == script লাইন/বাক্য সংখ্যা।
- প্রথম cue শুরু ≈ অডিও শুরু; শেষ cue শেষ ≈ অডিও শেষ।
- `skills/tools/validate_output.py` চালাবে।
