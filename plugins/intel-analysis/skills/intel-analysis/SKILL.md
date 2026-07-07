---
name: intel-analysis
description: >
  情報分析方法論(從利益到行動的十步驟框架):問題定義→事實建立→行為者分析→手段篩選→
  歸因校準→決策偏好→連鎖推演→情境預測→觀測指標→缺口聲明,加上可信度評級、預測校準回測
  與六個擴展模組(定量/敘事/制度/歷史類比/供應鏈/長期趨勢)。當使用者要做情報分析、地緣政治
  研判、行為者意圖分析、情境預測與機率評估、觀測指標追蹤、預測回測(Brier)、輿論敘事分析
  時使用。可單一 SKILL 呼叫、跑完整慢情報流程、或快情報精簡流程;預測一律登錄檔案化版本鏈
  帳本(docs/intel/predictions/)。繁中版;23 條核心紀律必遵。
metadata:
  version: 1.0.0
---

# intel-analysis — 分析方法論技能總管理

> 本 skill 自 Notion「SKILL Manager|分析方法論技能總管理」(2026-07-07 快照)保真遷移;遷移後以本 repo 為正典。繁中先行,英文版列 backlog。

## 概述

本 skill 是「共用分析方法論:從利益到行動的十步驟框架」的技能模組化管理入口。每個 SKILL 對應框架中的一個步驟或系統層,可獨立呼叫、組合使用。

## 使用方式

- **單一步驟呼叫**:直接指定 SKILL 編號,例如「請用 SKILL-04 行為者分析處理這份資料」
- **完整流程**:依序執行 SKILL-01 → SKILL-11,適合慢情報分析
- **快情報精簡流程**:依序執行 SKILL-01 → SKILL-02 → SKILL-04 → SKILL-09 → SKILL-10,完成後標記「初判」
- **系統層補強**:在對應步驟加入 SKILL-03(資訊評級)、SKILL-08b(跨域矩陣)、SKILL-10b(情報池)、SKILL-12(回測)

## 偵測 → 載入(SKILL 清單)

| 編號 | 名稱 | 對應步驟/系統層 | 核心問題 | 載入 |
|------|------|----------------|----------|------|
| SKILL-01 | 問題定義與範圍 | 步驟一 | 這篇分析要回答什麼? | [`references/skill-01-problem-definition.md`](references/skill-01-problem-definition.md) |
| SKILL-02 | 事實建立與背景 | 步驟二 | 已落地事實是什麼? | [`references/skill-02-fact-baseline.md`](references/skill-02-fact-baseline.md) |
| SKILL-03 | 資訊可信度評級 | 系統層 A | 這條情報可信嗎? | [`references/skill-03-credibility-rating.md`](references/skill-03-credibility-rating.md) |
| SKILL-04 | 行為者分析 | 步驟三 | 誰在局中、要什麼? | [`references/skill-04-actor-analysis.md`](references/skill-04-actor-analysis.md) |
| SKILL-05 | 可用手段篩選 | 步驟四 | 牌桌上有哪些牌? | [`references/skill-05-option-screening.md`](references/skill-05-option-screening.md) |
| SKILL-06 | 行為歸因與利益校準 | 步驟五 | 為什麼選這手段? | [`references/skill-06-attribution-calibration.md`](references/skill-06-attribution-calibration.md) |
| SKILL-07 | 決策偏好與機率調整 | 步驟六 | 最可能打哪張牌? | [`references/skill-07-decision-preference.md`](references/skill-07-decision-preference.md) |
| SKILL-08 | 連鎖反應推演 | 步驟七+系統層 B | 動作之後局面如何改變? | [`references/skill-08-chain-reaction.md`](references/skill-08-chain-reaction.md) |
| SKILL-09 | 情境預測 | 步驟八 | 可能走向哪裡?機率多少? | [`references/skill-09-scenario-forecast.md`](references/skill-09-scenario-forecast.md) |
| SKILL-10 | 觀測指標管理 | 步驟九+系統層 C | 用什麼訊號驗證劇本? | [`references/skill-10-indicator-management.md`](references/skill-10-indicator-management.md) |
| SKILL-11 | 分析缺口聲明 | 步驟十 | 分析哪裡穩、哪裡脆弱? | [`references/skill-11-gap-statement.md`](references/skill-11-gap-statement.md) |
| SKILL-12 | 預測校準與回測 | 系統層 E | 過去預測準不準?偏差在哪? | [`references/skill-12-calibration-backtest.md`](references/skill-12-calibration-backtest.md) |
| SKILL-13 | 定量數據解讀 | 擴展模組 | 這個數據變化是結構性還是噪音? | [`references/skill-13-quantitative-reading.md`](references/skill-13-quantitative-reading.md) |
| SKILL-14 | 敘事追蹤與輿論分析 | 擴展模組 | 各方在說什麼故事?敘事是否轉向? | [`references/skill-14-narrative-tracking.md`](references/skill-14-narrative-tracking.md) |
| SKILL-15 | 制度與法律約束分析 | 擴展模組 | 法律允許什麼?繞過的成本多少? | [`references/skill-15-institutional-constraints.md`](references/skill-15-institutional-constraints.md) |
| SKILL-16 | 歷史類比結構化比較 | 擴展模組 | 這次跟歷史哪個事件結構性相似? | [`references/skill-16-historical-analogy.md`](references/skill-16-historical-analogy.md) |
| SKILL-17 | 供應鏈與技術系統評估 | 擴展模組 | 瓶頸在哪?替代路徑需要多久? | [`references/skill-17-supply-chain.md`](references/skill-17-supply-chain.md) |
| SKILL-18 | 長期結構趨勢分析 | 擴展模組 | 哪些長期趨勢正在改變底層條件? | [`references/skill-18-structural-trends.md`](references/skill-18-structural-trends.md) |
| SKILL-19 | 機率分布工程 | 擴展模組 | (見該檔) | [`references/skill-19-probability-engineering.md`](references/skill-19-probability-engineering.md) |
| SKILL-20 | 跨家族遷移測試 | 擴展模組 | (見該檔) | [`references/skill-20-cross-family-transfer.md`](references/skill-20-cross-family-transfer.md) |

