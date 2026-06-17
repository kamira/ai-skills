---
name: ai-sdlc
description: >
  AI 開發治理流程套件:把開發拆成需求分析、結構設計、修改治理、驗收四個階段,並用文件貫穿,
  讓每次 AI 工作都先讀文件再動手,維持一致與可追溯。當使用者要規劃新專案或新功能、釐清需求、
  設計系統架構或資料庫、提出任何修改或新增功能、或要驗收成果是否達標時,務必使用本 skill 依
  階段流程進行,並讀取 references 內對應階段的指引。涵蓋:產出 AI Guideline、目錄/邏輯/設計/
  資料四種結構、變更記錄與影響分析、驗收報告與未通過回修迴圈。特別注意:使用者一旦提出「修改」
  或「新功能」,必須先走修改治理(modification-guide)而非直接改程式碼。Use this whenever
  planning, designing, modifying, or verifying software so the work stays documented and traceable.
---

# ai-sdlc — AI 開發治理流程

> 語言 / Language: **繁體中文** · [English](SKILL.md)

這套 skill 讓 AI 協助開發時有一致流程可循。核心理念:**先把需求、結構、變更、驗收都記錄成文件,AI 後續工作時讀這些文件當作依據**,而不是每次從零猜測。動手前先讀這裡,判斷「現在該用哪個階段」,再去讀 `references/` 內對應的詳細指引。

## 為什麼需要

AI 協助開發最大的問題是「失憶」與「漂移」:每次對話缺乏先前決策脈絡,容易做出與既有架構衝突的修改。本流程把每階段產出固定成文件(AI Guideline、結構文件、變更記錄、驗收報告),讓任何一次任務都能先讀文件、再動手。

## 四個階段與對應指引

```
 [需求/新功能]
      |
      v
 需求分析 --> 結構設計 --> 實作 --> 驗收
 (Guideline)  (四種結構)            |
                            +-------+-------+
                          通過           未通過
                            |              |
                            v              v
                          完成         修改治理
                                  (修改指引+記錄+結構同步)
                                          |
                                          v
                                重新實作 --> 重新驗收(回到驗收)

 另一入口:使用者隨時提出「修改 / 新功能」 --> 強制走修改治理 --> 實作 --> 驗收
```

| 階段 | 何時使用 | 詳細指引 | 主要產出 |
|------|----------|----------|----------|
| 1. 需求分析 | 新專案/新需求,需釐清做什麼 | [`references/requirement-analysis.zh-tw.md`](references/requirement-analysis.zh-tw.md) | `docs/ai-guideline.md` |
| 2. 結構設計 | Guideline 確立,要訂系統結構 | [`references/structure-design.zh-tw.md`](references/structure-design.zh-tw.md) | `docs/structure/*.md` |
| 3. 修改治理 | 提出修改或新功能時(**必走**) | [`references/modification-guide.zh-tw.md`](references/modification-guide.zh-tw.md) | `docs/changes/*.md` + 更新結構 |
| 4. 驗收 | 實作/修改完成,確認是否達標 | [`references/acceptance-verification.zh-tw.md`](references/acceptance-verification.zh-tw.md) | `docs/acceptance/*.md` |

跨階段的兩份(隨時可用):

| 面向 | 何時使用 | 詳細指引 |
|------|----------|----------|
| 文檔抗漂移與驗證 | 確認既有文件仍可信、變更收尾、進場接手時(單人也需要) | [`references/doc-integrity.zh-tw.md`](references/doc-integrity.zh-tw.md) |
| 子代理工作日誌 + 錯誤知識庫 | 你要派子代理、或被派執行任務前(單人派 subagent 也適用) | [`references/agent-worklog.zh-tw.md`](references/agent-worklog.zh-tw.md) |
| 代理編制與階層 | 任務由多個 agent 分工、或某 agent 要再派子 agent(編號+固定範圍+不越權;遞迴視平台而定) | [`references/agent-hierarchy.zh-tw.md`](references/agent-hierarchy.zh-tw.md) |
| 跨 repo 協調與一致性 | 一個需求/變更橫跨多個 git repo、或多 repo 共用契約時 | [`references/cross-repo.zh-tw.md`](references/cross-repo.zh-tw.md) |
| CI/CD 整合(**選用**) | 依需求,把驗收與結構一致性自動化成 pre-commit 或 pipeline 門檻 | [`references/ci-cd.zh-tw.md`](references/ci-cd.zh-tw.md) |

