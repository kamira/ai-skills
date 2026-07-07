---
name: ai-sdlc-autopilot
description: >
  建立在 ai-sdlc 之上的受治理自動駕駛執行層:把一筆已確認的需求自動做完——計畫(全域約束+
  逐 task 介面)→ 逐 task TDD 施工+唯讀 task review → 驗收 → commit → PR → merge——停點由
  ai-sdlc 風險分級驅動(低=全自動、中=一次確認閘、高/不可逆=必停人)。當使用者要「在治理下
  端到端自動完成一筆變更」、要 TDD/逐 task 審查紀律、或要跑 autopilot runner 時使用。
  硬相依 ai-sdlc skill(>= v1.17)作為治理層——先跑其進場握手。
metadata:
  version: 1.0.0
---

# ai-sdlc-autopilot — 受治理的自動駕駛執行

> 語言 / Language: **繁體中文** · [English](SKILL.md)

**一句話**:ai-sdlc 管帳本與閘門;本 skill 管施工與駕駛——需求進、一筆受治理/已審查/已測試/已合併的變更出,每一步自動落入 ai-sdlc 帳本。

三層:**治理**(ai-sdlc,外部相依、只讀)、**執行**(本 skill references:計畫格式、TDD、task review、除錯)、**驅動**(autopilot-loop 契約 + `assets/autopilot_policy.json` + `scripts/autopilot_runner.py`)。

## 硬相依:ai-sdlc 是治理層

- **先跑進場握手**(ai-sdlc handshake),動手前先 CHG,驗收同輪,knowledge 收尾——這些都不可選,也都不在本 skill 重複定義。
- 本 skill **只讀 ai-sdlc,永不修改它**。進場版本自檢:ai-sdlc >= v1.17(收尾自動化假設「重複性檢查欄+knowledge bootstrap」已存在)。
- **不建平行帳本**:計畫寫在目標專案的 CHG(修改指引段)、review 判定落 ACC 證據欄、錯誤入 `docs/knowledge/`。若發現自己在寫一個新的 docs 目錄,就是正在漂移。

## 偵測 → 載入

| 情境 | 線索 | 載入 |
|------|------|------|
| 撰寫/驗證可執行計畫 | 任務拆解、約束、介面、「幫我規劃」 | [`references/execution-plan.zh-tw.md`](references/execution-plan.zh-tw.md) |
| 施工一個 task | 實作、寫碼、紅綠、測試先行 | [`references/tdd-loop.zh-tw.md`](references/tdd-loop.zh-tw.md) |
| 某 task 的 diff 要判定 | 審這個 task、判決、規格合規 | [`references/task-review.zh-tw.md`](references/task-review.zh-tw.md) |
| 測試連續失敗 | 同一 task 連續 2+ 次失敗 | [`references/systematic-debugging.zh-tw.md`](references/systematic-debugging.zh-tw.md) |
| 跑整條流程/續作/接 CI | autopilot、端到端跑完、resume、停點策略 | [`references/autopilot-loop.zh-tw.md`](references/autopilot-loop.zh-tw.md) |

## 迴圈

```
ai-sdlc 握手 → CHG(plan-check 閘)
  → [ 逐 task:TDD 施工 → 測試 → 唯讀 task review → 打勾 + commit ]
  → 整支 review → ACC → PR →(依 policy)merge → knowledge 收尾
```

任一時刻中斷都安全:已勾 checkbox 是續作點,live handshake 檔(`docs/worklog/handshake-autopilot.md`)在每個 task 邊界更新。

## 停點策略(風險×階段——只准加嚴)

| 風險 | 確認閘 | task review | 驗收 | PR | merge |
|------|--------|-------------|------|----|-------|
| 低 | auto | auto | auto(自驗) | auto | auto |
| 中 | **confirm**(可預授權) | auto | auto | auto | auto |
| 高 | **halt** | auto | **halt**(獨立驗收者) | auto | **halt** |

**永遠停點**(永不自動、硬編碼、任何設定不可放寬):不可逆刪除、金流、生產資料遷移、安全邊界變更。決策順序:永遠停點 → CHG `Autonomy:` 欄(只准加嚴)→ policy 矩陣 → 查無=halt。

## Runner

```
python3 scripts/autopilot_runner.py plan-check --chg <CHG.md>
python3 scripts/autopilot_runner.py run --chg <CHG.md> --repo . \
    [--agent-cmd 'claude -p "$(cat {brief})"'] [--test-cmd 'pytest -q'] [--dry-run] [--no-commit]
python3 scripts/autopilot_runner.py status --chg <CHG.md>
```

runner **不含 LLM**:它是狀態機與裁判——施工與審查由你設定的任意 headless agent 指令執行。Exit codes:`0` 完成、`1` 非預期錯誤、`2` 計畫無效、`3` 合法停點(印出原因;cron/CI 據此接線)。

## 存放慣例

一切落入**目標專案**既有的 ai-sdlc 帳本——對應表見 [`docs/ai-sdlc-autopilot/structure/data.md`](../../docs/ai-sdlc-autopilot/structure/data.md)(計畫→CHG、判定→ACC 證據、根因→knowledge、每 task 一個帶 CHG 編號的 commit)。

## NOTICE(出處聲明)

本 skill 的執行方法論——計畫的全域約束/逐 task 介面塊、單 reviewer 雙判定(規格+品質)含合法的「diff 看不出」判定、末端整支 review、TDD/系統化除錯紀律——改寫自 **Superpowers**(Jesse Vincent/obra,MIT License,© 2025 Jesse Vincent)。見 [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md)。差異:產物落 ai-sdlc 帳本(不另立 plans/specs 目錄)、觸發靠 skill 偵測+runner(不靠 harness hook)、停點由治理層風險分級驅動。
