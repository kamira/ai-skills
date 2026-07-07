#!/usr/bin/env python3
"""
brier_report.py — SKILL-12 預測校準回測報告(intel-analysis;報告非閘門,恆 exit 0,--gate 除外)

以 chain_root 為鏈索引:
- Brier Score:取鏈中最後一個非取代版本(verified 且有 outcome.value)計 (p/100 - value)^2;輸出總分與逐鏈明細
- 措辭對表(紀律 16):wording 與 probability 不在 assets/estimative_language.json 區間 → 列出(以 % 為準)
- 敘事漂移(紀律 18):v>=2 而 version_note 空 → 不合規清單(lint 亦擋;此處供回顧統計)
- 延續性估計提醒(紀律 20):window.end 已過而仍 latest → 列出待結案鏈

用法:python3 brier_report.py --repo . [--dir docs/intel/predictions] [--json] [--gate]
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import date
from pathlib import Path


def load(pdir: Path):
    entries = {}
    for f in sorted(pdir.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue  # 壞檔由 prediction_lint fail-loud 把關
        if isinstance(d, dict) and d.get("id"):
            entries[d["id"]] = d
    return entries


def wording_table(script_dir: Path):
    f = script_dir.parent / "assets" / "estimative_language.json"
    try:
        return {k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    except Exception:
        return {}


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--dir", default="docs/intel/predictions")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--gate", action="store_true", help="有措辭不符/漂移時 exit 1(預設報告不擋)")
    args = ap.parse_args(argv[1:])
    pdir = Path(args.repo).resolve() / args.dir
    if not pdir.is_dir():
        print(f"(帳本目錄 {pdir} 不存在——尚無預測鏈)")
        return 0
    entries = load(pdir)
    chains = {}
    for d in entries.values():
        chains.setdefault(d.get("chain_root", d["id"]), []).append(d)

    briers, pending_verify, wording_mismatch, drift = [], [], [], []
    wt = wording_table(Path(__file__).resolve().parent)
    today = date.today().isoformat()
    for root, vs in sorted(chains.items()):
        vs.sort(key=lambda d: d.get("version_seq", 1))
        tip = next((d for d in reversed(vs) if d.get("version_status") != "superseded"), vs[-1])
        out = tip.get("outcome") or {}
        if tip.get("version_status") == "verified" and out.get("value") in (0, 1):
            b = (tip["probability"] / 100 - out["value"]) ** 2
            briers.append((root, tip["id"], tip["probability"], out["value"], round(b, 4)))
        elif tip.get("version_status") == "latest" and (tip.get("window") or {}).get("end", "9999") < today:
            pending_verify.append(f"{root}(window.end={tip['window']['end']} 已過,仍 latest——走紀律 20/23)")
        for d in vs:
            w = d.get("wording")
            if w and w in wt:
                lo, hi = wt[w]
                if not (lo <= d["probability"] <= hi):
                    wording_mismatch.append(f"{d['id']} wording「{w}」({lo}–{hi}%) vs probability {d['probability']}%(以 % 為準,紀律 16)")
            if d.get("version_seq", 1) >= 2 and not str(d.get("version_note", "")).strip():
                drift.append(d["id"])

    report = {
        "chains": len(chains), "snapshots": len(entries),
        "verified": len(briers),
        "brier_mean": round(sum(b for *_, b in briers) / len(briers), 4) if briers else None,
        "brier_detail": [{"chain": r, "tip": t, "probability": p, "outcome": v, "brier": b} for r, t, p, v, b in briers],
        "window_expired_unverified": pending_verify,
        "wording_mismatch": wording_mismatch,
        "narrative_drift(no_version_note)": drift,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"# Brier 校準報告({len(chains)} 鏈 / {len(entries)} 快照;已驗證 {len(briers)})")
        print(f"Brier 平均:{report['brier_mean']}(越低越準;0=完美,0.25=擲硬幣)" if briers else "Brier 平均:—(尚無已驗證鏈)")
        for r, t, p, v, b in briers:
            print(f"  - {r}:p={p}% outcome={v} → Brier {b}({t})")
        for title, items in (("視窗到期未結案(紀律 20/23)", pending_verify),
                             ("措辭↔機率不符(紀律 16)", wording_mismatch),
                             ("敘事漂移:無 version_note(紀律 18)", drift)):
            print(f"{title}:{len(items)}")
            for i in items:
                print(f"  - {i}")
    return 1 if (args.gate and (wording_mismatch or drift)) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
