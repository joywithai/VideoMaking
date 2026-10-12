# 03 — AUDIO ALIGN: word-level timing (video_data.json)

## উদ্দেশ্য
ভিডিওর প্রতিটা visual বলা শব্দের সময়ে আসবে — তাই প্রতিটা শব্দের আনুমানিক সময় লাগে।
`video_data.json` সেই ডেটা।

## নিয়ম (সংক্ষেপে)
1. **Cue time authoritative** (TTS chunk — skill 02)। অ্যালাইনমেন্ট কখনো cue সময় বদলাবে না (M2)।
2. VAD (voice activity detection) দিয়ে speech island বের করো:
   RMS উইন্ডো (২৫ms), threshold = `max(0.004, p82*0.16)`, ৩-ফ্রেম স্মুদিং,
   গ্যাপ ≤৫০ms মিলিয়ে island, দৈর্ঘ্য ≥০.১২s।
3. প্রতিটা cue-র ভেতরে: তার শব্দগুলো cue স্প্যানে সাজাও, প্রতিটা শব্দ HARD-assign হবে
   cue-জুড়ে island-এ (proportional → nearest/covering island, monotonic), একই island-এর
   শব্দগুলো island ভেতরে দৈর্ঘ্য-ওজনে ছড়াবে।
4. word.s = slot শুরু, word.e = slot শেষ; সর্বনিম্ন দৈর্ঘ্য ০.০৬–০.০৭s; monotonic থাকবে।
5. cue.s/e অপরিবর্তিত (word সীমা cue সীমার ভেতরে)।

## আউটপুট schema (`/home/user/work/video_data.json` বা build dir)
```json
{
  "duration": 287.49,
  "cues": [ {"s": 0.09, "e": 2.69, "lines": ["লেখা"], "w": [["JWT-এর", 0.12, 0.68], ...] } , ...],
  "words": [ ["JWT-এর", 0.12, 0.68, 0], ... ]   // [text, s, e, cueIdx]
}
```

## টুল
`skills/tools/align_words.py` — এই পুরো অ্যালগরিদম implement করা আছে (ভেতরে docstring)।
চালানোর ধাপ: `/home/user/.venv/bin/python skills/tools/align_words.py <mp3> <srt> <video_data.json>`।

## কঠোর নিয়ম (M1/M2/M3)
- কোনো transform নিজের input-এ লিখবে না — align_words.py শুধু video_data.json লেখে, SRT ছোঁয় না।
- টাইম/লেখা কখনো মেমোরি থেকে বানাবে না — সবসময় ফাইল/অডিও থেকে।
- রিপোর্টে থাকবে: শব্দ সংখ্যা, word duration গড়, cue-start সরণ পরিসংখ্যান।
