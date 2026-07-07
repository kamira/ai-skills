# AI Guideline — intel-analysis(情報分析方法論 skill 化)

- 專案:ai-skills / skill: intel-analysis
- 分支(Branch):claude/quirky-margulis-cad156
- 版本:v1.0
- 日期:2026-07-07
- 狀態:已確認(使用者四決策:檔案化帳本/繁中先行/同 repo 新 plugin/核心+腳本全包)

## 1. 背景與目標

使用者在 Notion 維護一套成熟的情報分析方法論:「SKILL Manager 總管理」+ SKILL-01〜20 子技能 + 23 條核心紀律 + 預測驗證資料庫(版本鏈快照機制)。目標:遷移打包為本 repo 的 **intel-analysis skill**(Superpowers 式大補帖第二個 plugin),預測帳本檔案化(一鏈一 JSON 快照,同 knowledge 拆檔哲學),附 lint 與 Brier 回測腳本。**內容遷移以保真為先——紀律與模板逐字保留,不摘要、不改寫語意。**

## 2. 範圍

### 納入
- `skills/intel-analysis/`:SKILL.md(orchestrator:三流程+偵測表+23 紀律索引)+ references(SKILL-01〜20 遷移 + disciplines 紀律全文 + prediction-ledger 帳本規範)
- 預測帳本規格:目標專案 `docs/intel/predictions/` 一鏈版本一 JSON;`assets/prediction_entry.schema.json` + `assets/estimative_language.json`(紀律 16 措辭↔機率表)
- `scripts/prediction_lint.py`(fail-loud 鏈驗證+INDEX 生成)+ `scripts/brier_report.py`(SKILL-12 校準回測)
- plugin:`plugins/intel-analysis/`(同 marketplace 第二個 plugin);`build_suite.py` 通用化為多 plugin 同步(屬 ai-sdlc-suite 專案之跨專案修改,該帳本另記 CHG-lite)
- 本 repo README 收錄

### 不納入(明確排除)
- 每日情報 autopilot runner(紀律 19〜23 狀態機)——留下一輪
- Notion 既有預測資料的批次遷移腳本(帳本從零起鏈;歷史鏈留 Notion 查閱)
- 英文版 references(繁中先行;英文版列 backlog)——**單語例外**:本 skill 暫不納 bilingual 檢查,README/CHG 註明
- OSINT 資料來源索引頁(工具/來源易變,留 Notion)

## 3. 利害關係人
| 角色 | 關注點 |
|------|--------|
| 使用者(分析者) | 方法論保真;預測鏈可稽核可回測;任何 agent 可載入 |
| 執行 agent | 快/慢/追蹤三流程可路由;紀律可查;帳本格式機器可驗 |
| 未來的每日 autopilot | 鏈狀態機器可讀(version_status/tracking_status/window) |

## 4. 功能需求
| 編號 | 需求 | 優先級 | 備註 |
|------|------|------|------|
| FR-1 | SKILL.md orchestrator:快情報/慢情報/追蹤循環三流程 + 20 skill 偵測表 + 23 紀律一行索引 | P0 | 紀律全文在 references/disciplines.md |
| FR-2 | SKILL-01〜20 逐頁遷移為 references(保真轉檔,Notion 表格/模板/callout 轉 markdown) | P0 | 繁中;檔名 skill-01-problem-definition.md 式 |
| FR-3 | 預測帳本:一鏈版本一 JSON(`P-YYYY-MMDD-NN[-vK].json`),欄位小寫英文鍵;快照不可覆蓋、每鏈單一 latest;INDEX 生成物 | P0 | schema 必填 id/chain_root/version_seq/version_status/statement/probability |
| FR-4 | prediction_lint.py:解析失敗/缺欄/enum 錯/id≠檔名/鏈斷鏈/多 latest/機率非 5% 步進/v≥2 缺 version_note → 擋;--index 重生 INDEX.md | P0 | fail-loud,同 knowledge lint 哲學 |
| FR-5 | brier_report.py:已驗證鏈 Brier 分數、措辭↔機率對表(紀律 16)、無說明版本清單(敘事漂移,紀律 18) | P0 | 報告非閘門 |
| FR-6 | plugin 打包:plugins/intel-analysis + marketplace 第二筆;build_suite 多 plugin 化 | P0 | 跨專案部分記 suite 帳本 |

## 5. 非功能需求
| 類別 | 要求 |
|------|------|
| 保真 | 遷移不得摘要或改寫紀律語意;逐頁對照 Notion 原文 |
| 平台中立 | 純 markdown+JSON+Python stdlib;不相依 Notion(來源引用除外) |
| AI-friendly | JSON 鍵小寫英文;機率整數 %;enum 固定值域 |
| 可稽核 | 快照 append-only,git diff 可審;INDEX 生成物永不手改 |

## 6. 限制與假設
- 假設:Notion 頁面結構如 2026-07-07 快照;遷移以當日內容為準
- 限制:單語(繁中)先行,bilingual 檢查暫豁免本 skill
- 待確認:無

## 7. 驗收條件
- [ ] AC-1 references 20 份齊全,SKILL-04/-09/-10 抽查與 Notion 原文逐段對照無語意損失
- [ ] AC-2 prediction_lint 雙向:合法鏈(首發+v2)exit 0;壞鏈(多 latest/斷 prev/機率 7%/v2 缺說明)各自被擋且訊息指出原因
- [ ] AC-3 brier_report 對合成已驗證鏈算出正確 Brier(手算對照);措辭不符表列出
- [ ] AC-4 INDEX 生成/--check 新鮮度;檔名=id lint
- [ ] AC-5 plugin 安裝面:marketplace 兩 plugin JSON valid;build_suite --check 對兩 plugin 皆過;py_compile/JSON 全綠;核心既有 skill 零改動
- [ ] AC-6 23 條紀律全文在 disciplines.md 逐條在(含 11/12/19-23 長文),SKILL.md 索引 23 行俱全

## 8. AI 開發約定
- 治理文件在 `docs/intel-analysis/`;knowledge 隨本 Guideline 同步建立
- 後續修改走 modification-guide;commit 帶 `intel-analysis CHG-…` 前綴;UTC+0
- 措辭↔機率、版本鏈規則以 Notion 總管理頁 2026-07-07 版為正典來源(遷移後以 repo 為準)
