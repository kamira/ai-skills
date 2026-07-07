#!/usr/bin/env python3
"""PreToolUse hook(Edit/Write)— 受治理 repo 的「先 CHG 再動手」閘。
warn(預設)=systemMessage 提示;block=deny;off=靜默。內部錯誤一律放行(exit 0)。"""
import json
import os
import re
import sys
from pathlib import Path

ACTIVE_HINTS = ("實作中", "草稿", "draft", "進行中", "in progress", "待驗收", "pending acceptance")
SKIP_PARTS = ("/docs/", "/.claude/", "/scratchpad/", "/tmp/", "/.git/", "/worklog/")


def ledger_dirs(root: Path):
    dirs = [root / "docs" / "changes"]
    docs = root / "docs"
    if docs.is_dir():
        dirs += [d / "changes" for d in docs.iterdir() if d.is_dir() and (d / "changes").is_dir()]
    return [d for d in dirs if d.is_dir()]


def has_active_chg(ledgers) -> bool:
    for d in ledgers:
        for f in d.glob("CHG-*.md"):
            text = f.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^##\s*(狀態|Status)\b(.*)\Z", text, re.MULTILINE | re.DOTALL)
            scope = (m.group(2) if m else text).lower()
            if any(h in scope for h in ACTIVE_HINTS):
                return True
    return False


def main() -> int:
    try:
        mode = os.environ.get("AI_SDLC_HOOK_MODE", "warn")
        if mode == "off":
            return 0
        data = json.load(sys.stdin)
        root = Path(data.get("cwd") or ".").resolve()
        fp = str(data.get("tool_input", {}).get("file_path", ""))
        if not fp or fp.endswith(".md") or any(p in fp for p in SKIP_PARTS):
            return 0  # 治理文件/暫存/文件類編修放行(開 CHG 本身要能寫)
        ledgers = ledger_dirs(root)
        if not ledgers:
            return 0  # 非受治理 repo
        if has_active_chg(ledgers):
            return 0
        msg = ("[ai-sdlc] 此程式編修沒有進行中的 CHG 對應——依 modification-guide,任何修改先開 CHG 再動手"
               "(AI_SDLC_HOOK_MODE=off 可關閉;=block 可改為硬擋)")
        if mode == "block":
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "deny",
                "permissionDecisionReason": msg}}, ensure_ascii=False))
        else:
            print(json.dumps({"systemMessage": msg}, ensure_ascii=False))
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
