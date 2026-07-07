#!/usr/bin/env python3
"""
ai_sdlc_mcp.py — ai-sdlc suite MCP server(stdio、stdlib-only、全工具唯讀)

newline-delimited JSON-RPC 2.0:initialize / tools/list / tools/call / ping。
五工具:governance_health、doc_integrity_check、plan_check、halt_gate、knowledge_search。
前四者包裝既有 CLI 腳本(單一真相);knowledge_search 原生實作(檔案唯讀)。

腳本尋徑順序:env AI_SDLC_SKILLS_DIR → plugin 內 skills/ 複本 → repo 頂層 skills/。
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = "2024-11-05"


def skills_dir():
    cands = []
    if os.environ.get("AI_SDLC_SKILLS_DIR"):
        cands.append(Path(os.environ["AI_SDLC_SKILLS_DIR"]))
    cands += [HERE.parent / "skills", HERE.parent.parent.parent / "skills"]
    for c in cands:
        if (c / "ai-sdlc" / "scripts").is_dir():
            return c
    return None


def run_script(rel: str, args: list) -> dict:
    base = skills_dir()
    if base is None:
        return {"error": "找不到 skills/(設 AI_SDLC_SKILLS_DIR 或執行 build_suite.py 同步複本)"}
    script = base / rel
    if not script.is_file():
        return {"error": f"腳本不存在:{script}"}
    r = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, timeout=120)
    return {"exit_code": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()}


# ---- 工具實作(全部唯讀) ----

def t_governance_health(a: dict) -> dict:
    out = run_script("ai-sdlc/scripts/governance_health.py", ["--repo", a.get("repo", "."), "--json"])
    if "stdout" in out and out.get("exit_code") == 0:
        try:
            return json.loads(out["stdout"])
        except json.JSONDecodeError:
            pass
    return out


def t_doc_integrity(a: dict) -> dict:
    args = ["--repo", a.get("repo", ".")]
    if a.get("commits_since"):
        args += ["--commits-since", a["commits_since"]]
    out = run_script("ai-sdlc/scripts/doc_integrity_check.py", args)
    problems = [l.strip()[2:] for l in out.get("stdout", "").splitlines() if l.strip().startswith("- ")]
    return {"ok": out.get("exit_code") == 0, "problems": problems, "raw": out}


def t_plan_check(a: dict) -> dict:
    out = run_script("ai-sdlc-autopilot/scripts/autopilot_runner.py", ["plan-check", "--chg", a["chg"]])
    return {"ok": out.get("exit_code") == 0, "raw": out}


def t_halt_gate(a: dict) -> dict:
    args = ["--gate", a["gate"], "--risk", a["risk"], "--why"]
    if a.get("action"):
        args += ["--action", a["action"]]
    if a.get("autonomy"):
        args += ["--autonomy", a["autonomy"]]
    out = run_script("ai-sdlc/scripts/halt_gate.py", args)
    code = out.get("exit_code")
    return {"decision": "AUTO" if code == 0 else "HALT" if code == 10 else "ERROR", "why": out.get("stdout", "")}


def _load_vocab(kdir: Path) -> dict:
    f = kdir / "vocabulary.json"
    if not f.is_file():
        return {}
    try:
        return {k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    except json.JSONDecodeError:
        return {}


def t_knowledge_search(a: dict) -> dict:
    """範圍檢索:query 詞經 vocabulary 正規化成 tags → 與條目 tags 交集;原詞對 keywords/內文子串。"""
    repo = Path(a.get("repo", ".")).resolve()
    kdir = repo / a.get("docs_root", "docs") / "knowledge"
    if not kdir.is_dir():
        return {"error": f"{kdir} 不存在(受治理 repo 應先 bootstrap;見 ai-sdlc knowledge「先建」)"}
    vocab = _load_vocab(kdir)
    terms = [t.lower() for t in a.get("query", [])]
    tags = set()
    for t in terms:
        for tag, aliases in vocab.items():
            if t == tag or any(t == al.lower() or t in al.lower() for al in aliases):
                tags.add(tag)
    hits = []
    entries_dir = kdir / "entries"
    if entries_dir.is_dir():  # 拆檔模式:JSON 條目
        for f in sorted(entries_dir.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            etags = set(map(str.lower, d.get("tags", [])))
            kw = " ".join(d.get("keywords", [])).lower()
            if etags & tags or any(t in kw for t in terms):
                hits.append(d)
    for f in sorted(kdir.glob("*.md")):  # 單檔模式:掃 KN/DIR 小節
        text = f.read_text(encoding="utf-8", errors="ignore")
        for sec in re.split(r"(?=^## (?:KN|DIR)-)", text, flags=re.MULTILINE):
            m = re.match(r"^## ((?:KN|DIR)-[\w.]+)", sec)
            if not m:
                continue
            low = sec.lower()
            if any(t in low for t in terms) or any(tag in low for tag in tags):
                hits.append({"id": m.group(1), "source": f.name, "text": sec.strip()[:800]})
    return {"normalized_tags": sorted(tags), "hits": hits, "count": len(hits)}


TOOLS = {
    "governance_health": (t_governance_health, "治理健康度報告(唯讀;CHG 狀態/懸空/knowledge 階梯/警示)", {
        "type": "object", "properties": {"repo": {"type": "string", "description": "repo 路徑(預設 .)"}}, "required": []}),
    "doc_integrity_check": (t_doc_integrity, "文檔抗漂移 lint(結構同步/CHG↔ACC/欄位/secrets/knowledge bootstrap/重複性檢查欄)", {
        "type": "object", "properties": {"repo": {"type": "string"}, "commits_since": {"type": "string", "description": "掃描 REF..HEAD commit 治理"}}, "required": []}),
    "plan_check": (t_plan_check, "autopilot 計畫格式驗證(Global Constraints+interfaces/test 行+checkbox)", {
        "type": "object", "properties": {"chg": {"type": "string", "description": "CHG 檔路徑"}}, "required": ["chg"]}),
    "halt_gate": (t_halt_gate, "自主停點查詢:AUTO(續跑)或 HALT(等人)", {
        "type": "object", "properties": {
            "gate": {"type": "string", "enum": ["requirement_confirmed", "structure_confirmed", "before_implement", "acceptance_failed", "before_merge_or_release"]},
            "risk": {"type": "string", "enum": ["low", "medium", "high"]},
            "action": {"type": "string"}, "autonomy": {"type": "string", "enum": ["auto", "halt"]}}, "required": ["gate", "risk"]}),
    "knowledge_search": (t_knowledge_search, "知識庫範圍檢索(vocabulary 正規化+tags 交集+keywords/內文子串;唯讀)", {
        "type": "object", "properties": {
            "repo": {"type": "string"}, "query": {"type": "array", "items": {"type": "string"}, "description": "任務側關鍵詞(任何語言)"},
            "docs_root": {"type": "string", "description": "治理文件根(預設 docs;本 repo 慣例可用 docs/ai-sdlc)"}}, "required": ["query"]}),
}


def handle(req: dict):
    mid = req.get("id")
    method = req.get("method", "")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "ai-sdlc", "version": "1.0.0"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": n, "description": d, "inputSchema": s} for n, (_, d, s) in TOOLS.items()]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        name = req.get("params", {}).get("name")
        args = req.get("params", {}).get("arguments", {}) or {}
        if name not in TOOLS:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown tool: {name}"}}
        try:
            result = TOOLS[name][0](args)
            is_err = isinstance(result, dict) and "error" in result
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                "isError": bool(is_err)}}
        except Exception as e:  # 工具層錯誤回報,不讓 server 掛掉
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": json.dumps({"error": str(e)}, ensure_ascii=False)}],
                "isError": True}}
    if mid is not None:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
    return None


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
