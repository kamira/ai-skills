#!/usr/bin/env python3
"""Stop hook — 懸空驗收攔截:CHG 已實作卻無 ACC 時,block 模式攔一次要求同輪收尾。
stop_hook_active=true 直接放行(防迴圈);warn=提示;off=靜默;錯誤一律放行。"""
import json
import os
import re
import sys
from pathlib import Path

IMPLEMENTED = ("已實作", "implemented", "待驗收", "pending acceptance")
EXEMPT = ("已驗收", "accepted", "暫停", "paused")
SELF_ACC = re.compile(r"自驗|self-?verified", re.IGNORECASE)
LOW_RISK = re.compile(r"(風險分級|Risk)\s*[::]\s*[^\n]{0,40}?(低|low)", re.IGNORECASE)
CHG_ID = re.compile(r"CHG-\d{8}-\d+")


def ledger_pairs(root: Path):
    docs = root / "docs"
    pairs = [(root / "docs" / "changes", root / "docs" / "acceptance")]
    if docs.is_dir():
        pairs += [(d / "changes", d / "acceptance") for d in docs.iterdir() if d.is_dir()]
    return [(c, a) for c, a in pairs if c.is_dir()]


def hanging(root: Path):
    out = []
    for ch_dir, acc_dir in ledger_pairs(root):
        acc_text = ""
        if acc_dir.is_dir():
            for a in acc_dir.glob("ACC-*.md"):
                acc_text += a.read_text(encoding="utf-8", errors="ignore").lower()
        for f in sorted(ch_dir.glob("CHG-*.md")):
            text = f.read_text(encoding="utf-8", errors="ignore")
            low = text.lower()
            if any(h in low for h in EXEMPT):
                continue
            if not any(h in low for h in IMPLEMENTED):
                continue
            if SELF_ACC.search(text) and LOW_RISK.search(text):
                continue  # CHG-lite 低風險內嵌自驗
            m = CHG_ID.search(f.stem) or CHG_ID.search(text)
            cid = m.group(0) if m else f.stem
            if cid.lower() not in acc_text:
                out.append(cid)
    return out


def main() -> int:
    try:
        mode = os.environ.get("AI_SDLC_HOOK_MODE", "warn")
        if mode == "off":
            return 0
        data = json.load(sys.stdin)
        if data.get("stop_hook_active"):
            return 0  # 已攔過一次,放行防迴圈
        root = Path(data.get("cwd") or ".").resolve()
        h = hanging(root)
        if not h:
            return 0
        msg = (f"[ai-sdlc] 懸空驗收:{', '.join(h[:5])} 已實作但無 ACC——依「同輪收尾」規則,"
               "請立即依 acceptance-verification 產 ACC 並把 CHG 狀態改為已驗收,再結束。")
        if mode == "block":
            print(json.dumps({"decision": "block", "reason": msg}, ensure_ascii=False))
        else:
            print(json.dumps({"systemMessage": msg}, ensure_ascii=False))
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
