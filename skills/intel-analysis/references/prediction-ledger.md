---
name: prediction-ledger
description: >
  預測驗證帳本版本化機制(檔案化):一鏈版本一 JSON 快照,歷史快照不可覆蓋、每鏈單一 latest,
  以 chain_root 串接版本鏈供 Brier 校準。SKILL-09 登錄預測、SKILL-10 觀測更新、SKILL-12
  回測、每日鏈覆蓋盤點(紀律 19-23)時讀本檔。含 Notion 中文欄名↔JSON 英文鍵對照。
---

# prediction-ledger — 預測驗證帳本(版本鏈快照)

> **核心原則:歷史快照不可被覆蓋。** 每條預測都是一條「版本鏈」,由 `chain_root`(原始預測 ID)串接。新訊號出現時不修改舊快照,而是新建一個快照檔、將舊快照標記為「已被取代」。此機制保留每一期的判斷供 Brier Score 與校準回測使用。

## 存放位置與檔式

目標專案 `docs/intel/predictions/` 下,**一鏈版本一 JSON 檔**,檔名=快照 id:

```
docs/intel/predictions/
├── INDEX.md                    # 生成物(prediction_lint.py --index),永不手改
├── P-2026-0520-03.json         # 首發快照(版本 1)
├── P-2026-0520-03-v2.json      # 同鏈第 2 版快照
└── archive/                    # 已驗證/已失效鏈可歸檔(選用)
```

選 JSON 同 knowledge 拆檔理由:解析是二值的——成功,或大聲失敗;git 可合併、AI 直讀、diff 可審計。

## ID 命名規則

- **首發**:`P-YYYY-MMDD-NN`(如 `P-2026-0520-03`)
- **後續版本**:`原 ID + -v{版本序}`(如 `P-2026-0519-03-v2`、`-v3`…)。後綴版本號永遠對齊 `version_seq`

## 欄位(JSON 英文鍵 ↔ Notion 原欄名對照)

| JSON 鍵 | Notion 原欄名 | 說明 |
|---------|---------------|------|
| `id` | 預測 ID | =檔名;首發 `P-YYYY-MMDD-NN`,後續 `-vK` |
| `chain_root` | 原始預測 ID | 本鏈首發 ID;同鏈所有版本共用;首發=自己的 id |
| `prev_id` | 前版 ID | 直接上一版的 id;第 1 版為 null |
| `version_seq` | 版本序 | 首發為 1,每次快照 +1 |
| `version_status` | 版本狀態 | `latest` / `superseded` / `verified` / `invalidated`(最新/已被取代/已驗證/已失效)。**同一鏈任一時刻僅一個 latest 或終態** |
| `version_note` | 版本說明 | 建立此快照的觸發訊號/調整理由(一句話);**v≥2 必填**(紀律 18 敘事漂移檢測) |
| `tracking_status` | 追蹤狀態 | `active` / `observing` / `dormant` / `verified` / `invalidated`(進行中/觀察中/休眠/已驗證/已失效) |
| `statement` | 預測內容 | 情境描述(可測試措辭) |
| `probability` | 機率 | 整數 %,**5% 步進**(紀律 6);措辭衝突時以 % 為準(紀律 16) |
| `wording` | 機率措辭 | 選填:幾乎確定/很可能/可能/兩可/不太可能/很不可能/幾乎不可能(對表見 assets/estimative_language.json) |
| `key_assumptions` | 關鍵假設 | 陣列;每條須通過可證偽自檢(紀律 14) |
| `triggers` | 觸發條件 | 陣列;哪些訊號出現代表正在走向此情境 |
| `indicators` | 觀測指標 | 陣列;SKILL-10 驗證用 |
| `window` | 驗證視窗 | `{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}` |
| `source_analysis` | 來源分析 | 建立此快照的分析文章/CHG 引用 |
| `outcome` | 實際結果 | 驗證時填:`{"result": "...", "value": 0 或 1, "calibration_note": "..."}` |
| `tags` / `actors` | (主題/行為者) | 陣列,小寫檢索鍵;鏈覆蓋盤點(紀律 19)與戰區掃描(紀律 22)的命中軸 |

## 操作流程

1. **首發**:建新檔。`chain_root = id`;`version_seq = 1`;`version_status = "latest"`;`prev_id = null`。
2. **更新(既有預測有新訊號)**:
   1. **新建一個快照檔**(**禁止編輯既有檔**)。`id` 採後綴版本號;`chain_root =` 鏈根;`prev_id =` 上一版 id;`version_seq =` 上一版 +1;`version_status = "latest"`;`source_analysis =` 當日分析;`version_note =` 一句話理由。
   2. **將上一版** `version_status` 由 `latest` 改為 `superseded`(唯一允許動舊檔的欄位——僅此欄、僅此值)。
3. **驗證**:在 latest 版填 `outcome`,`version_status` 改 `verified`、`tracking_status` 改 `verified`。歷史快照保留 `superseded` 不動。
4. **廢棄**:預測前提被根本否定時,latest 版 `version_status` 改 `invalidated`。

## SKILL-12 校準引用方式

- 校準回測以 `chain_root` 為鏈索引,取**鏈中最後一個非取代版本**(通常為 `verified`)的機率與實際結果計算 Brier Score(`brier_report.py` 自動化)。
- 「敘事漂移檢測」檢查同一鏈各版本機率變動是否都有 `version_note` 支撐,無說明的版本視為不合規(lint 對 v≥2 強制)。
- 對比與修正段落(時局分析)以 `chain_root` 串接整鏈,呈現完整 v1 → v2 → … → latest 的演變。

## 機器輔助

```
python3 scripts/prediction_lint.py --repo .            # fail-loud:缺欄/enum 錯/id≠檔名/斷鏈/多 latest/機率非 5% 步進/v2+ 缺 note → 擋
python3 scripts/prediction_lint.py --repo . --index    # 重生 INDEX.md;--check 驗新鮮度
python3 scripts/brier_report.py --repo .               # Brier+措辭對表(紀律 16)+漂移清單(紀律 18)
```
