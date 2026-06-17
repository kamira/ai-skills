# AI Skills

整理與管理自建 AI Skills 的 repo。每個 Skill 是一個獨立資料夾,內含 `SKILL.md` 與相關資源,可被 Claude / Cowork 等代理工具載入使用。

## 目錄

- [什麼是 Skill](#什麼是-skill)
- [Skill 一覽](#skill-一覽)
- [目錄結構](#目錄結構)
- [SKILL.md 格式](#skillmd-格式)
- [新增 Skill](#新增-skill)
- [命名規範](#命名規範)

## 什麼是 Skill

Skill 是一包可重複使用的能力:用自然語言寫成的指示、流程與資源檔。當使用者的需求符合 Skill 的觸發條件時,代理會載入該 Skill 的 `SKILL.md`,依其指示完成任務。

## Skill 一覽

| Skill | 說明 | 入口 |
|-------|------|------|
| **ai-sdlc** | AI 開發治理閉環:需求分析 → 結構設計 → 修改治理 → 驗收;**一套涵蓋單人到團隊**——預設單人,偵測到協作(多 agent / 跨 session / 多 repo)自動升級到團隊模式。團隊可為 AI agent 團隊。 | [`skills/ai-sdlc/SKILL.md`](skills/ai-sdlc/SKILL.md) |

**單一 skill,自適應單人/團隊**:不需選版本。**自主偵測為預設、使用者可選擇或覆寫**——偵測到多 repo 就載 `cross-repo`、並行/交接就載 `cross-agent`、要派子代理就載 `agent-worklog`/`agent-hierarchy`、提出修改就載 `modification-guide`……;使用者明示時以明示為準(如「強制團隊模式」「這次不要 CI/CD」)。

references(12 份,依偵測/選擇載入):

| 指引 | 用途 |
|------|------|
| 1. 需求分析 [`requirement-analysis`](skills/ai-sdlc/references/requirement-analysis.md) | 需求轉成標準化 AI Guideline |
| 2. 結構設計 [`structure-design`](skills/ai-sdlc/references/structure-design.md) | 產出目錄/邏輯/設計/資料四種結構 |
| 3. 修改治理 [`modification-guide`](skills/ai-sdlc/references/modification-guide.md) | 影響分析、變更記錄、結構同步(變更時強制走) |
| 4. 驗收 [`acceptance-verification`](skills/ai-sdlc/references/acceptance-verification.md) | 依 Guideline 與修改指引驗收,未通過回修迴圈 |
| ✦ 抗漂移 [`doc-integrity`](skills/ai-sdlc/references/doc-integrity.md) | 文檔抗漂移與驗證(單人也需要) |
| ✦ 子代理日誌 [`agent-worklog`](skills/ai-sdlc/references/agent-worklog.md) | 子代理執行前先寫、遇錯記錄;上層彙整錯誤進知識庫(單人派 subagent 也適用) |
| ✦ 代理編制 [`agent-hierarchy`](skills/ai-sdlc/references/agent-hierarchy.md) | 編號+固定範圍+不越權;遞迴授權只縮不放、上層管理;分析→實作(分派+自檢)→獨立驗收(遞迴視平台而定) |
| ✦ 跨 repo [`cross-repo`](skills/ai-sdlc/references/cross-repo.md) | 跨 repo 協調:權威來源+本地指標、XCHG 協調變更、整合驗收;附漂移檢查腳本 |
| ✦ 跨 agent [`cross-agent`](skills/ai-sdlc/references/cross-agent.md) | 跨 agent 協作與交接(順序接力 + 並行多 agent),角色與讀寫權限 |
| ✦ 獨立驗收 [`independent-acceptance`](skills/ai-sdlc/references/independent-acceptance.md) | 跨 agent / 多情境獨立驗收(驗收者 ≠ 實作者、唯讀、跨模型) |
| ✦ 自主停點 [`autonomy`](skills/ai-sdlc/references/autonomy.md) | 自主執行的停點契約:風險×關卡→auto/halt + 永遠停點動作;附 `halt_gate.py` 與 `halt_policy.json` |
| ✦ CI/CD [`ci-cd`](skills/ai-sdlc/references/ci-cd.md)(**選用**) | pre-commit 初步檢查 + pipeline 權威門檻;含風險分級與身分檢查 gate |

> 抗 session 壓縮:含「Session 啟動檢查 + 不倚賴記憶以文件為準」。跨專案/跨 repo:Guideline/CHG/ACC 標頭有「專案」欄;跨 repo 用權威來源 + XCHG 協調。風險分級:CHG/ACC 有風險欄,驅動驗收與 CI 門檻嚴格度。

可安裝版在 [`dist/`](dist/):`ai-sdlc.skill`(英文)、`ai-sdlc.zh-tw.skill`(繁中)。

## 目錄結構

```
ai-skills/
├── README.md                      # 本文件
├── .gitignore                     # 排除評測產物等
├── dist/                          # 可安裝的 .skill 發佈版
│   └── ai-sdlc.skill / .zh-tw.skill            # 英文 / 繁中
├── examples/cross-repo/           # 跨 repo 範本專案(authority + 2 消費 repo + XCHG)
└── skills/
    └── ai-sdlc/                   # 單一 skill(自適應單人/團隊)
        ├── SKILL.md / SKILL.zh-tw.md       # orchestrator(英文 / 繁中)
        ├── scripts/
        │   ├── cross_repo_check.py         # 跨 repo 指標漂移檢查(可接 pre-commit/CI)
        │   ├── doc_integrity_check.py      # 文檔抗漂移:結構同步 + CHG↔ACC 連結(可接 pre-commit/CI)
        │   └── halt_gate.py                # 自主停點查詢:風險×關卡→AUTO/HALT
        ├── assets/halt_policy.json         # 停點契約(可編輯)
        ├── references/                     # 12 份,各檔 .md(英文)+ .zh-tw.md(繁中):
        │   ├── requirement-analysis · structure-design · modification-guide · acceptance-verification
        │   ├── doc-integrity(抗漂移)· agent-worklog(子代理日誌+錯誤知識庫)
        │   ├── agent-hierarchy(代理編制階層)· cross-repo(跨 repo)
        │   ├── cross-agent(跨 agent 協作交接)· independent-acceptance(獨立驗收)
        │   ├── autonomy(自主執行停點契約)
        │   └── ci-cd(選用:pre-commit + pipeline)
        └── evals/evals.json       # 測試案例定義
```

> 命名慣例:`.md` 為英文(預設),`.zh-tw.md` 為繁體中文。打包成 `.skill` 時只能含一個 `SKILL.md`,故發佈版按語言分為兩個檔(見 `dist/`)。

## SKILL.md 格式

每個 Skill 以 YAML frontmatter 開頭,接著為指示內容:

```markdown
---
name: my-skill
description: 一句話說明這個 Skill 做什麼、何時該觸發(關鍵字越具體,觸發越準)。
---

# My Skill

## 用途
說明這個 Skill 解決什麼問題。

## 使用時機
列出觸發條件與範例情境。

## 步驟
1. ...
2. ...
```

### 撰寫要點

- **description 決定觸發率**:寫清楚「做什麼 + 何時用」,並放入使用者可能說出的關鍵字。
- **指示要明確**:把步驟、輸入、輸出講清楚,避免模糊。
- **資源分離**:腳本放 `scripts/`、範本放 `assets/`,`SKILL.md` 專注於指示。
- **雙語(選用)**:預設語言用 `SKILL.md`,其他語言用 `SKILL.<lang>.md`(如 `SKILL.zh-tw.md`),並於頂部互相連結。打包 `.skill` 時每包只留一個 `SKILL.md`。

## 新增 Skill

1. 在 `skills/` 下建立資料夾,命名用小寫加連字號(如 `weekly-report`)。
2. 建立 `SKILL.md` 並填入 frontmatter 與指示。
3. 需要的話加入 `scripts/`、`assets/`。
4. 更新本 README 的「Skill 一覽」與「目錄結構」。
5. commit。

## 命名規範

- 資料夾與 `name`:小寫、連字號分隔(kebab-case)。
- 一個 Skill 一個資料夾,職責單一。