## 分析流程圖

**快情報流程(初判)**
SKILL-01 問題定義與範圍 → SKILL-02 事實建立與背景 → SKILL-04 行為者分析 → SKILL-09 情境預測 → SKILL-10 觀測指標管理 → 標記「初判」

**慢情報流程(補齊初判)**
SKILL-03 資訊可信度評級 → SKILL-05 可用手段篩選 → SKILL-06 行為歸因與利益校準 → SKILL-07 決策偏好與機率調整 → SKILL-08 連鎖反應推演 → SKILL-11 分析缺口聲明 → 修正初判

**追蹤循環**
SKILL-10 觀測指標管理(持續觀測)→ SKILL-12 預測校準與回測(定期回測)

**擴展模組(依需要在任何步驟插入)**
- SKILL-13 定量數據解讀 → 配合 SKILL-02 事實建立、SKILL-10 觀測指標
- SKILL-14 敘事追蹤與輿論分析 → 配合 SKILL-04 行為者分析、SKILL-07 決策偏好
- SKILL-15 制度與法律約束分析 → 配合 SKILL-05 可用手段篩選
- SKILL-16 歷史類比結構化比較 → 配合 SKILL-07 決策偏好、SKILL-09 情境預測
- SKILL-17 供應鏈與技術系統評估 → 配合 SKILL-08 連鎖反應推演
- SKILL-18 長期結構趨勢分析 → 配合 SKILL-04 行為者分析、SKILL-05 約束篩選、SKILL-09 情境預測

## 核心紀律(23 條,必遵——全文見 [`references/disciplines.md`](references/disciplines.md))

1. 從利益出發,不從行為反推意圖
2. 事實與假設分離
3. 不押單一結論,同時維持多個劇本
4. 紅隊自我挑戰必做
5. 輸出要可檢驗,預測對應可觀測訊號
6. 機率標籤附 %(5% 步進,供 Brier 校準)
7. 歸因不一致時展開 ACH 矩陣
8. 連鎖推演至少一個關鍵行為者跑對手代言人機制
9. 資料來源標桌腿類型(HUMINT/SIGINT/IMINT/OSINT)
10. 資料量>10 條先信噪分類
11. 高風險分析啟動兩軸分組(功能×立場),制度與自律雙軌審計
12. 高壓+損失域下選牌邏輯反轉(Prospect Theory)
13. 客戶壓力逆向審計(Politicization Audit)
14. 假設可證偽性自檢(Falsifiability Check)
15. 對手情報體系結構性失靈評估(Adversary IC Audit)
16. 標準措辭與機率對應表(衝突時以 % 為準)
17. 過度確定降階(≥90% 須通過可改寫性測試)
18. 預測登錄採快照鏈機制(必遵)
19. 鏈覆蓋完整性(必遵)
20. 資訊真空 ≠ 維持機率(必遵)
21. 冷鏈自動降階與喚醒(必遵)
22. 戰區深化掃描(必遵)
23. 視窗驅動的主動驗證(必遵)

## 預測驗證帳本(檔案化版本鏈)

所有 SKILL-09 預測與 SKILL-12 回測登錄至**目標專案** `docs/intel/predictions/` ——一鏈版本一 JSON 快照(`P-YYYY-MMDD-NN[-vK].json`),**歷史快照不可覆蓋、每鏈單一 latest**。規範與中↔英欄位對照見 [`references/prediction-ledger.md`](references/prediction-ledger.md);schema 在 [`assets/prediction_entry.schema.json`](assets/prediction_entry.schema.json)。

機器輔助:
```
python3 scripts/prediction_lint.py --repo .            # fail-loud 鏈驗證(可接 pre-commit/CI)
python3 scripts/prediction_lint.py --repo . --index    # 重生 INDEX.md(生成物,永不手改)
python3 scripts/brier_report.py --repo .               # Brier 校準+措辭對表+漂移清單(報告非閘門)
```
