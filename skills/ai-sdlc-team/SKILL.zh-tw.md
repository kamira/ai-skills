---
name: ai-sdlc-team
description: >
  ai-sdlc 的團隊版:在單人版 ai-sdlc 的「需求分析→結構設計→修改治理→驗收」流程之上,加上
  多代理 / 多 session 協作機制與(選用)CI/CD 整合。當同一專案由多個 AI agent、或多人 / 多 session
  接力或並行開發、需要交接不漂移、避免並行衝突、或想把文件治理接上 CI/CD 門檻時,務必使用本 skill,
  並依需求讀 references:跨 agent 協作與交接讀 cross-agent;CI/CD 整合讀 ci-cd(選用)。前提是專案
  已採用 ai-sdlc 的文件治理(docs/ 為唯一事實來源)。Use for team / multi-agent development.
---

# ai-sdlc-team — AI 開發治理(團隊版)

> 語言 / Language: **繁體中文** · [English](SKILL.md)

這是 [`ai-sdlc`](../ai-sdlc/SKILL.zh-tw.md) 的**團隊延伸層**。單人版負責「一個人/一個 agent 把需求做成文件治理」;團隊版負責「**多個 agent / 多人協作時,如何不漂移、可交接、並用 CI/CD 把關**」。

## 單人版 vs 團隊版

- **ai-sdlc(單人版)**:核心四階段——需求分析(AI Guideline)、結構設計(四種結構)、修改治理(變更記錄)、驗收(報告與回修迴圈)。適合一人或單一 agent 的開發治理。
- **ai-sdlc-team(本 skill,團隊版)**:假設已採用 ai-sdlc,**額外**處理多人/多 agent 協作的兩件事——跨 agent 協作與交接、以及(選用)把治理接上 CI/CD。

> 本 skill 不重述四階段細節;階段內容請讀 ai-sdlc 的 references。本 skill 專注於「協作層」與「自動化把關層」。

## 「團隊」不限於人——可以是 AI agent 團隊

這裡的「團隊」指**多個獨立執行單位**,可以是多位開發者、也可以是**多個 AI agent**(不同執行個體 / 不同 context),或兩者混合。多 agent 協作正是本 skill 的核心情境:它們無法共用對話記憶,只能靠 `docs/` 協作;而「實作 agent」與「驗收 agent」分離所帶來的獨立性,正是團隊版把關品質的關鍵。

## 前提:docs/ 是團隊的唯一事實來源

團隊協作能成立的關鍵,是每個 agent / 每個人都把狀態與決策寫進 `docs/`,並在進場時先讀它——而不是靠各自的對話記憶(無法跨單位、會被壓縮)。這延續 ai-sdlc 的「文件即真實 / 不倚賴記憶」原則,並把它從「個人記憶」升級為「團隊協作媒介」。

## 與基底 ai-sdlc 的分工

**抗漂移(doc-integrity)、CI/CD(選用)都在基底 `ai-sdlc`**(單人/團隊共用,故放基底);本團隊版只加「協作層」的兩件事。請搭配 `ai-sdlc` 一起使用。

| 面向 | 何時讀 | 指引 |
|------|--------|------|
| 跨 agent 協作 / 交接 | 工作換手、跨 session 累加、或多 agent 同時動同一專案 | [`references/cross-agent.zh-tw.md`](references/cross-agent.zh-tw.md) |
| 跨 agent / 多情境獨立驗收 | code 改完要驗收時(由不同 agent、不同情境跑) | [`references/independent-acceptance.zh-tw.md`](references/independent-acceptance.zh-tw.md) |
| 文檔抗漂移與驗證 | (在基底)確認文件仍可信、變更收尾、進場接手 | `ai-sdlc` 的 `references/doc-integrity` |
| CI/CD 整合(**選用**) | (在基底)依需求把門檻自動化 | `ai-sdlc` 的 `references/ci-cd` |

重點:`cross-agent` 涵蓋**順序接力**與**並行多 agent**,並要求每個 agent 帶**明確角色與讀寫權限**;`independent-acceptance` 要求**驗收者 ≠ 實作者、跨情境、且驗收者唯讀**。抗漂移與 CI/CD 用基底 ai-sdlc 的對應 reference。

## 使用原則(在 ai-sdlc 原則之上)

1. **每個 agent 都要有明確角色與讀寫權限**:派工(人或 AI agent)時先定義「角色 + 可讀/可寫範圍」——例如實作者可寫其 claim 範圍、驗收者**唯讀**(只能讀程式與條件、只能寫自己的 ACC,不可改被驗的碼)。權限分離是獨立性與防誤改的基礎。
2. **進場先讀 docs/**:任何 agent 接手前,先讀既有文件還原狀態(含 ai-sdlc 的 Session 啟動檢查)。
3. **離場留乾淨狀態**:當場驗收、回填狀態、同步結構文件,讓下一棒讀文件就能接。
4. **並行要先認領**:多 agent 同時動時,先在協調文件 claim 不重疊範圍(含角色與讀寫範圍),單寫者規則避免互相覆蓋。
5. **驗收要獨立、多情境、唯讀**:code 改完**不由實作的 agent 自驗**,交給唯讀的驗收 agent、在不同情境下跑再彙整(見 independent-acceptance)。
6. **抗漂移與自動化**:文件持續驗證、不漂移(用基底 ai-sdlc 的 doc-integrity);有 CI/CD 則把門檻自動化(基底 ci-cd,選用)。
