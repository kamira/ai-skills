#!/usr/bin/env python3
"""
autopilot_runner.py — ai-sdlc-autopilot 驅動器(狀態機與裁判;不含 LLM)

施工與審查由外部 headless agent 指令執行(--agent-cmd,模板中 {brief} 代入簡報檔路徑);
runner 只負責:解析計畫、裁決停點、驅動逐 task 迴圈、打勾與 commit、維護 live handshake。

用法:
  python3 autopilot_runner.py plan-check --chg <CHG.md>
  python3 autopilot_runner.py run --chg <CHG.md> --repo . \\
      [--agent-cmd 'claude -p "$(cat {brief})"'] [--test-cmd 'pytest -q'] \\
      [--dry-run] [--no-commit] [--max-tasks N] [--confirmed] [--policy <json>]
  python3 autopilot_runner.py status --chg <CHG.md>

退出碼:0=完成 | 1=非預期錯誤 | 2=計畫無效 | 3=合法停點(原因已印出;cron/CI 據此接線)
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# 永遠停點:硬編碼——任何設定檔不可移除或放寬(見 autopilot-loop「停點決策順序」第 1 層)
PERMANENT_HALTS = ("irreversible-delete", "payments", "prod-migration", "security-boundary")
STAGES = ("confirm_gate", "task_review", "operational_verify", "acceptance", "pr", "merge")
ACTIONS = {"auto", "confirm", "halt", "halt_independent"}
DEFAULT_POLICY = {
    "low":    {"confirm_gate": "auto",    "task_review": "auto", "operational_verify": "auto", "acceptance": "auto",             "pr": "auto", "merge": "auto"},
    "medium": {"confirm_gate": "confirm", "task_review": "auto", "operational_verify": "auto", "acceptance": "auto",             "pr": "auto", "merge": "auto"},
    "high":   {"confirm_gate": "halt",    "task_review": "auto", "operational_verify": "halt", "acceptance": "halt_independent", "pr": "auto", "merge": "halt"},
}

TASK_RE = re.compile(r"^- \[(?P<tick>[ xX])\] (?P<tid>T\d+)\. (?P<title>.+?)\s*$")
IFACE_RE = re.compile(r"^\s+-\s*interfaces:\s*\S")
TEST_RE = re.compile(r"^\s+-\s*test:\s*(?P<v>\S.*)$")
GC_RE = re.compile(r"^###\s*Global Constraints", re.MULTILINE)
AOP_RE = re.compile(r"^###\s*Acceptance operation", re.MULTILINE)  # 末端操作測試節
DOCS_ONLY_RE = re.compile(r"Acceptance-operation:\s*n/?a|docs-only", re.IGNORECASE)  # 純文件豁免宣告
RISK_RE = re.compile(r"(風險分級|Risk)\s*[::]\s*[^\n]{0,40}?(高|high|中|medium|低|low)", re.IGNORECASE)
CHG_ID_RE = re.compile(r"CHG-\d{8}-\d+")
PERM_RE = re.compile(r"permanent-halt:\s*([\w-]+)")
AUTONOMY_HALT_RE = re.compile(r"^-\s*Autonomy\s*[::].*halt", re.MULTILINE | re.IGNORECASE)
VERDICT_RE = re.compile(r"\[task-review\]\s*(?:T\d+|branch)\s*\|\s*spec:\s*(pass|fail|cannot-verify)\s*\|\s*quality:\s*(pass|fail)", re.IGNORECASE)


def die(msg: str, code: int) -> int:
    print(f"{'HALT' if code == 3 else 'ERROR' if code == 1 else 'INVALID-PLAN'}: {msg}")
    return code


def read_chg(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_tasks(text: str):
    """回傳 (problems, tasks);task = {tid,title,ticked,has_iface,has_test,line_no}"""
    problems, tasks = [], []
    lines = text.splitlines()
    if not GC_RE.search(text):
        problems.append("缺「### Global Constraints」節——全域約束是 task 簡報自包含的前提")
    for i, line in enumerate(lines):
        m = TASK_RE.match(line)
        if not m:
            continue
        block = lines[i + 1:i + 6]  # task 的縮排附屬行(interfaces/test 應緊隨)
        sub = [l for l in block if l.startswith((" ", "\t")) and l.strip().startswith("-")]
        tasks.append({
            "tid": m.group("tid"), "title": m.group("title"),
            "ticked": m.group("tick").lower() == "x", "line_no": i,
            "has_iface": any(IFACE_RE.match(l) for l in sub),
            "has_test": any(TEST_RE.match(l) for l in sub),
        })
    if not tasks:
        problems.append("找不到任何 task(格式:- [ ] T1. <標題>)")
    for t in tasks:
        if not t["has_iface"]:
            problems.append(f"{t['tid']} 缺 interfaces: 行(consumes/produces)")
        if not t["has_test"]:
            problems.append(f"{t['tid']} 缺 test: 行(指令或可斷言條件)")
    nums = [int(t["tid"][1:]) for t in tasks]
    if nums != list(range(1, len(nums) + 1)):
        problems.append(f"task 編號須 T1..T{len(nums)} 連續,實得 {[t['tid'] for t in tasks]}")
    return problems, tasks


def load_policy(path):
    """載入停點矩陣;驗證值域,且 permanent_halts 不可縮減(硬清單以程式碼為準)。"""
    matrix = DEFAULT_POLICY
    if path:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        cfg_perm = data.get("permanent_halts")
        if cfg_perm is not None and not set(PERMANENT_HALTS) <= set(cfg_perm):
            raise ValueError("policy 不得縮減 permanent_halts(硬清單:%s)" % ", ".join(PERMANENT_HALTS))
        matrix = data.get("defaults", matrix)
    for risk, stages in matrix.items():
        for st, act in stages.items():
            if st not in STAGES or act not in ACTIONS:
                raise ValueError(f"policy 值域錯誤:{risk}.{st}={act}")
    return matrix


def risk_of(text: str) -> str:
    m = RISK_RE.search(text)
    if not m:
        return "high"  # 查無=保守
    v = m.group(2).lower()
    return {"高": "high", "中": "medium", "低": "low"}.get(v, v)


def stage_action(matrix, risk: str, stage: str, chg_text: str) -> str:
    act = matrix.get(risk, matrix["high"]).get(stage, "halt")
    if AUTONOMY_HALT_RE.search(chg_text) and stage in ("confirm_gate", "merge"):
        act = "halt"  # Autonomy 欄只准加嚴
    return act


def write_handshake(repo: Path, chg_id: str, doing: str, nxt: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    wl = repo / "docs" / "worklog"
    wl.mkdir(parents=True, exist_ok=True)
    (wl / "handshake-autopilot.md").write_text(
        f"branch/role/scope: autopilot / {chg_id}\ndoing: {doing}\nnext: {nxt}\n"
        f"last-updated: {ts} (UTC+0)\n", encoding="utf-8")


def tick_task(chg_path: Path, tid: str) -> None:
    lines = read_chg(chg_path).splitlines(keepends=True)
    for i, line in enumerate(lines):
        m = TASK_RE.match(line.rstrip("\n"))
        if m and m.group("tid") == tid:
            lines[i] = line.replace("- [ ]", "- [x]", 1)
            break
    chg_path.write_text("".join(lines), encoding="utf-8")


def run_shell(cmd: str, cwd: Path):
    return subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)


def agent_call(tmpl: str, brief: str, cwd: Path):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(brief)
        brief_path = f.name
    return run_shell(tmpl.replace("{brief}", brief_path), cwd)


def build_brief(chg_text: str, task, mode: str, extra: str = "") -> str:
    gc = chg_text[chg_text.find("### Global Constraints"):]
    gc = gc[:gc.find("### Tasks")] if "### Tasks" in gc else gc[:1500]
    head = ("依 TDD(紅→綠→重構)完成以下 task;先寫失敗測試。" if mode == "build"
            else "唯讀審查以下 task 的 diff;輸出一行判定:[task-review] %s | spec: ... | quality: ... | 理由" % task["tid"])
    return f"{head}\n\n{gc}\n\n## Task\n{task['tid']}. {task['title']}\n{extra}\n"


def cmd_plan_check(args) -> int:
    problems, tasks = parse_tasks(read_chg(Path(args.chg)))
    if problems:
        print("❌ plan-check 未通過:")
        for p in problems:
            print(f"  - {p}")
        return 2
    text = read_chg(Path(args.chg))
    if not AOP_RE.search(text) and not DOCS_ONLY_RE.search(text):
        print("  (提示:無「### Acceptance operation」——收尾將要求實際操作驗收;純文件變更請標「Acceptance-operation: n/a (docs-only)」。此為非阻斷提示。)")
    print(f"✅ plan-check 通過({len(tasks)} 個 task,格式完整)。")
    return 0


def cmd_status(args) -> int:
    text = read_chg(Path(args.chg))
    _, tasks = parse_tasks(text)
    done = [t for t in tasks if t["ticked"]]
    todo = [t for t in tasks if not t["ticked"]]
    mid = CHG_ID_RE.search(text)
    print(f"CHG:{mid.group(0) if mid else '?'} | 風險:{risk_of(text)}")
    print(f"已完成 {len(done)}/{len(tasks)};下一個:{todo[0]['tid'] + '. ' + todo[0]['title'] if todo else '(無——進入收尾)'}")
    return 0


def cmd_run(args) -> int:
    chg_path, repo = Path(args.chg), Path(args.repo).resolve()
    text = read_chg(chg_path)
    mid = CHG_ID_RE.search(text)
    chg_id = mid.group(0) if mid else chg_path.stem
    problems, tasks = parse_tasks(text)
    if problems:
        return cmd_plan_check(args)
    try:
        matrix = load_policy(args.policy)
    except ValueError as e:
        return die(str(e), 1)
    risk = risk_of(text)

    # 第 1 層:永遠停點(存在即停,任何風險等級皆然)
    perm = PERM_RE.findall(text)
    if perm:
        return die(f"永遠停點標記 {perm}:該動作必須由人執行/在場,autopilot 不代行", 3)

    # 確認閘
    act = stage_action(matrix, risk, "confirm_gate", text)
    if act != "auto" and not args.confirmed:
        return die(f"確認閘({risk} 風險 → {act}):請人審閱 CHG 後以 --confirmed 重跑(或依 knowledge 預授權)", 3)

    todo = [t for t in tasks if not t["ticked"]]
    ran = 0
    for t in todo:
        if args.max_tasks and ran >= args.max_tasks:
            print(f"⏸ --max-tasks {args.max_tasks} 已達,暫停(續作點=checkbox)")
            write_handshake(repo, chg_id, f"{chg_id} 暫停於 {t['tid']} 之前", t["tid"])
            return 0
        write_handshake(repo, chg_id, f"{chg_id} task {t['tid']}/{len(tasks)}", "施工→測試→審查")
        if args.dry_run:
            print(f"[dry-run] {t['tid']} 施工=模擬 ok;測試=模擬綠;review=模擬 [task-review] {t['tid']} | spec: pass | quality: pass")
        elif args.agent_cmd:
            ok = False
            for attempt in (1, 2):  # 一次回修機會
                r = agent_call(args.agent_cmd, build_brief(text, t, "build"), repo)
                if r.returncode != 0:
                    return die(f"{t['tid']} agent 施工失敗:{r.stderr.strip()[:200]}", 1)
                if args.test_cmd:
                    tr = run_shell(args.test_cmd, repo)
                    if tr.returncode != 0:
                        if attempt == 2:
                            return die(f"{t['tid']} 測試二連敗——切 systematic-debugging 或人工介入", 3)
                        continue
                rv = agent_call(args.agent_cmd, build_brief(text, t, "review"), repo)
                m = VERDICT_RE.search(rv.stdout)
                if m and m.group(1).lower() != "fail" and m.group(2).lower() == "pass":
                    print(f"{t['tid']} 判定:{m.group(0)}")
                    ok = True
                    break
                if attempt == 2:
                    return die(f"{t['tid']} review 二連敗:{(m.group(0) if m else '無判定行')}", 3)
            if not ok:
                return die(f"{t['tid']} 未通過施工/審查迴圈", 1)
        else:
            print(build_brief(text, t, "build"))
            return die(f"{t['tid']}:無 --agent-cmd(人在迴圈模式)——請依上方簡報人工完成後打勾重跑", 3)
        tick_task(chg_path, t["tid"])
        text = read_chg(chg_path)
        if not (args.no_commit or args.dry_run):
            run_shell("git add -A", repo)
            run_shell(f'git commit -m "{chg_id}: {t["tid"]} {t["title"]}"', repo)
        else:
            print(f"[skip-commit] 等效訊息:{chg_id}: {t['tid']} {t['title']}")
        ran += 1

    # 整支 review → 實際操作驗收 → 驗收 → PR → merge
    print("[stage] 整支 review:" + ("[dry-run] 模擬 [task-review] branch | spec: pass | quality: pass" if args.dry_run else "以最強模型對整條 branch diff 審一次(判定行入 ACC)"))

    # 實際操作驗收(task 測試=單元/build;此處把整個變更真的跑一次)
    op_act = stage_action(matrix, risk, "operational_verify", text)
    if DOCS_ONLY_RE.search(text) and not AOP_RE.search(text):
        print("[stage] 實際操作驗收:docs-only 宣告,略過")
    elif not AOP_RE.search(text):
        return die("缺實際操作驗收:程式類變更不得只憑 task 級測試收尾——請在 CHG 補「### Acceptance operation」"
                   "(operate/observe/pass)或標記「Acceptance-operation: n/a (docs-only)」", 3)
    elif args.dry_run:
        print(f"[dry-run] 實際操作驗收=模擬 operate/observe/pass 通過(op_act={op_act})")
    elif op_act == "auto" and args.verify_cmd:
        vr = run_shell(args.verify_cmd, repo)
        if vr.returncode != 0:
            return die(f"實際操作驗收失敗(--verify-cmd 非零):{vr.stderr.strip()[:200] or vr.stdout.strip()[:200]}", 3)
        print(f"[stage] 實際操作驗收:--verify-cmd 通過\n{vr.stdout.strip()[:300]}")
    else:
        m = AOP_RE.search(text)
        print(text[m.start():m.start() + 600])
        reason = "高風險:操作簽核須由人執行" if op_act == "halt" else "無 --verify-cmd(人在迴圈)"
        return die(f"實際操作驗收({reason}):請依上方 operate/observe/pass 實際操作、記錄證據入 ACC,再續 merge", 3)

    act = stage_action(matrix, risk, "acceptance", text)
    if act == "halt_independent":
        return die("驗收(高風險):需獨立驗收者(≠實作者)產 ACC——autopilot 停,交人/獨立 agent", 3)
    print("[stage] 驗收:依 acceptance-verification 產 ACC(task 判定行=證據欄)")
    act = stage_action(matrix, risk, "merge", text)
    if act != "auto":
        return die(f"merge({risk} 風險 → {act}):PR 已備,合併由人執行", 3)
    if args.dry_run:
        print("[dry-run] PR+merge=模擬完成")
    elif shutil.which("gh"):
        print("[stage] PR/merge:gh 可用——請確認 CHG 收尾欄後執行 gh pr create/merge(帶 CHG 編號)")
    else:
        return die("無 gh CLI:請人工開 PR 並 merge(commit 已帶 CHG 編號)", 3)
    write_handshake(repo, chg_id, f"{chg_id} 全 task 完成", "收尾:ACC/Commit-PR 回填/重複性檢查/knowledge")
    print(f"✅ {chg_id}:{len(tasks)} task 全數完成;收尾提醒=CHG 狀態+Commit/PR+重複性檢查欄+knowledge。")
    return 0


def main(argv) -> int:
    ap = argparse.ArgumentParser(description="ai-sdlc-autopilot runner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan-check", "run", "status"):
        p = sub.add_parser(name)
        p.add_argument("--chg", required=True)
        if name == "run":
            p.add_argument("--repo", default=".")
            p.add_argument("--agent-cmd", default=None, help="headless agent 指令模板,{brief}=簡報檔路徑")
            p.add_argument("--test-cmd", default=None, help="每個 task 的單元/build 測試指令")
            p.add_argument("--verify-cmd", default=None, help="末端操作測試指令(把變更真的跑一次;見 ### Acceptance operation)")
            p.add_argument("--policy", default=None, help="autopilot_policy.json 路徑(預設內建矩陣)")
            p.add_argument("--dry-run", action="store_true")
            p.add_argument("--no-commit", action="store_true")
            p.add_argument("--max-tasks", type=int, default=0)
            p.add_argument("--confirmed", action="store_true", help="人已於確認閘核可(confirm 階段放行)")
    args = ap.parse_args(argv[1:])
    try:
        return {"plan-check": cmd_plan_check, "run": cmd_run, "status": cmd_status}[args.cmd](args)
    except FileNotFoundError as e:
        return die(str(e), 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
