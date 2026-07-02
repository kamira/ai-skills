---
name: branch-isolation
description: >
  分支隔離:當有多個 git 分支(branch)並行時,每個分支的需求、變更記錄、驗收與驗證只能針對「該
  分支」,不得引用其他分支開出的需求。當專案存在多個分支、或你在某分支上工作/驗收時讀本檔。涵蓋
  分支標記、只採當前分支來源、合併時才帶入的規則,以及與 cross-repo 的區別。
---

# branch-isolation — 分支隔離

> 語言 / Language: **繁體中文** · [English](branch-isolation.md)

## 用途

多分支並行時,不同分支常各自開出不同需求與變更。**在某分支工作或驗收時,所有需求/CHG/ACC/驗證只能引用該分支的來源,不得引用其他分支開出的需求**——否則會拿 B 分支的需求去驗 A 分支的程式,造成錯誤把關與範圍污染。

> 與 `cross-repo` 區別:cross-repo 是「多個 repo」間的契約協調;branch-isolation 是「同一 repo 內多個 branch」不可互相引用需求。兩者可同時存在。

## 規則

- **標記分支**:Guideline / CHG / ACC 標頭都填「分支(Branch)」欄。驗收條件與需求引用時,只取**與當前分支相同**者。
- **只採當前分支來源**:偵測/驗收/影響分析時,過濾掉其他分支的 CHG/需求。當前分支 = 進場 handshake 已確認的分支。
- **不得跨分支引用**:A 分支的驗收不可拿 B 分支的需求當基準;A 分支的 CHG 不可連結 B 分支的需求作為依據。
- **合併(merge)才帶入**:其他分支的需求/變更,只有在**合併進當前分支**時,才依正常流程(modification-guide + 驗收)納入;合併前一律視為「不在本分支範圍」。
- **共用基準**:若確有全分支共用的需求/規則,應放在共用基準(如主分支或 knowledge 標「全分支」),而非從某功能分支橫向引用。

## 何時讀

- 專案存在多個分支(feature / release / hotfix…)
- 你在某分支上實作或驗收
- 要判斷「某需求/驗收條件屬於哪個分支」

## 模板欄位

在 Guideline / CHG / ACC 標頭加:

```
- 分支(Branch):<branch 名稱>   ← 本文件所屬分支;引用/驗收只採同分支來源
```

## 與既有流程的關係

- handshake:進場第一步先確認當前分支;之後所有引用限該分支。
- modification-guide / acceptance-verification:CHG/ACC 標分支;驗收基準只取同分支的 Guideline/CHG。
- doc-integrity:可加「CHG/ACC 的分支欄 = 當前 git 分支」的檢查(不符 → flag)。
- knowledge:directive 預設當前分支;通用者標「全分支」。