依當前任務屬於哪個階段,才去讀對應的 reference,避免一次載入過多無關內容。英文版為各檔的 `*.md`、本檔英文版為 SKILL.md。

> **多人/多 agent 團隊**:本 skill 是單人/單一 agent 的基底;團隊協作(交接、並行、獨立驗收、角色與讀寫權限)請另用 `ai-sdlc-team`。
>
> **跨專案**:同時涉及多個專案時,Guideline / CHG / ACC / 結構文件都要在標頭註明所屬「專案」,變更與驗收編號建議帶專案前綴,避免跨專案張冠李戴。

## Session 啟動檢查(跨 session 累加開發必做)

**每次進場、動任何新需求之前,先掃既有文件確認沒有「斷在半路」的階段:**

1. 讀 `docs/changes/` 最新的 CHG:若有狀態不是「已驗收」者,代表上一個 session 的變更只做到一半。
2. 比對 `docs/acceptance/`:若某個 CHG 沒有對應的 ACC 驗收報告,代表驗收被交棒卻沒人接。
3. **先把這些未收尾的驗收補做(走 acceptance-verification),再開始新需求。**

為什麼:跨 session 開發最常見的破口是「修改流程把驗收當下一步交棒,但下一個 session 來的是新功能、不是驗收」,於是驗收永遠懸著。進場先檢查,能讓「修改→驗收」的迴圈在跨 session 也自動接上。

## 強制規則:修改一定先治理

**只要使用者在一個 session 提出「修改」或「新功能」,必須先讀並依循 `references/modification-guide.zh-tw.md`,不可直接改程式碼。** 任何變更都可能牽動既有結構與先前決策;跳過治理會造成架構漂移與記錄缺漏。修改治理有兩個入口:(1) 使用者主動提出,(2) 驗收未通過交回修正——兩者都走「修改治理 → 重新實作 → 重新驗收」,讓迴圈鎖死。

**收尾即驗收**:一次變更的實作完成後,**在同一輪就接著做 acceptance-verification 產出 ACC**,不可只把狀態標成「待驗收」就結束——跨 session 沒有人會接棒。

## 文件存放慣例

產出文件放在**目標專案**的 `docs/` 下(非本 skill):

```
目標專案/docs/
├── ai-guideline.md          # 需求分析產出
├── structure/{directory,logical,design,data}.md   # 結構設計產出
├── changes/CHG-YYYYMMDD-NN.md                      # 每次變更一份
└── acceptance/ACC-YYYYMMDD-NN.md                   # 每次驗收一份
```

若目標專案已有文件慣例,以該專案為準,並在 AI Guideline 註明實際路徑。

## 使用原則

1. **先讀後做**:動手前先讀對應階段指引與既有文件。
2. **文件即真實**:結構變了就同步更新結構文件,不能只改程式。
3. **每次變更留痕**:修改一定在 `docs/changes/` 留記錄,寫清楚動機與取捨。
4. **驗收對齊來源**:驗收標準來自 Guideline 與該次修改指引,不憑空發明。
5. **不倚賴記憶,以文件為準**:長對話的 context 可能被壓縮而遺失或扭曲早期決策。**不要單憑印象**——每次動手前,以 `docs/`(Guideline、結構、CHG、ACC)既有文件重新確認既有約束與決策;當記憶與文件不一致時,以文件為準。這讓壓縮、跨 session、換手都不會造成漂移。
