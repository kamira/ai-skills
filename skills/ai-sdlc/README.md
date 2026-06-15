# ai-sdlc — AI 開發治理流程 Skill 套件

> 語言 / Language: **繁體中文** · [English](README.en.md)

這是一套讓 AI 在協助開發時有一致流程可循的 skill 集合。核心理念:**先把需求、結構、變更、驗收都記錄成文件,AI 後續工作時讀這些文件當作依據**,而不是每次都從零猜測。

這份說明檔是整套系統的入口。AI 在開始一項開發任務前,應先讀這裡判斷「現在該用哪個 skill」。

## 為什麼需要這套流程

AI 協助開發最大的問題是「失憶」與「漂移」:每次對話都缺乏先前的決策脈絡,容易做出與既有架構衝突的修改。這套流程把每個階段的產出固定成文件(AI Guideline、結構文件、變更記錄、驗收報告),讓任何一次 AI 任務都能先讀文件、再動手,維持一致性。

## 四個階段與對應 skill

整體是一個閉環,從需求進來,到驗收完成。**驗收未通過會交回修改流程重做,重新驗收,直到通過或使用者接受**:

```
 [需求/新功能]
      │
      ▼
 requirement-analysis ──► structure-design ──► 實作 ──► acceptance-verification
  (需求 → Guideline)       (四種結構)                          │
                                                       ┌────────┴────────┐
                                                     通過              未通過
                                                       │                  │
                                                       ▼                  ▼
                                                     完成        modification-guide
                                                              (修改指引+記錄+結構調整)
                                                                          │
                                                                          ▼
                                                                重新實作 → 重新驗收
                                                                (回到 acceptance)

 另一個入口:使用者在任何時候提出「修改 / 新功能」
   → 強制掛載 modification-guide → 實作 → acceptance-verification(同一條驗收線)
```

modification-guide 有兩個入口:(1) 使用者主動提出修改/新功能,(2) 驗收未通過交回修正。兩者都走「修改治理 → 重新實作 → 重新驗收」,讓迴圈鎖死,不會出現「驗收沒過卻無人接手」的斷點。

| 階段 | Skill | 何時使用 | 主要產出 |
|------|-------|----------|----------|
| 1. 需求分析 | `requirement-analysis` | 收到新專案或新需求,需釐清做什麼 | `docs/ai-guideline.md` |
| 2. 結構設計 | `structure-design` | Guideline 確立後,要訂出系統結構 | `docs/structure/*.md` |
| 3. 修改治理 | `modification-guide` | 提出修改或新功能時(**強制掛載**) | `docs/changes/*.md` + 更新結構 |
| 4. 驗收 | `acceptance-verification` | 實作或修改完成,要確認是否達標 | `docs/acceptance/*.md` |

## 強制掛載規則(對應原始第 5 項需求)

**只要使用者在一個 session 中提出「修改」或「新功能」,AI 必須先載入並依循 `modification-guide` skill,不可略過。** 這是因為任何變更都可能牽動既有結構與先前決策,跳過修改治理會造成架構漂移與記錄缺漏。詳細機制寫在 `modification-guide/SKILL.md`。

其餘 skill 採「依需求、非必需」讀取:AI 判斷當前任務屬於哪個階段,才去讀對應 skill,避免一次塞入過多無關內容。

## 文件存放慣例

這套 skill 產出的文件都放在**目標專案**的 `docs/` 下(不是放在本 repo)。本 repo 只存放 skill 本身。建議結構:

```
<目標專案>/
└── docs/
    ├── ai-guideline.md          # 需求分析產出
    ├── structure/
    │   ├── directory.md          # 目錄結構
    │   ├── logical.md            # 邏輯結構
    │   ├── design.md             # 設計結構
    │   └── data.md               # 資料結構
    ├── changes/
    │   └── CHG-YYYYMMDD-NN.md    # 每次變更一份記錄
    └── acceptance/
        └── ACC-YYYYMMDD-NN.md    # 每次驗收一份報告
```

若目標專案已有其他文件慣例,以該專案為準,並在 AI Guideline 中註明實際路徑。

## 使用原則

1. **先讀後做**:動手前先讀對應階段的 skill 與既有文件。
2. **文件即真實**:結構文件與 Guideline 是後續判斷的依據;結構變了就要同步更新文件,不能只改程式。
3. **每次變更留痕**:修改一定要在 `docs/changes/` 留一份記錄,寫清楚動機與取捨。
4. **驗收對齊來源**:驗收標準來自 Guideline 與該次修改指引,不憑空發明。

## 子 skill 一覽

- [`requirement-analysis/`](requirement-analysis/SKILL.md) — 需求分析,產出 AI Guideline
- [`structure-design/`](structure-design/SKILL.md) — 產出目錄/邏輯/設計/資料結構
- [`modification-guide/`](modification-guide/SKILL.md) — 修改指引、變更記錄、結構調整、強制掛載
- [`acceptance-verification/`](acceptance-verification/SKILL.md) — 依據驗收結果
