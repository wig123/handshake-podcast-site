#!/usr/bin/env python3
"""校验 index.html 里每一条英文引语，并用 VTT 里匹配到的 cue 起始秒数回填时间戳。

规则（来自任务书）：
  * 英文引语必须是「官方 VTT 逐字稿把相邻 cue 用空格拼接后」的原样连续子串，
    不得改词、不得拼接不同位置的句子；
  * 时间戳 = 匹配到的那个 cue 的起始秒数；
  * 匹配不上的引语一律从页面里删掉。

用法：
  python3 tools/verify_quotes.py            # 回填时间戳 + 删除匹配不上的引语
  python3 tools/verify_quotes.py --check    # 只校验，不改文件；有失败则退出码 1
"""
import html
import re
import sys
import difflib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vtt import parse, secs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
YT = "https://www.youtube.com/watch?v=v5IJwVnTxzg&amp;t={}s"
QUOTE_RE = re.compile(
    r'<figure class="quote">\s*<blockquote>(.*?)</blockquote>\s*'
    r"<figcaption>.*?</figcaption>(.*?)</figure>",
    re.S,
)


def build(cues):
    """返回 (拼接文本, [(start,end,cue)])。cue 之间用一个空格拼接。"""
    parts, spans, pos = [], [], 0
    for c in cues:
        t = c["text"]
        parts.append(t)
        spans.append((pos, pos + len(t), c))
        pos += len(t) + 1
    return " ".join(parts), spans


def cue_at(spans, idx):
    for a, b, c in spans:
        if a <= idx < b:
            return c
    for a, b, c in spans:  # idx 落在 cue 之间的空格上
        if b <= idx:
            return c
    return spans[-1][2]


def stamp(ts):
    s = int(secs(ts))
    if s < 3600:
        return f"{s // 60}:{s % 60:02d}", s
    return f"{s // 3600}:{(s % 3600) // 60:02d}:{s % 60:02d}", s


def main():
    check_only = "--check" in sys.argv
    cues = parse(str(ROOT / "transcript.vtt"))
    joined, spans = build(cues)
    page = PAGE.read_text(encoding="utf-8")

    matched, missing = 0, []
    out, cursor = [], 0

    for m in QUOTE_RE.finditer(page):
        raw = m.group(1)
        quote = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", raw))).strip()
        idx = joined.find(quote)
        if idx < 0:
            missing.append(quote)
            if check_only:
                out.append(m.group(0))
                cursor = m.end()
                continue
            out.append(page[cursor:m.start()])  # 删掉整段引语
            cursor = m.end()
            continue
        cue = cue_at(spans, idx)
        label, seconds = stamp(cue["start"])
        block = (
            '<figure class="quote">\n'
            f"        <blockquote>{raw.strip()}</blockquote>\n"
            f'        <figcaption><a class="qts" href="{YT.format(seconds)}">{label}</a></figcaption>'
            f"{m.group(2).rstrip()}\n"
            "      </figure>"
        )
        out.append(page[cursor : m.start()])
        out.append(block)
        cursor = m.end()
        matched += 1

    out.append(page[cursor:])
    new_page = "".join(out)

    print(f"引语：匹配 {matched} 条，未匹配 {len(missing)} 条")
    for q in missing:
        near = difflib.get_close_matches(q[:120], [joined], n=1, cutoff=0.4)
        hint = ""
        if near:
            pos = joined.find(near[0][:60]) if near[0] in joined else -1
            if pos >= 0:
                hint = "（VTT 中有近似位置，需人工核对）"
        print(f"  ✗ {q[:100]}…{hint}")

    if not check_only:
        if new_page != page:
            PAGE.write_text(new_page, encoding="utf-8")
            print("已写回 index.html")
        else:
            print("index.html 无需改动")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
