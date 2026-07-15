# AI Guideline — ai-sdlc-autopilot(受治理的自動駕駛執行層)

- 專案:ai-skills / skill: ai-sdlc-autopilot
- 分支(Branch):claude/quirky-margulis-cad156
- 版本:v1.0
- 日期:2026-07-06
- 狀態:已確認(使用者於 2026-07-06 三項決策:新橋接 skill / 風險分級自動 / 一次做完整)

## 1. 背景與目標

ai-sdlc(v1.17)解決「所有變更如何被治理」——帳本、閘門、驗收、知識庫;但它不規定「一筆變更怎麼施工」,也沒有把「需求→merge」自動跑完的驅動件。Superpowers(obra,MIT)反之:施工方法論成熟(plan 格式、每-task review、TDD、worktree 流程)但無治理帳本、靠 harness hook 綁定平台。

目標:建立橋接 skill **ai-sdlc-autopilot**,吸收 Superpowers 的執行方法論(MIT 改寫、含出處聲明)、以 ai-sdlc 為強制治理層,加上驅動層(契約+runner),讓一筆需求能在風險分級的停點策略下**自動化完成**:需求 → CHG → 逐 task 施工(TDD+唯讀 review)→ ACC → commit → PR →(依風險)merge,每一步自動落帳。

成功定義:低風險白名單變更可零人工跑完並留下完整 CHG/ACC/knowledge 記錄;中風險僅停一次確認閘;高風險/永遠停點絕不代行。

## 2. 範圍

### 納入
- 執行層 references(雙語):execution-plan(計畫格式)、tdd-loop、task-review、systematic-debugging、autopilot-loop(驅動契約)
- 驅動層:`assets/autopilot_policy.json`(風險×階段停點矩陣)+ `scripts/autopilot_runner.py`(plan-check / run / status;headless agent 指令可設定)
- 與 ai-sdlc 的硬相依:進場先握手、修改先 CHG、驗收同輪、knowledge 落帳——autopilot 不另立平行帳本
- evals、dist 打包(en/zh-tw 兩包)、README 收錄

### 不納入(明確排除)
- 不 fork/不內嵌 Superpowers 程式碼(僅方法論改寫+出處);不裝其 hook 生態
- 不修改 ai-sdlc 本體(治理層照用 v1.17 契約)
- CI/cron 排程接線(runner 預留 exit code 契約,接線屬使用者環境)
- 多 repo 自動駕駛(先單 repo;跨 repo 沿用 ai-sdlc cross-repo 人工節奏)

## 3. 利害關係人
| 角色 | 關注點 |
|------|--------|
| 使用者(專案擁有者) | 自動化省工但不失控;帳本完整可稽核;高風險絕不代行 |
| 執行 agent(任何廠牌) | 契約可讀、續作點明確(checkbox+live handshake)、停點可查詢 |
| ai-sdlc 治理層 | autopilot 產物落入既有 CHG/ACC/knowledge 格式,lint 可驗 |

