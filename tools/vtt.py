#!/usr/bin/env python3
"""Helpers to parse the official VTT transcript."""
import re
import sys


def parse(path="transcript.vtt"):
    raw = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n\s*\n", raw.strip())
    cues = []
    for b in blocks:
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        if not lines:
            continue
        ti = None
        for i, l in enumerate(lines):
            if "-->" in l:
                ti = i
                break
        if ti is None:
            continue
        start, end = [t.strip() for t in lines[ti].split("-->")]
        text = " ".join(lines[ti + 1 :]).strip()
        if not text:
            continue
        cues.append({"start": start, "end": end, "text": text})
    return cues


def secs(ts):
    ts = ts.replace(",", ".")
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


if __name__ == "__main__":
    cues = parse()
    if sys.argv[1] == "dump":
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        for c in cues:
            s = secs(c["start"])
            if lo <= s < hi:
                print(f"[{c['start'][:8]}] {c['text']}")
    elif sys.argv[1] == "count":
        print(len(cues))
    elif sys.argv[1] == "joined":
        print(" ".join(c["text"] for c in cues))
