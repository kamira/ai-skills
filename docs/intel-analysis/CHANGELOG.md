# Changelog — intel-analysis

本檔記錄 `intel-analysis` skill 的版本變更。格式參考 Keep a Changelog;tag 採 skill 範圍 `intel-analysis-vX.Y.Z`。版本號寫於 `skills/intel-analysis/SKILL.md` 的 `metadata.version`。

## [1.1.0] — 2026-07-07

業界規範對齊(見 `docs/intel-analysis/changes/CHG-20260707-03.md`;對照審視:ICD 203 九項工藝標準+SAT 技法)。

### Changed
- **評級標度升級為 Admiralty/NATO 標準 A–F × 1–6**(SKILL-03):新增 F(來源無法判斷——新來源預設格位)與 6(真偽無法判斷≠假);附 v1.0 舊制(A–D×1–4)對照表,歷史標記依表讀、不回頭重寫;下游規則同步(SKILL-03 處置/交叉驗證、SKILL-10 情報池規則與模板、disciplines 遷移註)。

### Added
- **欺騙偵測四框架 MOM/POP/MOSES/EVE**(SKILL-03):對手主動欺騙情境的結構化評估——動機/機會/手段、過往欺騙實踐、來源易感性、證據評估;≥2 框架指向欺騙即降級,確認欺騙做反向情報價值分析。
- **關鍵判斷來源附錄**(SKILL-11,對齊 ICD 206):每個核心判斷附支撐來源清單(源類型+評級+日期);[F-6] 不得為唯一支撐;附錄與正文分離供獨立稽核。
- SKILL.md「標準對齊」聲明節。

## [1.0.0] — 2026-07-07

首發:Notion「SKILL Manager|分析方法論技能總管理」保真遷移(見 `docs/intel-analysis/changes/CHG-20260707-01.md`)+每日盤點 runner 帳本側(`CHG-20260707-02.md`)。

### Added
- SKILL.md orchestrator(快情報/慢情報/追蹤循環三流程+20 skill 偵測表)+ references ×23(skill-01〜20+disciplines 23 條紀律全文+prediction-ledger+daily-loop)。
- 檔案化預測驗證帳本:一鏈版本一 JSON 快照(P-YYYY-MMDD-NN[-vK]),歷史不可覆蓋、每鏈單一 latest;`prediction_lint.py`(fail-loud+INDEX 生成)、`brier_report.py`(Brier+措辭對表+漂移清單)、`intel_daily.py`(每日盤點帳本側;資訊獲取由使用者自理)。
- plugin `intel-analysis`(marketplace 第二筆)。
