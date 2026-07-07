#!/usr/bin/env python3
"""SessionStart hook — 受治理 repo 的進場握手提醒(warn/block 皆只提示;off 靜默;錯誤一律放行)。"""
import json
import os
import re
import sys
from pathlib import Path

ACCEPTED = ("已驗收", "accepted")
PAUSED = ("暫停", "paused")


def ledger_dirs(root: Path):
    dirs = [root / "docs" / "changes"]
    docs = root / "docs"
    if docs.is_dir():
        dirs += [d / "changes" for d in docs.iterdir() if d.is_dir() and (d / "changes").is_dir()]
    return [d for d in dirs if d.is_dir()]


def main() -> int:
    try:
        if os.environ.get("AI_SDLC_HOOK_MODE", "warn") == "off":
            return 0
        data = json.load(sys.stdin)
        root = Path(data.get("cwd") or ".").resolve()
        ledgers = ledger_dirs(root)
        if not ledgers:
            return 0  # 非受治理 repo,不打擾
        pending = []
        for d in ledgers:
            for f in sorted(d.glob("CHG-*.md")):
                text = f.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r"^##\s*(狀態|Status)\b(.*)\Z", text, re.MULTILINE | re.DOTALL)
                scope = (m.group(2) if m else text).lower()
                if not any(h in scope for h in ACCEPTED) and not any(h in scope for h in PAUSED):
                    pending.append(f.stem)
        ctx = ("[ai-sdlc] 本 repo 受治理:動手前先跑進場握手(AGENTS.md → Guideline → knowledge INDEX → 未收尾 CHG → git status 對帳);"
               "任何修改先開 CHG、同輪 ACC 收尾。")
        ctx += f" 未收尾 CHG:{', '.join(pending[:5])}——先收尾再開新需求。" if pending else " 未收尾 CHG:無。"
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx}},
                         ensure_ascii=False))
        return 0
    except Exception:
        return 0  # 治理工具不可成為故障點


if __name__ == "__main__":
    sys.exit(main())
