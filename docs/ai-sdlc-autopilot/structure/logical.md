# 邏輯結構 — ai-sdlc-autopilot

- 專案:ai-skills / skill: ai-sdlc-autopilot
- 版本:v1.0 | 日期:2026-07-06(UTC+0)

## 三層架構與相依方向

```
使用者需求
   │
   ▼
┌─ 治理層 = ai-sdlc v1.17+(外部相依,只讀)─────────────┐
│ handshake·CHG/ACC·風險分級·審議會·knowledge·lint    │
└──────────────△───────────────────────────────────────┘
               │ 單向唯讀引用(autopilot 永不修改 ai-sdlc)
┌─ 執行層 = references ────────────────────────────────┐
│ execution-plan → tdd-loop ⇄ systematic-debugging     │
│                → task-review(每 task + 末端整支)     │
└──────────────△───────────────────────────────────────┘
               │ 契約(格式與判定行)
┌─ 驅動層 = autopilot-loop + policy + runner ──────────┐
│ 狀態機:握手→CHG(plan-check)→[T_i:施工→測→review→   │
│ 勾+commit]→整支 review→ACC→PR→(policy)merge→收尾   │
└───────────────────────────────────────────────────────┘
```

## 停點決策順序(嚴格、只准加嚴)
1. **永遠停點**:task 或 CHG 帶 `permanent-halt:<類別>` 標記 → 無條件 halt(policy 不可放寬,runner 硬拒)
2. CHG 標頭 `Autonomy:` 欄(只准比 policy 嚴)
3. `autopilot_policy.json` 風險×階段矩陣
4. 查無 → 保守 halt

## Runner exit code 契約(供 CI/cron 接線)
| code | 意義 | 外層動作 |
|------|------|----------|
| 0 | 全程完成(或該階段完成) | 收下一單 |
| 1 | 非預期錯誤 | 告警,人看 |
| 2 | 計畫格式無效(plan-check) | 回修 CHG 計畫段 |
| 3 | 合法停點(確認閘/審議/永遠停點/merge 待人) | 通知人,帶停點原因 |

## 續作語意
checkbox 打勾=已完成 task(續作點);`docs/worklog/handshake-autopilot.md` 每 task 邊界更新(ai-sdlc v1.15 常駐握手)。中斷後重跑 `run`:跳過已勾 task,從首個未勾開始;工作樹對帳交給 ai-sdlc 進場握手。

## 與 Superpowers 的關係(方法論來源)
plan 的 Global Constraints/Interfaces 塊、單 reviewer 雙判定(合規+品質)與「diff 看不出」判定、末端整支 review、TDD/系統化除錯紀律——改寫自 obra/superpowers v6(MIT © 2025 Jesse Vincent,見 THIRD-PARTY-NOTICES)。差異:產物一律落 ai-sdlc 帳本(不建 docs/superpowers/ 平行帳本)、觸發靠 SKILL 偵測與 runner(不靠 harness hook)、停點由治理層風險分級驅動。
