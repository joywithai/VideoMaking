#!/usr/bin/env python3
"""align_words.py — word-level timing via cue-anchored VAD island allocation.

Algorithm (skills/03-AUDIO-ALIGN.md — this file is the reference implementation):
  1. VAD: RMS win=25ms hop=10ms; thr = max(0.004, p82*0.16); smooth 3 frames;
     islands = voiced runs, merge gap <= 50ms, drop < 0.12s.
  2. Cue times are AUTHORITATIVE (TTS chunk boundaries). Never rewritten (M2).
  3. Each cue's words are hard-assigned, monotonic, to islands spanning the cue
     (island score = covered word ratio, then duration); words within one island
     are laid out inside it proportional to their length, expanded with
     post-blend gap padding; islands never merged across separate islands.
  4. word bounds clamped to [cue.s, cue.e]; min duration 0.07s; monotonic
     e >= s + 0.01 within a cue; cue bounds preserved exactly.

Usage: align_words.py <mp3> <srt> <out_video_data.json> [--report report.txt]

Writes ONLY the output JSON (never its inputs — M1).
"""
import json
import math
import re
import sys

import numpy as np
import soundfile as sf


def load_cues(path):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n").strip()
    cues = []
    for b in raw.split("\n\n"):
        lines = b.split("\n")
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1])
        t = lambda h, mi, s, ms: int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000
        s, e = t(*m.groups()[:4]), t(*m.groups()[4:])
        txt = "\n".join(l for l in lines[2:] if l.strip())
        cues.append({"s": s, "e": e, "lines": txt.split("\n")})
    return cues


def load_audio(path):
    y, sr = sf.read(path, dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    return y, sr


def detect_islands(y, sr):
    win = int(0.025 * sr)
    hop = int(0.010 * sr)
    if len(y) < win:
        return []
    n = 1 + (len(y) - win) // hop
    rms = np.sqrt(np.sum(np.lib.stride_tricks.sliding_window_view(y, win)[::hop] ** 2, axis=1) / win)[:n]
    thr = max(0.004, float(np.percentile(rms, 82)) * 0.16)
    sm = np.convolve(rms, np.ones(3) / 3, mode="same")
    mask = sm > thr
    islands = []
    i = 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j + 1 < len(mask) and mask[j + 1]:
                j += 1
            islands.append([i * hop, (j * hop) + win])
            i = j + 1
        else:
            i += 1
    merged = []
    for a, b in islands:
        if merged and a - merged[-1][1] <= 0.05:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [[a / sr, b / sr] for a, b in merged if b - a >= 0.12]


def gen_words(cues, islands):
    flat = []  # (text, cueIdx, wIdxInCue)
    for ci, c in enumerate(cues):
        for line in c["lines"]:
            for tok in line.split():
                flat.append((tok, ci))
    total = len(flat)
    W = [None] * total
    k = 0
    for ci, c in enumerate(cues):
        ws = [w for w in flat if w[1] == ci]
        n = len(ws)
        if n == 0:
            continue
        s0, e0 = c["s"], c["e"]
        span = max(0.2, e0 - s0)
        cand = [isl for isl in islands if isl[1] > s0 + 0.01 and isl[0] < e0 - 0.01]
        if not cand:
            mid = (s0 + e0) / 2
            cand = [x for x in islands if x[0] <= mid <= x[1]] or [[s0, e0]]
        # assignment: each island takes words proportional to overlap, ordered
        slots = []
        # island weights
        wts = []
        for a, b in cand:
            ov = max(0.0, min(b, e0) - max(a, s0))
            wts.append(ov if ov > 0 else 0.02 * span)
        tot = sum(wts) or 1.0
        start_idx = 0
        for li, ((a, b), wt) in enumerate(zip(cand, wts)):
            take = int(round(n * wt / tot))
            if li == len(cand) - 1:
                take = n - start_idx
            take = max(0, min(take, n - start_idx))
            if take == 0 and li != len(cand) - 1:
                continue
            if li == len(cand) - 1 and start_idx < n:
                take = n - start_idx
            words_i = list(range(start_idx, start_idx + take))
            start_idx += take
            if not words_i:
                continue
            ia, ib = max(a, s0), min(b, e0)
            # post-blend gap padding (70ms before / 100ms after within island)
            ia, ib = ia + 0.07, ib - 0.10
            if ib <= ia:
                ia, ib = max(a, s0), min(b, e0)
            ls = [len(ws[i][0]) for i in words_i]
            tsum = sum(ls) or len(ls)
            cur = ia
            avail = max(0.05, ib - ia)
            for idx, l in zip(words_i, ls):
                d = avail * (l / tsum)
                slots.append((idx, cur, cur + d, ia, ib))
                cur += d
        # leftover words (take rounding) — append last slot extension
        if start_idx < n:
            for idx in range(start_idx, n):
                slots.append((idx, s0 + (e0 - s0) * idx / n, s0 + (e0 - s0) * (idx + 1) / n, s0, e0))
        slots.sort()
        prev_e = s0
        for idx, s, e, ia, ib in slots:
            s = min(max(s, s0), e0 - 0.02)
            if s < prev_e:
                s = prev_e
            e = min(max(e, s + 0.07), e0)
            if e <= s:
                s = max(s0, e - 0.07)
            prev_e = e
            W[k + idx] = (ws[idx][0], s, e)
        k += n
    out = []
    for ci, c in enumerate(cues):
        arr = []
        for i in range(len([w for w in flat if w[1] == ci])):
            gi = sum(len([w for w in flat if w[1] == j]) for j in range(ci)) + i
            if W[gi] is not None:
                arr.append(list(W[gi]))
        c["w"] = arr
        out.append(c)
    words = [[w[0], w[1], w[2], ci] for ci, c in enumerate(out) for w in c["w"]]
    return out, words


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    mp3, srt, outp = sys.argv[1:4]
    cues = load_cues(srt)
    y, sr = load_audio(mp3)
    dur = len(y) / sr
    islands = detect_islands(y, sr)
    cues2, words = gen_words(cues, islands)
    data = {"duration": round(dur, 2), "cues": cues2, "words": words}
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    # report
    shifts = []
    for c in cues2:
        if c["w"]:
            shifts.append(c["w"][0][1] - c["s"])
    rep = [
        f"duration={dur:.2f}s  cues={len(cues2)}  words={len(words)}  islands={len(islands)}",
        f"word dur avg={np.mean([w[2]-w[1] for w in words]):.3f}s min={min(w[2]-w[1] for w in words):.3f}s",
        f"cue-start shift mean={np.mean(shifts):.3f}s max={max(abs(s) for s in shifts):.3f}s",
    ]
    txt = "\n".join(rep)
    if len(sys.argv) > 4:
        open(sys.argv[4], "w", encoding="utf-8").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
