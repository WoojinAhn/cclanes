#!/usr/bin/env python3
"""lately — per-repo 'what was I working on' CLI tool."""

import argparse
import json
import sys
from pathlib import Path

HOME_DIR = Path.home() / "home"
CONFIG_PATH = Path.home() / ".lately" / "config.json"


def load_config(path: Path = CONFIG_PATH) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"exclude": []}


def save_config(cfg: dict, path: Path = CONFIG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


def add_excludes(cfg: dict, repos: list[str]) -> dict:
    current = set(cfg["exclude"])
    current.update(repos)
    cfg["exclude"] = sorted(current)
    return cfg


def remove_excludes(cfg: dict, repos: list[str]) -> dict:
    cfg["exclude"] = [r for r in cfg["exclude"] if r not in repos]
    return cfg


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="lately",
        description="Per-repo 'what was I working on' summaries.",
    )
    parser.add_argument("--days", type=int, default=None,
                        help="Only show repos with activity in the last N days")
    parser.add_argument("--raw", action="store_true",
                        help="No LLM summary — raw data only (fast/offline)")
    parser.add_argument("--memo", nargs=2, metavar=("REPO", "MESSAGE"),
                        help="Save a manual memo to a repo's .lately file")
    parser.add_argument("--exclude", type=str,
                        help="Permanently exclude repos (comma-separated)")
    parser.add_argument("--include", type=str,
                        help="Remove repos from permanent exclusion (comma-separated)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    # --exclude: add to config and exit
    if args.exclude:
        repos = [r.strip() for r in args.exclude.split(",")]
        cfg = load_config()
        cfg = add_excludes(cfg, repos)
        save_config(cfg)
        print(f"제외 목록에 추가됨: {', '.join(repos)}")
        return

    # --include: remove from config and exit
    if args.include:
        repos = [r.strip() for r in args.include.split(",")]
        cfg = load_config()
        cfg = remove_excludes(cfg, repos)
        save_config(cfg)
        print(f"제외 목록에서 제거됨: {', '.join(repos)}")
        return

    # --memo: write memo file and exit
    if args.memo:
        repo_name, message = args.memo
        memo_path = HOME_DIR / repo_name / ".lately"
        if not (HOME_DIR / repo_name).is_dir():
            print(f"오류: ~/home/{repo_name} 디렉토리가 없습니다.", file=sys.stderr)
            sys.exit(1)
        memo_path.write_text(message + "\n")
        print(f"메모 저장됨: ~/home/{repo_name}/.lately")
        return

    # Default: scan and display (placeholder)
    print("(scan not implemented yet)")


if __name__ == "__main__":
    main()
