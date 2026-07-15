# Changelog — ai-sdlc-autopilot

本檔記錄 `ai-sdlc-autopilot` skill 的版本變更。格式參考 Keep a Changelog;tag 採 skill 範圍 `ai-sdlc-autopilot-vX.Y.Z`。版本號寫於 `skills/ai-sdlc-autopilot/SKILL.md` 的 `metadata.version`。

## [1.1.0] — 2026-07-15

實際操作驗收閘(見 `docs/ai-sdlc-autopilot/changes/CHG-20260715-01.md`;使用者:最終測試不能只有傳統 code 測試,要有實際操作測試)。

### Added
- **operational_verify 階段**:插在整支 review 與 ACC 之間——把變更真的跑一次(operate/observe/pass)。task 級 `test:` 是單元/build(RED-GREEN,證明零件對),不證明變更真的跑起來;此階段補上「最後一哩」實跑證據。
- **計畫格式加 `### Acceptance operation`**(operate/observe/pass):程式類 CHG 必附;純文件以 `Acceptance-operation: n/a (docs-only)` 一行豁免。
- **runner `--verify-cmd`**:低/中風險可自動跑操作測試(非零→exit 3);無 verify-cmd 則人在迴圈(印簡報後 exit 3);高風險 operational_verify=halt(永遠人執行,機器不自證);dry-run 模擬通過。
- **機械閘門**:程式 CHG 既無 `### Acceptance operation` 也無 docs-only 標記→在操作驗收階段 exit 3,不得抵達 ACC。plan-check 僅提示(非阻斷),不影響 CI 與既有 CHG。
- policy 三風險加 operational_verify(低/中 auto、高 halt);SKILL loop 圖與停點表加欄(×2 語言)。

## [1.0.0] — 2026-07-07

首發:受治理的自動駕駛執行層(見 `docs/ai-sdlc-autopilot/changes/CHG-20260706-01.md`)。

### Added
- **三層架構**:治理層=ai-sdlc(≥v1.17,唯讀硬相依)/ 執行層=5 份雙語 references(execution-plan、tdd-loop、task-review、systematic-debugging、autopilot-loop)/ 驅動層=autopilot_policy.json + autopilot_runner.py。
- **計畫格式**:全域約束+逐 task interfaces/test 行+checkbox,寫在目標專案 CHG 內(單一帳本);plan-check 機器閘。
- **逐 task 迴圈**:TDD(紅綠重構)→ 測試 → 唯讀 task review(單 reviewer 雙判定:spec+quality,含 cannot-verify)→ 打勾+帶 CHG 編號 commit → live handshake;一次回修、二敗即停;末端整支 review。
- **風險分級停點**:低=全自動到 merge、中=確認閘一次(可預授權)、高=審議/獨立驗收/merge 必停;**永遠停點硬編碼**(不可逆刪除/金流/生產遷移/安全邊界),任何設定不可放寬;決策順序=永遠停點→CHG Autonomy(只准加嚴)→policy 矩陣→查無即停。
- **runner**:plan-check / run / status;--dry-run 可全測狀態機;exit 0/1/2/3 契約供 cron/CI 接線;無 agent/無 gh 均有降級模式。
- 方法論改寫自 Superpowers v6(obra,MIT © 2025 Jesse Vincent;見 THIRD-PARTY-NOTICES)。
