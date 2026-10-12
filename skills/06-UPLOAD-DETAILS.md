# 06 — UPLOAD DETAILS: YouTube + Facebook metadata

## ফাইল
`output/{topic}UploadDetails.txt` — নিচের গঠনে (উদাহরণ: `output/JWTUploadDetails.txt`)।

## YouTube
- **৩টা title option** (বাংলা + English tech term; একটাতে প্রশ্ন, একটাতে scope, একটাতে টান/hook)।
- **Description ≈ ২০০০ শব্দ** (১৯০০–২১০০):
  - সূচনা hook → বিষয় পরিচিতি → ভিডিওতে যা যা (bullet list, **timestamp একদম নয়**) →
    গভীর ব্যাখ্যা/প্রয়োগ → সাধারণ ভুল → কাদের জন্য → প্রশ্নোত্তর → CTA (like/subscribe/comment) → শুভেচ্ছা।
  - বাংলা ভাষা, English tech term অপরিবর্তিত; শেষে ২-৪টা hashtag।
- **Tags: ৪০+** (কমা দিয়ে; ইংরেজি+বাংলা মিশ্রিত: topic, বিষয়শব্দ, synonym, সম্পর্কিত প্রযুক্তি)।

## Facebook
- **১টা title** (সরল, আকর্ষণীয়)।
- **১০টা hashtag** (সবচেয়ে জনপ্রিয় আগে)।
- **১০টা tag** (কমা দিয়ে keyword)।

## গঠন (format)
```
════... UPLOAD DETAILS — {topic} ...
【 TITLE OPTIONS (3) 】 1. ... 2. ... 3. ...
【 DESCRIPTION 】 ≈2000 শব্দ (timestamp নেই)
【 TAGS 】 40+ tags
──────────── FACEBOOK ────────────
【 TITLE 】 ...
【 HASHTAGS (10) 】 ...
【 TAGS (10) 】 ...
```

## যাচাই
description শব্দসংখ্যা ১৯০০+; "timestamp" ধরনের `0:00`/`০:০০` নেই; tags ৪০+; hashtag ১০;
সব লেখায় topic-এর মূল keyword আছে। `validate_output.py` সংখ্যা যাচাই করে।
