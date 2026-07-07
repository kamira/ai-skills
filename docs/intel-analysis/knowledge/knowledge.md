# knowledge — intel-analysis(專案開始即建;空 INDEX 為合法知識庫)

## INDEX(讀這裡,不是整份檔)
| id | tier | tags/scope | 一句規則 | 狀態 |
|----|------|-----------|----------|------|
| KN-001 | shallow | plugin · migration | 新能力域以「skill+帳本+lint+plugin」四件套落地,建置複本由 build_suite 對照表統一同步 | 觀察中(seen 2 / applied 1) |
| KN-002 | shallow | discipline · automation | 紀律類規則的自動化採三段式:runner 出清單(機械)+人/agent 出判斷+帳本記結果(append-only) | 觀察中(seen 2 / applied 1) |

## KN-001 — 新能力域以「skill+帳本+lint+plugin」四件套落地
- tier:shallow
- 日期 / 分支:2026-07-07(UTC+0)/ claude/quirky-margulis-cad156
- tags/scope:plugin · migration
- 觸發證據:ai-sdlc-suite CHG-20260707-01(大補帖打包)、intel-analysis CHG-20260707-01(第 2 次同動機:打包成 plugin 發佈)
- 計數:seen 2 / applied 1 / last-applied 2026-07-07
- 狀態:觀察中

## KN-002 — 紀律類規則的自動化採三段式
- tier:shallow
- 日期 / 分支:2026-07-07(UTC+0)/ claude/quirky-margulis-cad156
- tags/scope:discipline · automation
- 規則:runner 出清單(確定性機械)+人/agent 出判斷(資訊與判讀)+帳本記結果(append-only)——機械件永不代行判斷,判斷永不吃掉記錄
- 觸發證據:ai-sdlc-autopilot CHG-20260706-01(施工紀律 runner 化)、intel-analysis CHG-20260707-02(盤點紀律 runner 化;使用者明定資訊自理)
- 計數:seen 2 / applied 1 / last-applied 2026-07-07
- 狀態:觀察中
