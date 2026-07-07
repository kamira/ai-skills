---
name: daily-loop
description: >
  每日盤點驅動契約(紀律 19-23 的帳本側機械化):intel_daily.py 產出「該盤哪些鏈、誰進/
  過驗證視窗、誰是冷鏈候選」,你自備資料源做命中查證與判讀,再以 A/B/C/D 處置記錄回帳本。
  資訊獲取由使用者自理,runner 零搜尋零網路。每日分析開始前讀本檔。
---

# daily-loop — 每日盤點驅動契約

## 分工邊界(先講清楚)

> **資訊獲取由使用者自理。** runner 不呼叫任何搜尋、不抓任何資料、不碰網路——它只是帳本的狀態機與記錄員。紀律 19(c) 的定向查證、紀律 22 的戰區掃描,**「查什麼」由 runner 列出,「去查」與「判讀」是你(或你指派的 agent)用自己的來源完成**。

| 誰 | 做什麼 |
|----|--------|
| **runner(機械)** | 盤點清單(該覆蓋的鏈+命中關鍵詞)、視窗到期/即將到期清單(紀律 23)、真空偵測(紀律 20)、冷鏈候選計算(紀律 21)、處置結果記錄(append-only) |
| **使用者(判斷)** | 用自備來源做命中比對與查證(紀律 19c 三級:一致/不足/反向)、決定 A/B/C/D 處置、建快照/結案、確認冷鏈降階與喚醒 |

## 每日迴圈

```
1. python3 scripts/intel_daily.py brief --repo .
      → 當日簡報:待覆蓋鏈(含 tags/actors/indicators 作為你的查證關鍵詞)
                  + 視窗到期待結案清單 + 冷鏈候選 + 休眠鏈關鍵詞(供喚醒比對)
2. 你用自己的資料源逐鏈查證(runner 不參與)
3. 依判讀處置:
      - 建快照/改機率 → 依 prediction-ledger 操作流程(新快照,舊版改 superseded)
      - 結案 → 在 latest 填 outcome、改 verified/invalidated
4. python3 scripts/intel_daily.py log --repo . --chain P-… --outcome A|B|C|D [--note "…"]
      → 記入當日 coverage 檔(每鏈一筆;零命中鏈不得無聲延續——A 也要記)
5. python3 scripts/prediction_lint.py --repo . --index   # 帳本驗證+INDEX 重生
```

## 四類處置(紀律 19d,逐鏈必記其一)

| 代碼 | 含義 | 帳本動作 |
|------|------|----------|
| **A** | 真無訊號 | 不建快照;log 記 A(「前期鏈本日覆蓋自檢」的明文依據) |
| **B** | 漏收訊號(你的查證有結果) | 建快照,version_note 註「定向查證補入」;log 記 B |
| **C** | 間接訊號 | 建快照並註明間接來源;log 記 C |
| **D** | 視窗到期真空 | 不建快照;走紀律 20(延續性估計,SKILL-11 明文標註);log 記 D |

查證反向(被否證)→ 按否證處理(不建正向快照;視情況 invalidated),log 記 B 並註明反向。

## 冷鏈規則(紀律 21 的機械化)

- **計數**:runner 讀最近 3 個 coverage 檔;某鏈連續 3 個分析日皆記 A → 列入**冷鏈候選**。
- **降階是你的決定**:確認後把該鏈 latest 的 `tracking_status` 改為 `dormant`(就地更新,見下)。
- **喚醒**:brief 會列出休眠鏈的關鍵詞;你的當日資料命中時,喚醒=當日重走 SKILL-04→09 並建快照,`version_note` 註「冷鏈喚醒:訊號 = …」。

## 就地更新 vs 新快照(重要區分)

- **內容/機率變更 → 一律新快照**(prediction-ledger 鐵律)。
- **營運狀態欄** — `tracking_status`(active/observing/dormant 轉換)與結案時的 `outcome`/`version_status`(latest→verified/invalidated)— **就地更新於 latest**(與 Notion 原機制一致:驗證在最新列填寫)。歷史快照(superseded)永不動。

## coverage 檔格式(`docs/intel/coverage/YYYY-MM-DD.json`)

一日一檔、append-only(當日重跑 log 會合併條目,同鏈以最後一筆為準):

```json
{
  "date": "2026-07-07",
  "entries": [
    {"chain": "P-2026-0520-03", "outcome": "A", "note": ""},
    {"chain": "P-2026-0601-01", "outcome": "B", "note": "定向查證補入:合成訊號"}
  ]
}
```

## exit codes

`0` 正常 | `1` 錯誤(帳本/參數) | `2` coverage 檔格式無效。無「合法停點」語意(判斷都在使用者側)。
