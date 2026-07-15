---
name: autopilot-loop
description: >
  驅動契約:從需求到 merge 的狀態機、停點決策順序(永遠停點 → CHG Autonomy → policy 矩陣 →
  查無=停)、續作語意、落帳對應、runner 指令與 exit codes。跑整條流程、續作中斷的執行、
  或把 runner 接進 cron/CI 時讀本檔。
---

# autopilot-loop — 驅動契約

> 語言 / Language: **繁體中文** · [English](autopilot-loop.md)

## 狀態機

```
ai-sdlc 進場握手(治理層——必經,含 knowledge INDEX + 未收尾 CHG 掃描)
  → CHG 存在且已確認?  否 → 先走需求/修改治理(ai-sdlc)
  → plan-check 閘(不過 exit 2——壞計畫永遠不開跑)
  → 確認閘            (依 policy:auto / confirm / halt)
  → [ 逐未勾 task T_i:
        TDD 施工 → task 測試 → 唯讀 task review
        → 過:打勾 + commit「CHG-<id>: T<i> <標題>」+ 更新 live handshake
        → 敗:一次回修 → 重審 → 第二次敗 = 停 ]
  → 整支 review
  → 實際操作驗收(真的跑起來:operate → observe → pass;依 policy)
  → 驗收(ACC;依 policy 自驗/獨立)
  → PR → merge(依 policy)→ 收尾:CHG 狀態 + Commit/PR + 重複性檢查 + knowledge
```

## 實際操作驗收——最後一哩(task 測試不夠)

逐 task 的 `test:` 是**單元/build 級**(RED-GREEN——零件對)。它**不證明**變更真的跑起來、真的被操作過——就是「全綠但功能還是壞的」盲區。驗收前 runner 要求一次**操作測試**:把 app/變更真的跑起來、操作它、觀察行為。

- 計畫在 **`### Acceptance operation`** 節宣告操作測試(`operate:` 怎麼跑/操作 / `observe:` 什麼確認可用 / `pass:` 通過標準)——見 execution-plan。
- runner 在此階段的行為:
  - 給了 `--verify-cmd C` 且階段為 `auto`(低/中):跑 `C`;非零 → 停(exit 3,「操作驗收失敗」)。
  - 無 `--verify-cmd`(且非 dry-run):印出 `### Acceptance operation` 簡報後停(exit 3)——**人在迴圈**:實際操作、記錄證據入 ACC,再續 merge。
  - 階段為 `halt`(高風險):**永遠由人執行**——高風險操作簽核不可機器自證,即使 `--verify-cmd` 通過也一樣。
  - `--dry-run`:模擬 operate/observe/pass。
- **docs-only 豁免**:CHG 宣告 `Acceptance-operation: n/a (docs-only)`(且無 `### Acceptance operation`)則略過此階段——純文件變更不逼造假操作。
- **程式類 CHG 既無 `### Acceptance operation` 也無 docs-only 標記→在此停(exit 3)**——程式變更沒有操作測試在案,不得抵達 ACC。

## 停點決策順序(嚴格、只准加嚴)

1. **永遠停點**——task 或 CHG 帶 `permanent-halt:<類別>` 標記(不可逆刪除/金流/生產遷移/安全邊界):無條件停;runner 拒絕任何放寬這些的設定。
2. **CHG `Autonomy:` 欄**——只准比 policy 更嚴。
3. **`assets/autopilot_policy.json`**——風險×階段矩陣。
4. **查無 → 停。** 契約認不得的關卡就停下來;猜「auto」正是自動駕駛出事的方式。

`confirm` 階段可經 knowledge directive 預授權(窄類別、闖禍自動失效)——ai-sdlc 的預授權規則,原樣沿用。

## 續作語意

已勾 checkbox=已完成 task;重跑 `run` 會跳過它們、從第一個未勾 task 繼續。live handshake 檔(`docs/worklog/handshake-autopilot.md`)在每個 task 邊界重寫——任一時刻中斷,檔案都是最新。重進場的工作樹對帳屬於 ai-sdlc 握手,不屬於 runner。

## Runner 指令與 exit codes

```
plan-check --chg <CHG.md>                      # 只驗計畫格式(操作測試提示為非阻斷)
run  --chg <CHG.md> --repo . [--agent-cmd T] [--test-cmd C] [--verify-cmd V] [--dry-run] [--no-commit] [--max-tasks N]
status --chg <CHG.md>                          # 已勾/未勾、下一個 task、當前階段
```

`--test-cmd` 跑每個 task 的單元/build 測試;`--verify-cmd` 跑末端操作測試(把變更真的操作一次)。Exit codes:`0` 完成 · `1` 非預期錯誤 · `2` 計畫無效 · `3` 合法停點(印出原因)。cron/CI 接 3(帶原因通知人)與 0(接下一筆 CHG)。`--dry-run` 模擬施工/測試/審查**與操作驗收**成功,不需 agent 即可演練狀態機與停點策略。

## 降級模式

- **無 headless agent**(未設 `--agent-cmd` 且非 dry-run):runner 印出每個 task 簡報後停(exit 3)——人在迴圈模式;勾選照樣驅動續作。
- **無 `--verify-cmd`**(且非 dry-run):runner 印出 `### Acceptance operation` 簡報後停(exit 3)——人執行操作測試並記錄證據入 ACC。
- **無 gh CLI**:PR/merge 階段印出該執行的指令後停(exit 3),不代行合併。
- **審查無法 spawn**:同一 agent 序列地施工再審查——在 ACC 註明降級(與 ai-sdlc 審議降級同規則)。
