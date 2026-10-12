#!/usr/bin/env python3
"""build_audio.py — chunk থেকে final mp3 + word-accurate SRT (skills/01, 03)

কাজ:
  1. প্রতিটা TTS chunk decode করে হুবহু দৈর্ঘ্য মাপে (chunk boundary = AUTHORITATIVE, M2)।
  2. back-to-back জোড়া দিয়ে 160kbps mono 44.1kHz mp3 encode করে (lameenc; ffmpeg নেই)।
  3. প্রতিটা chunk-এর ভেতরে তার sentence/cue গুলো VAD island + voiced-time proportion
     দিয়ে ভাগ করে — cue সীমা আসল অডিওর pause থেকে আসে (মেমোরি থেকে নয়, M3)।
     drift chunk-এর ভেতরেই সীমিত থাকে, chunk সীমা কখনো নড়ে না।
     ⚠️ হিসাব সবসময় chunk-relative coordinate-এ, শেষে absolute করা হয় (না হলে
        candidate filter ভুল করে — এই build-এ ধরা পড়া ভুল)।
  4. SRT লেখে (text == Script.txt, M10) — কখনো নিজের input-এ লেখে না (M1)।

Usage:
  build_audio.py <chunks.json> <chunks_dir> <out.mp3> <out.srt> [--report r.txt]

chunks.json schema: {"lines": ["cue1 লেখা", ...], "groups": [[startIdx, endIdx], ...]}
                    (0-based, end exclusive)
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from align_words import detect_islands  # একই VAD (skills/03) — নতুন করে বানাইনি (M3)

TARGET_SR = 44100
WRAP = 58     # SRT লাইন প্রতি সর্বোচ্চ অক্ষর
MIN_CUE = 0.30  # cue-র সর্বনিম্ন দৈর্ঘ্য (সেকেন্ড)
SNAP_TOL = 0.75  # pause-এ snap করার সর্বোচ্চ দূরত্ব


def decode(path):
    y, sr = sf.read(path, dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    if sr != TARGET_SR:
        n = int(round(len(y) * TARGET_SR / sr))
        y = np.interp(np.linspace(0, 1, n, endpoint=False),
                      np.linspace(0, 1, len(y), endpoint=False), y).astype("float32")
    return y


def silence_edges(y, sr, thr=0.01):
    """chunk-এর শুরু/শেষের নীরবতা মাপে (report-এর জন্য — কাটা হয় না)"""
    idx = np.where(np.abs(y) > thr)[0]
    if not len(idx):
        return len(y) / sr, len(y) / sr
    return idx[0] / sr, (len(y) - 1 - idx[-1]) / sr


def voiced_between(islands, x, y):
    return sum(max(0.0, min(b, y) - max(a, x)) for a, b in islands)


def split_cues(y, sr, n_sent, word_counts):
    """একটা chunk-কে n_sent cue-তে ভাগ করো → chunk-RELATIVE (start, end) list।

    পদ্ধতি: VAD island-এর gap/edge গুলোকে candidate split point ধরে, DP দিয়ে সেই
    কম্বিনেশন বেছে নেওয়া যায় যেখানে প্রতিটা sentence-এর ভেতরের **voiced সময়** তার
    শব্দসংখ্যার অনুপাতের সবচেয়ে কাছাকাছি। ফলে সীমা সবসময় আসল pause-তে বসে।
    """
    cdur = len(y) / sr
    islands = detect_islands(y, sr)
    if not islands or n_sent == 1:
        b = [cdur * i / n_sent for i in range(n_sent + 1)]
        return [(b[i], b[i + 1]) for i in range(n_sent)], cdur, islands

    first_s, last_e = islands[0][0], islands[-1][1]
    total_voiced = voiced_between(islands, 0.0, cdur) or cdur
    W = float(sum(word_counts)) or 1.0
    start = max(0.0, first_s - 0.09)

    # fast voiced-time query (10ms grid prefix sum) — DP ভেতরে বহুবার লাগে
    RES = 0.01
    nres = int(cdur / RES) + 3
    mask = np.zeros(nres, dtype=bool)
    for a, b in islands:
        i0 = max(0, int(a / RES))
        i1 = min(nres, max(i0 + 1, int(b / RES) + 1))
        mask[i0:i1] = True
    cumv = np.concatenate([[0.0], np.cumsum(mask * RES)])

    def vb(x, y):
        i = min(max(int(x / RES), 0), nres)
        j = min(max(int(y / RES) + 1, i), nres)
        return float(cumv[j] - cumv[i])

    # candidate: gap midpoint (penalty 0) + island edge (penalty 0.06)
    cands = []
    for i in range(len(islands) - 1):
        ga, gb = islands[i][1], islands[i + 1][0]
        cands.append(((ga + gb) / 2, 0.00))
        cands.append((islands[i][1], 0.06))
        cands.append((islands[i + 1][0], 0.06))
    cands = sorted({round(c, 3): p for c, p in cands if start + MIN_CUE < c < cdur - MIN_CUE}.items())
    cpts = [c for c, _ in cands]
    cpen = {c: p for c, p in cands}
    if n_sent - 1 > len(cpts):                      # যথেষ্ট pause না থাকলে সমান ভাগ
        b = [start + (cdur - start) * i / n_sent for i in range(n_sent + 1)]
        b[0], b[-1] = start, cdur
        return [(b[i], b[i + 1]) for i in range(n_sent)], cdur, islands

    # ---- DP: kটা সীমা বাছাই, প্রতিটা segment-এর voiced সময় target-এর কাছাকাছি ----
    INF = float("inf")
    tgt = [total_voiced * w / W for w in word_counts]
    prev = [start] * (n_sent - 1)
    dp = [[INF] * len(cpts) for _ in range(n_sent - 1)]
    back = [[-1] * len(cpts) for _ in range(n_sent - 1)]
    for j, c in enumerate(cpts):
        if c < start + MIN_CUE or c > cdur - MIN_CUE * (n_sent - 1):
            continue
        cost = abs(vb(start, c) - tgt[0]) + cpen[c]
        dp[0][j] = cost
    for k in range(1, n_sent - 1):
        lo = start
        for j, c in enumerate(cpts):
            if c < lo + MIN_CUE or c > cdur - MIN_CUE * (n_sent - 1 - k):
                continue
            best, bi = INF, -1
            for i, p in enumerate(cpts):
                if p >= c - MIN_CUE or dp[k - 1][i] == INF:
                    continue
                v = dp[k - 1][i] + abs(vb(p, c) - tgt[k]) + cpen[c]
                if v < best:
                    best, bi = v, i
            dp[k][j], back[k][j] = best, bi
    # শেষ segment (last bound -> cdur) যোগ করে সেরা শেষ পয়েন্ট
    bestj, bestv = -1, INF
    for j, c in enumerate(cpts):
        if dp[n_sent - 2][j] == INF or c > cdur - MIN_CUE:
            continue
        v = dp[n_sent - 2][j] + abs(vb(c, cdur) - tgt[n_sent - 1])
        if v < bestv:
            bestv, bestj = v, j
    if bestj < 0:                                   # DP ব্যর্থ → সমান ভাগ fallback
        b = [start + (cdur - start) * i / n_sent for i in range(n_sent + 1)]
        b[0], b[-1] = start, cdur
        return [(b[i], b[i + 1]) for i in range(n_sent)], cdur, islands
    picks = [cpts[bestj]]
    j = bestj
    for k in range(n_sent - 2, -1, -1):
        j = back[k][j]
        if j < 0:
            break
        picks.append(cpts[j])
    bounds = [start] + list(reversed(picks)) + [cdur]
    if len(bounds) != n_sent + 1:                   # safety
        b = [start + (cdur - start) * i / n_sent for i in range(n_sent + 1)]
        b[0], b[-1] = start, cdur
        return [(b[i], b[i + 1]) for i in range(n_sent)], cdur, islands
    for i in range(1, len(bounds)):
        bounds[i] = max(bounds[i], bounds[i - 1] + MIN_CUE)
    for i in range(len(bounds) - 2, -1, -1):
        bounds[i] = min(bounds[i], bounds[i + 1] - MIN_CUE)
    bounds[0], bounds[-1] = max(bounds[0], 0.0), cdur
    return [(bounds[i], bounds[i + 1]) for i in range(n_sent)], cdur, islands


def fmt_srt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap(text):
    if len(text) <= WRAP:
        return [text]
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > WRAP:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    if len(lines) <= 2:
        return lines
    h = (len(lines) + 1) // 2
    return [" ".join(lines[:h]), " ".join(lines[h:])]


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    cdir, out_mp3, out_srt = sys.argv[2], sys.argv[3], sys.argv[4]
    lines, groups = spec["lines"], spec["groups"]
    ys, report = [], [f"chunks: {len(groups)}  cues: {len(lines)}"]

    for i, (a, b) in enumerate(groups):
        y = decode(os.path.join(cdir, f"c{i + 1:02d}.mp3"))
        ys.append(y)
        lead, trail = silence_edges(y, TARGET_SR)
        report.append(f"  c{i + 1:02d} cues {a + 1:>2}-{b:<2} {len(y) / TARGET_SR:6.3f}s "
                      f"| silence lead {lead:.2f}s trail {trail:.2f}s")

    audio = np.concatenate(ys)
    dur = len(audio) / TARGET_SR
    report.append(f"concat total: {dur:.3f}s = {int(dur) // 60}:{int(dur) % 60:02d} "
                  f"| {len(' '.join(lines).split())} words -> {len(' '.join(lines).split()) / dur:.2f} w/s")

    import lameenc
    peak = float(np.abs(audio).max()) or 1.0
    if peak > 0.99:
        audio = audio * (0.99 / peak)
        report.append(f"normalized: peak was {peak:.3f}")
    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
    enc = lameenc.Encoder()
    enc.set_bit_rate(160)
    enc.set_in_sample_rate(TARGET_SR)
    enc.set_channels(1)
    enc.set_quality(2)
    data = enc.encode(pcm) + enc.flush()
    open(out_mp3, "wb").write(data)
    report.append(f"mp3: {out_mp3} ({len(data) / 1024:.0f} KB, 160kbps mono 44.1kHz)")

    blocks, off = [], 0.0
    for i, (a, b) in enumerate(groups):
        wc = [len(x.split()) for x in lines[a:b]]
        spans, cdur, isl = split_cues(ys[i], TARGET_SR, b - a, wc)
        report.append("  c%02d islands=%d cue-ends(abs): %s" %
                      (i + 1, len(isl), " ".join(f"{off + e:.2f}" for s, e in spans[:-1])))
        for j, (s, e) in enumerate(spans):
            blocks.append((len(blocks) + 1, off + s, off + e, lines[a + j]))
        off += cdur

    out = []
    for n, s, e, txt in blocks:
        out.append(f"{n}\n{fmt_srt(s)} --> {fmt_srt(e)}\n" + "\n".join(wrap(txt)))
        out.append("")
    open(out_srt, "w", encoding="utf-8").write("\n".join(out).rstrip() + "\n")

    durs = [e - s for _, s, e, _ in blocks]
    wps = [len(t.split()) / d for (_, _, _, t), d in zip(blocks, durs)]
    report.append(f"srt: {out_srt} ({len(blocks)} cues)")
    report.append(f"cue dur: mean={np.mean(durs):.2f}s min={min(durs):.2f}s max={max(durs):.2f}s")
    report.append(f"cue w/s: mean={np.mean(wps):.2f} min={min(wps):.2f} max={max(wps):.2f}")
    # segment timings (hook 1-2, news 3-39, outro 40-42)
    seg = {"hook(1-2)": blocks[1][2] - blocks[0][1],
           "news(3-39)": blocks[38][2] - blocks[2][1],
           "outro(40-42)": blocks[41][2] - blocks[39][1]}
    for k, v in seg.items():
        report.append(f"  {k}: {v:.1f}s = {int(v) // 60}:{int(v) % 60:02d}")
    txt = "\n".join(report)
    print(txt)
    if "--report" in sys.argv:
        open(sys.argv[sys.argv.index("--report") + 1], "w", encoding="utf-8").write(txt + "\n")


if __name__ == "__main__":
    main()