## 4. 功能需求
| 編號 | 需求 | 優先級 | 備註 |
|------|------|------|------|
| FR-1 | 計畫格式:CHG 修改指引強化為 Global Constraints + 逐 task Interfaces + test 行 + checkbox | P0 | 單一帳本:plan 就在 CHG 裡,不另立檔 |
| FR-2 | 逐 task 迴圈:施工(TDD)→ 測試 → 唯讀 task-review(單 reviewer 雙判定:合規+品質)→ 打勾 → commit | P0 | review 不改工作樹;「diff 看不出」是合法判定 |
| FR-3 | 風險分級停點:低=全自動到 merge;中=確認閘停一次(可預授權)後自動;高=審議/獨立驗收/merge 必停人;永遠停點永不自動 | P0 | 矩陣在 autopilot_policy.json,只准加嚴 |
| FR-4 | runner:plan-check(機器驗計畫格式)/ run(驅動 headless agent 逐 task)/ status;exit code 契約(0 完成/1 錯誤/2 計畫無效/3 合法停點) | P0 | agent 指令模板可設定(claude/codex/任意);--dry-run 可測 |
| FR-5 | 續作點:checkbox 打勾 + live handshake 檔(docs/worklog/handshake-autopilot.md)每 task 邊界更新 | P0 | 沿用 ai-sdlc v1.15 常駐握手 |
| FR-6 | 收尾自動落帳:ACC 產出(task-review 記錄為證據)、CHG 重複性檢查欄、錯誤入 knowledge | P0 | 全走 ai-sdlc v1.17 格式,lint 可驗 |
| FR-7 | 末端整支 review:所有 task 完成後,對整個 branch diff 做一次總 review 再進 ACC | P1 | 取自 Superpowers v6 whole-branch review |
| FR-8 | systematic-debugging:測試連續失敗時的假說→驗證迴圈,根因入 knowledge | P1 | 取代盲目重試 |
| FR-9 | 實際操作驗收(operational_verify):整支 review 後、ACC 前把變更真的跑一次(operate/observe/pass);程式 CHG 缺操作測試不得抵達 ACC;docs-only 可豁免;高風險人執行 | P0 | v1.1.0;task 測試=單元/build,操作驗收=整支末端實跑 |

## 5. 非功能需求
| 類別 | 要求 |
|------|------|
| 平台中立 | 契約=純 markdown+JSON;runner=Python 3 標準庫,agent 指令外部化 |
| 可稽核 | 每 task 一 commit(帶 CHG 編號);review 判決留檔;停點事件寫 worklog |
| 安全 | 永遠停點清單硬編入 policy 且 runner 拒絕覆寫放寬;secrets 不入任何產物(沿用 doc-integrity 掃描) |
| 可維護性 | 雙語成對(bilingual_check 可驗);runner 單檔 <400 行 |
| 相容性 | 依賴 ai-sdlc ≥ v1.17(Skill 版本自檢);MIT 出處聲明(Superpowers © 2025 Jesse Vincent) |

## 6. 限制與假設
- 限制:runner 不內建 LLM——它是狀態機與裁判,施工與 review 由外部 agent 指令執行
- 限制:merge 自動化依賴 gh CLI;無 gh 時降級為印出指令並以停點結束
- 假設:目標 repo 已受 ai-sdlc 治理(有 docs/changes/ 與 root 進入點);未治理 repo 先走 ai-sdlc 進場
- 待確認:無(三項關鍵決策已由使用者確認)

## 7. 驗收條件
- [ ] AC-1 plan-check 對「缺 Global Constraints / task 缺 interfaces 或 test 行」的計畫 exit 2 並指出缺項;合規計畫 exit 0
- [ ] AC-2 --dry-run 全跑:低風險 CHG 從首 task 到「merge 階段」全自動不停;中風險在確認閘 exit 3;高風險在審議點 exit 3
- [ ] AC-3 中斷續作:模擬跑到 T2 中斷,重跑後從 T3 開始(checkbox 為續作點),live handshake 檔內容為最新
- [ ] AC-4 每 task 產生一個帶 CHG 編號的 commit(dry-run 以 --no-commit 模擬時,輸出等效訊息)
- [ ] AC-5 永遠停點:CHG 含永遠停點標記時,任何風險等級都在該步 exit 3,policy 無法放寬
- [ ] AC-6 bilingual_check --skill-dir skills/ai-sdlc-autopilot 全對平行;py_compile runner OK;evals JSON valid
- [ ] AC-7 出處聲明存在(SKILL.md NOTICE 節+THIRD-PARTY-NOTICES.md);README 收錄新 skill;dist 兩包重建

## 8. AI 開發約定
- 治理文件在 `docs/ai-sdlc-autopilot/`(本 repo 慣例:治理記錄依 skill 分目錄);knowledge 已隨本 Guideline 同步建立(先建規則)
- 任何後續修改走 ai-sdlc modification-guide(CHG→ACC 同輪);commit message 帶 CHG 編號;UTC+0
- 雙語成對:`.md` 英 / `.zh-tw.md` 繁中;結構平行
- 本 skill 對 ai-sdlc 只讀不寫:引用其 references 與 scripts,不修改之
