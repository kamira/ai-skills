#!/usr/bin/env python3
"""
prediction_lint.py — 預測驗證帳本 fail-loud 鏈驗證 + INDEX 生成(intel-analysis)

驗證 docs/intel/predictions/*.json(一鏈版本一快照):解析失敗/缺必填/enum 錯/id≠檔名/
id 格式錯/斷鏈(prev_id 不存在或版本序不連續)/同鏈多 latest/機率非 5% 步進/v>=2 缺
version_note/未知欄位 → 全部擋下(一條規則靜默消失,比一次提交被擋更糟)。

用法:
  python3 prediction_lint.py --repo .              # 驗證(exit 0/1)
  python3 prediction_lint.py --repo . --index      # 驗證+重生 INDEX.md(生成物,永不手改)
  python3 prediction_lint.py --repo . --check      # 驗證+INDEX 新鮮度(過期 exit 1)
  python3 prediction_lint.py --repo . --dir docs/intel/predictions   # 自訂帳本路徑
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ID_ROOT = re.compile(r"^P-\d{4}-\d{4}-\d{2}$")
ID_ANY = re.compile(r"^P-\d{4}-\d{4}-\d{2}(-v(\d+))?$")
REQUIRED = ("id", "chain_root", "version_seq", "version_status", "statement", "probability")
V_STATUS = {"latest", "superseded", "verified", "invalidated"}
T_STATUS = {"active", "observing", "dormant", "verified", "invalidated"}
WORDINGS = {"幾乎確定", "很可能", "可能", "兩可", "不太可能", "很不可能", "幾乎不可能"}
KNOWN = {"id", "chain_root", "prev_id", "version_seq", "version_status", "version_note",
         "tracking_status", "statement", "probability", "wording", "key_assumptions",
         "triggers", "indicators", "window", "source_analysis", "outcome", "tags", "actors", "note"}


def load_entries(pdir: Path):
    problems, entries = [], {}
    for f in sorted(pdir.glob("*.json")):
        rel = f.name
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{rel} JSON 解析失敗(fail-loud,不跳過):{e}")
            continue
        missing = [k for k in REQUIRED if k not in d]
        if missing:
            problems.append(f"{rel} 缺必填欄:{', '.join(missing)}(schema:assets/prediction_entry.schema.json)")
            continue
        if d["id"] != f.stem:
            problems.append(f"{rel} id「{d['id']}」≠ 檔名「{f.stem}」——檔名即 id")
        m = ID_ANY.match(str(d["id"]))
        if not m:
            problems.append(f"{rel} id 格式錯(P-YYYY-MMDD-NN[-vK])")
            continue
        seq_in_id = int(m.group(2)) if m.group(2) else 1
        if d["version_seq"] != seq_in_id:
            problems.append(f"{rel} version_seq={d['version_seq']} 與 id 後綴版本 {seq_in_id} 不一致")
        if not ID_ROOT.match(str(d["chain_root"])):
            problems.append(f"{rel} chain_root 格式錯(須為首發 ID)")
        if d["version_status"] not in V_STATUS:
            problems.append(f"{rel} version_status「{d['version_status']}」不在 {sorted(V_STATUS)}")
        if "tracking_status" in d and d["tracking_status"] not in T_STATUS:
            problems.append(f"{rel} tracking_status「{d['tracking_status']}」不在 {sorted(T_STATUS)}")
        p = d["probability"]
        if not isinstance(p, int) or not (0 <= p <= 100) or p % 5 != 0:
            problems.append(f"{rel} probability={p!r} 須為 0–100 整數且 5% 步進(紀律 6)")
        if "wording" in d and d["wording"] not in WORDINGS:
            problems.append(f"{rel} wording「{d['wording']}」不在標準措辭七級(紀律 16)")
        if d["version_seq"] >= 2 and not str(d.get("version_note", "")).strip():
            problems.append(f"{rel} v{d['version_seq']} 缺 version_note——無說明的版本視為不合規(紀律 18 敘事漂移)")
        unknown = set(d) - KNOWN
        if unknown:
            problems.append(f"{rel} 未知欄位 {sorted(unknown)}——打錯欄名=資料靜默消失(schema 為準)")
        entries[d["id"]] = d
    return problems, entries


def check_chains(entries: dict):
    problems, chains = [], {}
    for d in entries.values():
        chains.setdefault(d["chain_root"], []).append(d)
    for root, vs in sorted(chains.items()):
        vs.sort(key=lambda d: d["version_seq"])
        seqs = [d["version_seq"] for d in vs]
        if seqs != list(range(1, len(seqs) + 1)):
            problems.append(f"鏈 {root} 版本序不連續:{seqs}(快照不可跳號、不可缺版)")
        open_states = [d for d in vs if d["version_status"] in ("latest", "verified", "invalidated")]
        latests = [d for d in vs if d["version_status"] == "latest"]
        if len(latests) > 1:
            problems.append(f"鏈 {root} 有 {len(latests)} 個 latest——同鏈任一時刻僅能一個")
        if not open_states:
            problems.append(f"鏈 {root} 全為 superseded——鏈尾必須是 latest/verified/invalidated 之一")
        for d in vs:
            if d["version_seq"] == 1:
                if d.get("prev_id"):
                    problems.append(f"{d['id']} 首發不得有 prev_id")
                if d["chain_root"] != d["id"]:
                    problems.append(f"{d['id']} 首發 chain_root 須=自身 id")
            else:
                prev = d.get("prev_id")
                if not prev or prev not in entries:
                    problems.append(f"{d['id']} prev_id「{prev}」不存在——斷鏈")
                elif entries[prev]["version_seq"] != d["version_seq"] - 1:
                    problems.append(f"{d['id']} prev_id 版本序不相鄰")
                elif entries[prev]["version_status"] not in ("superseded", "verified", "invalidated"):
                    problems.append(f"{d['id']} 的上一版 {prev} 仍為 latest——建新快照時須將上一版改 superseded")
    return problems, chains


def render_index(chains: dict) -> str:
    lines = ["# INDEX — 預測驗證帳本(生成物:prediction_lint.py --index,永不手改)", "",
             "| chain_root | 最新版 | seq | version_status | tracking | prob | statement | window.end |",
             "|---|---|---|---|---|---|---|---|"]
    for root, vs in sorted(chains.items()):
        tip = max(vs, key=lambda d: d["version_seq"])
        lines.append("| {} | {} | {} | {} | {} | {}% | {} | {} |".format(
            root, tip["id"], tip["version_seq"], tip["version_status"],
            tip.get("tracking_status", ""), tip["probability"],
            str(tip["statement"])[:60].replace("|", "/"), (tip.get("window") or {}).get("end", "")))
    return "\n".join(lines) + "\n"


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--dir", default="docs/intel/predictions")
    ap.add_argument("--index", action="store_true", help="重生 INDEX.md")
    ap.add_argument("--check", action="store_true", help="驗 INDEX 新鮮度(過期 exit 1)")
    args = ap.parse_args(argv[1:])
    pdir = Path(args.repo).resolve() / args.dir
    if not pdir.is_dir():
        print(f"(帳本目錄 {pdir} 不存在——尚無預測鏈,略過)")
        return 0
    problems, entries = load_entries(pdir)
    if not problems:
        chain_problems, chains = check_chains(entries)
        problems += chain_problems
    if problems:
        print("❌ prediction-lint 未通過:")
        for p in problems:
            print(f"  - {p}")
        return 1
    _, chains = check_chains(entries)
    idx = render_index(chains)
    index_path = pdir / "INDEX.md"
    if args.index:
        index_path.write_text(idx, encoding="utf-8")
        print(f"✅ 驗證通過;INDEX.md 已重生({len(chains)} 鏈 / {len(entries)} 快照)。")
        return 0
    if args.check:
        if not index_path.is_file() or index_path.read_text(encoding="utf-8") != idx:
            print("❌ INDEX.md 過期或缺失——跑 prediction_lint.py --index 重生後提交")
            return 1
    print(f"✅ prediction-lint 通過({len(chains)} 鏈 / {len(entries)} 快照)。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
