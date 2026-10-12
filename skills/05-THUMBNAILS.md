# 05 — THUMBNAILS: ৩টা ক্লিক-টানা থাম্বনেইল

## স্টাইল (ইউজার reference — কঠোর)
- ১২৮০×৭২০, ডার্ক ব্যাকগ্রাউন্ড, **subject বামে**, **ডানে ২-লাইন bold লেখা**
  (লাইন ১ সাদা, লাইন ২ কমলা `#FF7A1A`), high contrast, সরল/পরিচ্ছন্ন।
- লেখা: Hind Siliguri Bold (google/fonts থেকে `HindSiliguri-Bold.ttf` নামাও —
  `api.github.com/repos/google/fonts/contents/ofl/hindsiliguri/HindSiliguri-Bold.ttf`,
  Accept: `application/vnd.github.raw+json`)।
- লেখা কখনো clip হবে না / কিনারা ছোঁয়াবে না — auto-fit (চওড়া মাপিয়ে font size কমাও),
  stroke+shadow দিও।

## উপাদান
1. **BG:** `materials/BG.jpg` → cover-crop, ঘুরিয়ে ধোঁয়াটে করো (brightness ≈0.36)।
2. **Subject (বামে):** videoDetails/src থেকে ছবি থাকলে সেটা; না থাকলে AI-generate
   (ডার্ক ব্যাকগ্রাউন্ড, কমলা rim light, **কোনো লেখা/অক্ষর নয়**, glass/neon tech object)।
   rounded/feather mask + কমলা glow দিয়ে বসাও (~৫০০px, বামে)।
3. **লেখা (ডানে):** প্রতিটা থাম্বনেইলে আলাদা hook (৩টা variation) —
   বাংলা bold, লাইন ১ প্রশ্ন/কল, লাইন ২ topic keyword।

## ৩টা hook প্যাটার্ন (প্রতিটা ভিডিওর জন্য নতুন করে, এই ঢঙে)
1. প্রশ্ন/উদ্দীপনা: "X কীভাবে কাজ করে?" / "Header · Payload · Signature"
2. আহ্বান: "নিজেই বুঝে ফেলো!" / "সহজ ভাষায় X"
3. সত্য-ফাঁক: "decode ≠ verify!" / "X-এর গোপন সত্য!"

## ফাইল
`output/{topic}Thumbnail_1.png`, `_2.png`, `_3.png` (PNG, ১২৮০×৭২০)।
`skills/tools/make_thumbnails.py` এই সব ধাপ automate করে (subject art পাথ + লেখা দাও)।

## যাচাই
আয়তন ১২৮০×৭২০; লেখা পরিষ্কার পড়া যায় (স্ক্রিনে নিজে দেখবে); কোনো লেখা বাইরে/ছেঁড়া নয়;
৩টা আলাদা হুক।
