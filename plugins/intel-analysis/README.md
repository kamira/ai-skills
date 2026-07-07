# intel-analysis — 情報分析方法論大補帖

把 Notion「SKILL Manager|分析方法論技能總管理」保真遷移為可安裝 plugin:**從利益到行動的十步驟框架**(SKILL-01〜12 核心流程 + SKILL-13〜20 擴展模組)、**23 條核心紀律**、**檔案化預測驗證帳本**(版本鏈快照、Brier 校準)。繁中先行,英文版列 backlog。

## 安裝(Claude Code)

```
/plugin marketplace add kamira/ai-skills
/plugin install intel-analysis@ai-skills
```

## 內容物

| 元件 | 路徑 | 說明 |
|------|------|------|
| SKILL.md | `skills/intel-analysis/` | orchestrator:三流程(快情報/慢情報/追蹤循環)+ 20 skill 偵測表 + 23 紀律索引(複本;單一真相在 repo 頂層 `skills/`) |
| references ×22 | `skills/intel-analysis/references/` | skill-01〜20 + disciplines(紀律全文)+ prediction-ledger(帳本規範) |
| 預測帳本 schema | `skills/intel-analysis/assets/` | prediction_entry.schema.json + estimative_language.json(措辭↔機率表) |
| 帳本工具 | `skills/intel-analysis/scripts/` | `prediction_lint.py`(fail-loud 鏈驗證+INDEX 生成)/`brier_report.py`(Brier+措辭對表+漂移清單) |

## 預測驗證帳本(檔案化版本鏈)

預測落在**目標專案** `docs/intel/predictions/`,一鏈版本一 JSON 快照(`P-YYYY-MMDD-NN[-vK].json`):歷史快照不可覆蓋、每鏈單一 latest、v2+ 必附 version_note。

```
python3 skills/intel-analysis/scripts/prediction_lint.py --repo .          # 鏈驗證(可接 pre-commit/CI)
python3 skills/intel-analysis/scripts/prediction_lint.py --repo . --index  # 重生 INDEX.md
python3 skills/intel-analysis/scripts/brier_report.py --repo .             # Brier 校準報告
```

## 與 ai-sdlc-suite 的關係

獨立領域、獨立安裝——情報分析不相依開發治理。若同時安裝,knowledge/預測帳本互不干涉(各自目錄)。每日自動盤點(紀律 19〜23 的 runner 化)為後續版本規劃。

## 來源與正典

自 Notion 2026-07-07 快照保真遷移;遷移後**以本 repo 為正典**,Notion 原頁轉唯讀查閱。既有 Notion 預測資料庫保留查閱,新預測鏈一律落檔案帳本。
