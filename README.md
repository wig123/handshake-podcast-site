# Handshake 数据深潜 · 中文笔记站

Latent Space 播客《What Frontier Labs Buy: A Data Deep Dive with Handshake AI — Garrett Lord & Team》(2026-11-09,164 分钟)的中文手机端静态笔记页。

纯静态:一个 `index.html` + `styles.css` + `app.js`,没有构建步骤,没有外部依赖,深浅色自适应,33 段原文时间戳可点击跳 YouTube。

## 内容

- 按原文 33 个时间戳分段的要点(金融段 Project Falcon / existing goodwill 错误 / Excel grader 被 reward hack;生物段 VIALS 凝胶条带与脑组织切片;对齐段的文件服务器任务、CAREBench、公平信贷红线;企业私有基准、holdout、招聘)。
- 30 条精选英文原话 + 中文翻译。每条都经脚本校验,必须是官方 ASR 逐字稿(相邻 cue 用空格拼接后)的原样连续子串,时间戳取匹配到的那条 cue 的起始秒数。
- 最后一节「对 Agent 评测的启发」。

## 校验引语

```bash
# 先取官方 VTT(约 209KB,974 条 cue)
curl -A "Mozilla/5.0 ... Chrome/131.0.0.0 Safari/537.36" \
     -H "Referer: https://www.latent.space/" \
     -o transcript.vtt \
     "https://rss.beehiiv.com/podcasts/transcriptions/01a1c104-0c36-7bb0-9cd9-d552c4d789a7.vtt"

python3 tools/verify_quotes.py          # 回填时间戳,删除匹配不上的引语
python3 tools/verify_quotes.py --check  # 只校验(有失配则退出码 1)
```

- `tools/vtt.py` 解析 VTT。
- `tools/verify_quotes.py` 会把 `index.html` 里每个 `figure.quote` 的 `<blockquote>` 文本和拼接后的逐字稿做子串匹配,命中就写入该 cue 的起始时间,并通过同一个脚本可重复执行(幂等)。

## 声明

英文摘录来自官方 ASR 逐字稿,没有说话人标签,可能存在识别误差。中文内容是对字幕的转述与要点整理,不是逐句翻译。本页与 Latent Space、Handshake 无关,仅供学习参考。
