# 資料結構 — ai-sdlc-autopilot(格式契約)

- 專案:ai-skills / skill: ai-sdlc-autopilot
- 版本:v1.0 | 日期:2026-07-06(UTC+0)

## 1. 計畫格式(CHG 修改指引內;plan-check 驗證)

```markdown
### Global Constraints(全域約束——每個 task 都要遵守)
- <約束句,可測試措辭>

### Tasks(checkbox=續作點)
- [ ] T1. <標題>
  - interfaces: consumes <輸入/前置> / produces <輸出/交付>
  - test: <驗證方式——指令或可斷言條件>
- [ ] T2. ...

### Acceptance operation(末端操作測試——程式類必附;純文件改一行 `Acceptance-operation: n/a (docs-only)`)
- operate: <怎麼真的跑/操作>
- observe: <什麼確認可用>
- pass: <通過標準>
```

plan-check 規則:必有 Global Constraints 節;每 task 必有 `interfaces:` 與 `test:` 行;task 編號 T1..Tn 連續;至少一個未勾 task 才可 run。缺 `### Acceptance operation` 且非 docs-only 者,plan-check 僅提示(非阻斷);run 的操作驗收階段才強制(見 logical 狀態機)。

## 2. autopilot_policy.json

```json
{
  "defaults": {
    "low":    {"confirm_gate": "auto",    "task_review": "auto", "acceptance": "auto",             "pr": "auto", "merge": "auto"},
    "medium": {"confirm_gate": "confirm", "task_review": "auto", "acceptance": "auto",             "pr": "auto", "merge": "auto"},
    "high":   {"confirm_gate": "halt",    "task_review": "auto", "acceptance": "halt_independent", "pr": "auto", "merge": "halt"}
  },
  "permanent_halts": ["irreversible-delete", "payments", "prod-migration", "security-boundary"],
  "preauthorizable": ["medium.confirm_gate"]
}
```

值域:`auto`(不停)/`confirm`(停一次要人確認;可被 knowledge 預授權 directive 覆蓋為 auto)/`halt`(必停人)/`halt_independent`(必停且驗收者≠實作者)。`permanent_halts` 為硬清單:runner 讀到即 halt,任何設定不可移除或放寬。

## 3. task-review 判定行(reviewer 輸出契約)

```
[task-review] T<n> | spec: pass|fail|cannot-verify | quality: pass|fail | <一句理由>
```

`cannot-verify`=需求落在本 task diff 之外(合法判定,不算 fail);任一 fail → 回修一次 → 再 fail 則 halt(exit 3)。末端整支 review 同格式,`T<n>` 改為 `branch`。

## 4. live handshake 檔(docs/worklog/handshake-autopilot.md)

```
branch/role/scope: <branch> / autopilot / <CHG-id>
doing: CHG-<id> task T<n>/<m>
next: <一行>
last-updated: YYYY-MM-DD HH:MM (UTC+0)
```

## 5. 落帳對應(全部沿用 ai-sdlc v1.17 格式,無新帳本)
| autopilot 產物 | 落點 |
|----------------|------|
| 計畫 | 目標專案 CHG 修改指引段 |
| task-review 判定行 | ACC 查核明細「證據」欄 |
| 施工錯誤/根因 | docs/knowledge/(error 條目) |
| 停點事件 | worklog 一行 + handshake 檔 |
| 每 task commit | `CHG-<id>: T<n> <標題>` |
