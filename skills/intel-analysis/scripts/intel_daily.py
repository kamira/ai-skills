#!/usr/bin/env python3
"""
intel_daily.py — 每日盤點 runner(紀律 19-23 的帳本側狀態機;intel-analysis)

分工邊界:**資訊獲取由使用者自理**——本工具零網路、零搜尋,只做:
  盤點清單(該覆蓋的鏈+查證關鍵詞)/ 視窗到期清單(紀律 23)/ 真空偵測(紀律 20)/
  冷鏈候選計算(紀律 21:連續 3 個分析日 A)/ 處置結果記錄(append-only,紀律 19d)。

用法:
  python3 intel_daily.py status --repo .                       # 機器可讀狀態(JSON)
  python3 intel_daily.py brief  --repo . [--date YYYY-MM-DD]   # 當日盤點簡報(人讀)
  python3 intel_daily.py log    --repo . --chain P-… --outcome A|B|C|D [--note "…"] [--date …]

退出碼:0 正常 | 1 錯誤 | 2 coverage 檔格式無效
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import date
from pathlib import Path

OUTCOMES = ("A", "B", "C", "D")
COLD_STREAK = 3  # 紀律 21:連續 3 個分析日真無訊號 → 冷鏈候選
OPEN_TRACKING = ("active", "observing")  # 待覆蓋盤點的追蹤狀態(紀律 19)


def load_chains(pdir: Path):
    """回傳 {chain_root: tip}(tip=版本序最大的快照;壞檔交給 prediction_lint,此處跳過)。"""
    chains = {}
    for f in sorted(pdir.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        root = d.get("chain_root") or d.get("id")
        if not root:
            continue
        cur = chains.get(root)
        if cur is None or d.get("version_seq", 1) > cur.get("version_seq", 1):
            chains[root] = d
    return chains


def load_coverage(cdir: Path):
    """回傳依日期排序的 [(date, {chain: outcome})];格式錯 → (None, 檔名)。"""
    days = []
    for f in sorted(cdir.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            entries = {e["chain"]: e["outcome"] for e in d["entries"]}
        except (json.JSONDecodeError, KeyError, TypeError):
            return None, f.name
        days.append((d.get("date", f.stem), entries))
    return days, None


def analyze(repo: Path, today: str):
    pdir = repo / "docs" / "intel" / "predictions"
    cdir = repo / "docs" / "intel" / "coverage"
    chains = load_chains(pdir) if pdir.is_dir() else {}
    days, bad = load_coverage(cdir) if cdir.is_dir() else ([], None)
    if bad:
        return None, f"coverage 檔格式無效:{bad}(見 daily-loop coverage 檔格式)"

    to_cover, window_due, dormant, cold_candidates = [], [], [], []
    recent = [entries for _, entries in days[-COLD_STREAK:]]
    for root, tip in sorted(chains.items()):
        vs, ts = tip.get("version_status"), tip.get("tracking_status", "active")
        keys = {"tags": tip.get("tags", []), "actors": tip.get("actors", []),
                "indicators": tip.get("indicators", [])}
        if ts == "dormant":
            dormant.append({"chain": root, "keywords": keys, "statement": tip.get("statement", "")})
            continue
        if vs != "latest" or ts not in OPEN_TRACKING:
            continue  # verified/invalidated/superseded 不入盤點(紀律 19 範圍)
        end = (tip.get("window") or {}).get("end", "")
        item = {"chain": root, "tip": tip["id"], "probability": tip.get("probability"),
                "statement": tip.get("statement", ""), "keywords": keys, "window_end": end}
        to_cover.append(item)
        if end and end <= today:
            window_due.append({**item, "action": "紀律 23:主動查證結案;仍真空 → 處置 D(紀律 20 延續性估計)"})
        if len(recent) == COLD_STREAK and all(root in e and e[root] == "A" for e in recent):
            cold_candidates.append({"chain": root, "reason": f"最近 {COLD_STREAK} 個分析日皆 A(真無訊號)",
                                    "action": "確認後將 latest 的 tracking_status 改 dormant(就地更新)"})
    return {"date": today, "chains_total": len(chains), "to_cover": to_cover,
            "window_due": window_due, "cold_candidates": cold_candidates, "dormant": dormant}, None


def cmd_status(args) -> int:
    result, err = analyze(Path(args.repo).resolve(), args.date)
    if err:
        print(f"ERROR: {err}")
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_brief(args) -> int:
    result, err = analyze(Path(args.repo).resolve(), args.date)
    if err:
        print(f"ERROR: {err}")
        return 2
    r = result
    print(f"# 每日盤點簡報 — {r['date']}(鏈總數 {r['chains_total']};資訊獲取由你自理,本簡報只列「該查什麼」)")
    print(f"\n## 待覆蓋鏈({len(r['to_cover'])})——逐鏈以你的資料源查證,處置 A/B/C/D 後 log")
    for c in r["to_cover"]:
        kw = ", ".join(c["keywords"]["tags"] + c["keywords"]["actors"] + c["keywords"]["indicators"][:3])
        print(f"  - {c['chain']}(p={c['probability']}%,window.end={c['window_end'] or '—'}):{c['statement'][:50]}")
        print(f"    查證關鍵詞:{kw or '(無——建議補 tags/indicators)'}")
    print(f"\n## 視窗到期待結案({len(r['window_due'])})(紀律 23/20)")
    for c in r["window_due"]:
        print(f"  - {c['chain']}(end={c['window_end']}):{c['action']}")
    print(f"\n## 冷鏈候選({len(r['cold_candidates'])})(紀律 21;降階由你確認)")
    for c in r["cold_candidates"]:
        print(f"  - {c['chain']}:{c['reason']} → {c['action']}")
    print(f"\n## 休眠鏈({len(r['dormant'])})——你的當日資料若命中其關鍵詞,依紀律 21 喚醒")
    for c in r["dormant"]:
        kw = ", ".join(c["keywords"]["tags"] + c["keywords"]["actors"])
        print(f"  - {c['chain']}:{kw or '(無關鍵詞)'}")
    return 0


def cmd_log(args) -> int:
    if args.outcome not in OUTCOMES:
        print(f"ERROR: outcome 須為 {OUTCOMES}(紀律 19d 四類處置)")
        return 1
    repo = Path(args.repo).resolve()
    cdir = repo / "docs" / "intel" / "coverage"
    cdir.mkdir(parents=True, exist_ok=True)
    f = cdir / f"{args.date}.json"
    data = {"date": args.date, "entries": []}
    if f.is_file():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERROR: 當日 coverage 檔解析失敗(fail-loud):{e}")
            return 2
    data["entries"] = [e for e in data.get("entries", []) if e.get("chain") != args.chain]
    data["entries"].append({"chain": args.chain, "outcome": args.outcome, "note": args.note or ""})
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ {args.date} 記錄:{args.chain} → {args.outcome}(共 {len(data['entries'])} 鏈)")
    return 0


def main(argv) -> int:
    ap = argparse.ArgumentParser(description="intel-analysis 每日盤點 runner(帳本側;零網路)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("status", "brief", "log"):
        p = sub.add_parser(name)
        p.add_argument("--repo", default=".")
        p.add_argument("--date", default=date.today().isoformat())
        if name == "log":
            p.add_argument("--chain", required=True)
            p.add_argument("--outcome", required=True)
            p.add_argument("--note", default="")
    args = ap.parse_args(argv[1:])
    try:
        return {"status": cmd_status, "brief": cmd_brief, "log": cmd_log}[args.cmd](args)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
