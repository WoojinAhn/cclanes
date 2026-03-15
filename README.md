🇰🇷 [한국어](README.ko.md)

# lately

> "What was I working on?" — A per-repo work summary CLI for parallel vibe coding.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![No Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](https://docs.python.org/3/library/)

Scan all your local repos, collect git activity + Claude Code session history + manual memos, and get a sorted summary table — powered by LLM one-liners via `claude` CLI.

## Demo

```
$ lately
📋 캐시 19개 / 새 분석 2개
레포                          마지막 활동        요약
──────────────────────────  ────────────  ────────────────────────────────────────
dev-dashboard               방금            lately CLI 구현 완료
kr-whisky-tracker           11일 전         위스키 정렬 기능 구현
GoPeaceTrain                10시간 전        한탄호텔 예약 모니터링 시작
```

## Features

- 🔍 **Auto-scan** — Discovers all repos under `~/home/*` automatically
- 🤖 **LLM summaries** — One-line work summaries via Claude Haiku, no API key needed (uses `claude` CLI)
- ⚡ **Smart caching** — Only re-analyzes repos that changed since last run
- 📝 **Manual memos** — Attach short notes to any repo (auto-expire after 15 min)
- 🚫 **Exclude/Include** — Permanently hide irrelevant repos from output
- 📊 **Raw mode** — Skip LLM, show raw git + session data directly
- 📦 **Zero dependencies** — Python 3.10+ stdlib only

## Quick Start

### Prerequisites

- Python 3.10+
- [`claude` CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated (for LLM summaries)
- Git repos under `~/home/`

### Installation

```bash
# Clone
git clone https://github.com/WoojinAhn/dev-dashboard.git
cd dev-dashboard

# Run directly
python lately.py

# Or add an alias
echo 'alias lately="python ~/home/dev-dashboard/lately.py"' >> ~/.zshrc
```

### Usage

```bash
lately                          # Full scan with LLM summaries
lately --raw                    # No LLM, raw git + session data
lately --days 7                 # Only repos active in last 7 days
lately --memo <repo> "message"  # Save manual memo
lately --exclude repo1,repo2    # Permanently exclude repos
lately --include repo1          # Remove from exclusion
```

## Configuration

### `~/.lately/config.json`

```json
{
  "exclude": ["docs", "archive"]
}
```

### `.lately` memo files

Drop a `.lately` file in any repo to attach a manual note:

```bash
lately --memo my-repo "Waiting for API review"
```

Memos are valid when written within 15 minutes of the last git commit or Claude session activity. Stale memos are ignored (not deleted) and the LLM summary is used instead.

## How It Works

```
~/home/* repos
     │
     ├── git log / status ──────┐
     ├── Claude Code sessions ──┤──→ Cache (skip unchanged) ──→ Claude Haiku ──→ Summary Table
     └── .lately memos ─────────┘
```

1. **Scan** — Walk `~/home/` subdirectories, identify git repos
2. **Collect** — Gather git log, uncommitted changes, Claude Code session history, manual memos
3. **Cache** — Compare repo state hash with cached version; skip unchanged repos
4. **Summarize** — Send changed repo data to Claude Haiku for one-line summary
5. **Display** — Sort by last activity, render as a clean terminal table

## Tech Stack

| Component | Choice |
|---|---|
| Language | Python 3.10+ (stdlib only) |
| LLM | Claude Haiku via `claude` CLI |
| Data sources | git, Claude Code sessions, manual memos |
| Storage | JSON file cache (`~/.lately/cache.json`) |

## License

[MIT](LICENSE)
