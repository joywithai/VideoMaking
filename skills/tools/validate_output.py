#!/usr/bin/env python3
"""validate_output.py — self-check for a build's output/ package.

Usage: validate_output.py <topic> [output_dir]
Checks (skills/04 + 06 + 02 rules):
  files exist, SRT text == Script text (M10), word counts, beat cue-ranges,
  data-w bounds + trigger times inside beat cue span, kinetic word order,
  uploadDetails sizes. Prints PASS/FAIL list; exit 1 on any FAIL.

Also: `validate_output.py --css file.html` scans CSS selectors for the
M4 hex-escape pitfall (\\[0-9a-fA-F] inside selectors).
"""
import json
import os
import re
import sys


def fail(msg, F):
    F.append("FAIL " + msg)


def ok(msg, F):
    F.append("ok   " + msg)


def srt_words(path):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n").strip()
    words = []
    for b in raw.split("\n\n"):
        lines = b.split("\n")
        words += " ".join(lines[2:]).split()
    return words


def script_words(path):
    return open(path, encoding="utf-8").read().split()


def check_css(path, F):
    html = open(path, encoding="utf-8").read()
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    css = m.group(1) if m else ""
    for sel in re.findall(r"([^{]+)\{", css):
        if re.search(r"\\[0-9a-fA-F]", sel):
            fail(f"M4: hex-escape in selector: {sel.strip()[:40]!r}", F)
    if "healCards" not in html and "gbox" in html:
        fail("self-heal JS (healCards) missing", F)
    else:
        ok("CSS selectors + healCards present", F)


def check(topic, outdir):
    F = []
    need = [f"{topic}Audio.mp3", f"{topic}Audio.srt", f"{topic}Script.txt", f"{topic}Video.html",
            f"{topic}UploadDetails.txt"] + [f"{topic}Thumbnail_{i}.png" for i in (1, 2, 3)]
    for f in need:
        p = os.path.join(outdir, f)
        if not os.path.exists(p):
            fail(f"missing {f}", F)
        else:
            ok(f"exists {f}", F)
    srt_p = os.path.join(outdir, f"{topic}Audio.srt")
    scr_p = os.path.join(outdir, f"{topic}Script.txt")
    if os.path.exists(srt_p) and os.path.exists(scr_p):
        sw, cw = srt_words(srt_p), script_words(scr_p)
        if sw == cw:
            ok(f"SRT text == Script text ({len(sw)} words)", F)
        else:
            fail(f"SRT words ({len(sw)}) != Script words ({len(cw)}) — M10", F)
    vid_p = os.path.join(outdir, f"{topic}Video.html")
    if os.path.exists(vid_p):
        html = open(vid_p, encoding="utf-8").read()
        m = re.search(r"const DATA = (\{.*?\});\n", html, re.S)
        if not m:
            fail("DATA json not found in Video.html", F)
            return F
        data = json.loads(m.group(1))
        words = data["words"]
        beats = re.findall(r"c0\s*:\s*(\d+)\s*,\s*c1\s*:\s*(\d+)", html)
        if not beats:
            fail("no BEATS found", F)
            return F
        covered = []
        for a, b in beats:
            covered += list(range(int(a), int(b) + 1))
        if sorted(covered) == list(range(len(data["cues"]))):
            ok(f"{len(beats)} beats cover {len(data['cues'])} cues exactly once", F)
        else:
            fail(f"beat cue-ranges do not tile cues (covered {len(set(covered))}/{len(data['cues'])})", F)
        body = html
        bad = 0
        for mw in re.finditer(r'data-w="(\d+)"', body):
            w = int(mw.group(1))
            if w >= len(words):
                bad += 1
        if bad:
            fail(f"{bad} data-w out of range", F)
        else:
            ok(f"all data-w < {len(words)}", F)
        # trigger inside beat cue span
        trig_bad = 0
        beat_spans = [(int(a), int(b)) for a, b in beats]
        for mw in re.finditer(r'data-w="(\d+)"[^>]*', body):
            w = int(mw.group(1))
            if w < len(words):
                t = words[w][1] - 0.12
                ci = words[w][3]
                if not any(a <= ci <= b for a, b in beat_spans):
                    trig_bad += 1
        if trig_bad:
            fail(f"{trig_bad} word triggers outside their beat cue span", F)
        else:
            ok("all word triggers inside beat cue spans", F)
        # kinetic order
        kin = re.search(r'class="el kw[^"]*"[^>]*data-w="(\d+)"', body)
        kin_ws = [int(x) for x in re.findall(r'class="el kw[^"]*"[^>]*data-w="(\d+)"', body)]
        if kin_ws == sorted(kin_ws):
            ok(f"kinetic order monotonic ({len(kin_ws)} spans)", F)
        elif kin_ws:
            fail("kinetic spans not in word order", F)
        check_css(vid_p, F)
    up_p = os.path.join(outdir, f"{topic}UploadDetails.txt")
    if os.path.exists(up_p):
        t = open(up_p, encoding="utf-8").read()
        if "DESCRIPTION" in t:
            desc = t.split("【 DESCRIPTION 】")[1].split("【 TAGS 】")[0]
            n = len(desc.split())
            if n >= 1500:
                ok(f"description words = {n}", F)
            else:
                fail(f"description too short: {n} words", F)
        tags_m = re.search(r"【 TAGS 】(.+?)\n\n", t, re.S)
        if tags_m:
            ntags = len([x for x in tags_m.group(1).split(",") if x.strip()])
            if ntags >= 40:
                ok(f"tags = {ntags}", F)
            else:
                fail(f"tags < 40: {ntags}", F)
    return F


if __name__ == "__main__":
    if sys.argv[1] == "--css":
        F = []
        check_css(sys.argv[2], F)
        print("\n".join(F))
        sys.exit(1 if any(x.startswith("FAIL") for x in F) else 0)
    topic = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "output"
    F = check(topic, outdir)
    print("\n".join(F))
    print("RESULT:", "PASS ✅" if not any(x.startswith("FAIL") for x in F) else "FAIL ❌")
    sys.exit(1 if any(x.startswith("FAIL") for x in F) else 0)
