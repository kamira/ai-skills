---
name: ai-sdlc-team
description: >
  AI 開發治理(團隊版,自我完備):涵蓋完整流程——需求分析→結構設計→修改治理→驗收,加上抗漂移、
  子代理工作日誌與錯誤知識庫、(選用)CI/CD,以及團隊協作機制(跨 agent 交接/並行、獨立驗收、角色與
  讀寫權限)。當專案由多人或多個 AI agent 接力/並行開發、需要交接不漂移、獨立把關時使用。團隊不限於
  人,可為 AI agent 團隊。本版自含,無需另裝個人版 ai-sdlc。Use for team / multi-agent development.
---

# ai-sdlc-team — AI 開發治理(團隊版,自我完備)

> 語言 / Language: **繁體中文** · [English](SKILL.md)

讓 AI 協助開發時有一致流程可循,並支援**多人 / 多 AI agent 協作**。核心理念:**先把需求、結構、變更、驗收都記錄成文件,大家(含未來的自己、別的 agent)讀文件當依據**,而不是靠各自的對話記憶。**本版自我完備,涵蓋完整治理 + 協作,不需另裝個人版 `ai-sdlc`**(個人單純開發可改用較精簡的 `ai-sdlc`)。

## 偵測即載入(自動觸發)

**不要等使用者點名;偵測到下列情境就主動載入對應 reference**(同一套偵測機制,單人或團隊皆適用):

| 偵測到的情境 | 主動載入 |
|--------------|----------|
| 涉及多個 git repo / 多 repo 共用契約 | `cross-repo`(+ `scripts/cross_repo_check.py` 查漂移) |
| 並行多 agent、跨 session 接力、交接/換手 | `cross-agent` |
| 要派子代理 / 多 agent 分工 | `agent-worklog` + `agent-hierarchy` |
| 提出「修改 / 新功能」 | `modification-guide`(強制) |
| code 改完要驗收(尤其高風險、由不同 agent) | `acceptance-verification` + `independent-acceptance` |
| 進場接手 / 跨 session | Session 啟動檢查:讀既有 docs/ + 錯誤知識庫 + `doc-integrity` |
| 專案有 / 要導入 CI/CD | `ci-cd`(選用;pre-commit 或 pipeline) |

## 「團隊」不限於人——可以是 AI agent 團隊

「團隊」指**多個獨立執行單位**:多位開發者、多個 AI agent(不同執行個體 / 不同 context),或混合。它們無法共用對話記憶,只能靠 `docs/` 協作;而「實作 agent」與「驗收 agent」分離帶來的獨立性,正是把關品質的關鍵。

## 流程閉環

```
 [需求/新功能]
      │
      ▼
 需求分析 ──► 結構設計 ──► 實作 ──► 驗收
 (Guideline)  (四種結構)            │
                            ┌───────┴───────┐
                          通過            未通過
                            │                │
                            ▼                ▼
                          完成          修改治理 → 重新實作 → 重新驗收
```

## 階段指引(依需求載入)

| 階段 | 何時使用 | 指引 |
|------|----------|------|
| 1. 需求分析 | 新專案/新需求 | [`references/requirement-analysis.zh-tw.md`](references/requirement-analysis.zh-tw.md) |
| 2. 結構設計 | Guideline 確立,訂系統結構 | [`references/structure-design.zh-tw.md`](references/structure-design.zh-tw.md) |
| 3. 修改治理 | 提出修改/新功能時(**必走**) | [`references/modification-guide.zh-tw.md`](references/modification-guide.zh-tw.md) |
| 4. 驗收 | 實作/修改完成 | [`references/acceptance-verification.zh-tw.md`](references/acceptance-verification.zh-tw.md) |

## 跨階段指引

| 面向 | 何時使用 | 指引 |
|------|----------|------|
| 文檔抗漂移與驗證 | 確認文件仍可信、變更收尾、進場接手 | [`references/doc-integrity.zh-tw.md`](references/doc-integrity.zh-tw.md) |
| 子代理工作日誌 + 錯誤知識庫 | 派子代理、或被派執行前 | [`references/agent-worklog.zh-tw.md`](references/agent-worklog.zh-tw.md) |
| 代理編制與階層 | 多 agent 分工、或某 agent 要再派子 agent(編號+固定範圍+不越權;遞迴視平台) | [`references/agent-hierarchy.zh-tw.md`](references/agent-hierarchy.zh-tw.md) |
| 跨 repo 協調與一致性 | 需求/變更橫跨多個 git repo、或多 repo 共用契約 | [`references/cross-repo.zh-tw.md`](references/cross-repo.zh-tw.md) |
| CI/CD 整合(**選用**) | 把門檻自動化成 pre-commit 或 pipeline | [`references/ci-cd.zh-tw.md`](references/ci-cd.zh-tw.md) |

## 團隊協作指引

| 面向 | 何時使用 | 指引 |
|------|----------|------|
| 跨 agent 協作 / 交接 | 換手、跨 session 累加、多 agent 同時動 | [`references/cross-agent.zh-tw.md`](references/cross-agent.zh-tw.md) |
| 跨 agent / 多情境獨立驗收 | code 改完,由不同 agent、唯讀、多情境驗 | [`references/independent-acceptance.zh-tw.md`](references/independent-acceptance.zh-tw.md) |

## 強制規則:修改一定先治理

只要有人提出「修改」或「新功能」,**先走 `modification-guide`,不可直接改碼**;實作完**同一輪當場驗收**產出 ACC、回填 CHG 狀態,不可把驗收交棒給下一個 session(沒人會接)。

## Session 啟動檢查(跨 session / 換手必做)

每次進場、動新需求前先掃:`docs/changes/` 有沒有未驗收的 CHG、`docs/acceptance/` 有沒有缺 ACC、`docs/knowledge/` 錯誤知識庫有哪些已知坑——先補未收尾的、讀過知識庫,再開始。

## 文件存放慣例

產出放在**目標專案** `docs/`:`ai-guideline.md`、`structure/{directory,logical,design,data}.md`、`changes/CHG-*.md`、`acceptance/ACC-*.md`、`worklog/`、`knowledge/errors.md`。**跨專案**時,各文件標頭註明所屬「專案」,編號可帶專案前綴。

## 使用原則

1. **每個 agent 都要有明確角色與讀寫權限**:派工(人或 AI agent)先定義「角色 + 可讀/可寫範圍」;驗收者**唯讀**(只讀碼與條件、只寫自己的 ACC,不可改被驗的碼)。最小權限。
2. **子代理執行前先寫、遇錯記錄再續**:子代理動手前先在 worklog 寫「要做什麼」;遇錯記「什麼錯+根因+解法」再繼續;完成回報錯誤清單,由上層彙整進知識庫。
3. **進場先讀 docs/(含知識庫)**:不倚賴記憶,以文件為準;記憶與文件衝突時以文件為準(抗壓縮/換手)。
4. **離場留乾淨狀態**:當場驗收、回填狀態、同步結構文件。
5. **並行要先認領**:在協調文件 claim 不重疊範圍(含角色與讀寫權限),單寫者規則。
6. **驗收獨立、多情境、唯讀**:不由實作者自驗。
7. **文件抗漂移**:結構變了就同步,發現漂移回流程補記。
8. **能自動就自動(選用)**:有 CI/CD 就把門檻放 pre-commit / pipeline。
