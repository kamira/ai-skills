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
| **ai-sdlc**(單人版) | AI 開發治理閉環:需求分析 → 結構設計 → 修改治理 → 驗收;含抗漂移、子代理工作日誌/錯誤知識庫、選用 CI/CD;適合一人/單一 agent。**自含。** | [`skills/ai-sdlc/SKILL.md`](skills/ai-sdlc/SKILL.md) |
| **ai-sdlc-team**(團隊版) | 完整流程 + 多代理/多 session 協作交接、獨立驗收、角色與讀寫權限;適合團隊(可為 AI agent 團隊)。**自含,不需另裝單人版。** | [`skills/ai-sdlc-team/SKILL.md`](skills/ai-sdlc-team/SKILL.md) |

兩版都**自我完備**(各自可獨立安裝):個人用 `ai-sdlc`,團隊用 `ai-sdlc-team`(它是單人版的超集 + 協作層)。

`ai-sdlc`(單人版)references:

| 指引 | 用途 |
|------|------|
| 1. 需求分析 [`requirement-analysis`](skills/ai-sdlc/references/requirement-analysis.md) | 需求轉成標準化 AI Guideline |
| 2. 結構設計 [`structure-design`](skills/ai-sdlc/references/structure-design.md) | 產出目錄/邏輯/設計/資料四種結構 |
| 3. 修改治理 [`modification-guide`](skills/ai-sdlc/references/modification-guide.md) | 影響分析、變更記錄、結構同步(變更時強制走) |
| 4. 驗收 [`acceptance-verification`](skills/ai-sdlc/references/acceptance-verification.md) | 依 Guideline 與修改指引驗收,未通過回修迴圈 |
| ✦ 抗漂移 [`doc-integrity`](skills/ai-sdlc/references/doc-integrity.md) | 文檔抗漂移與驗證(單人也需要) |
| ✦ 子代理日誌 [`agent-worklog`](skills/ai-sdlc/references/agent-worklog.md) | 子代理執行前先寫、遇錯記錄;上層彙整錯誤進知識庫(單人派 subagent 也適用) |
| ✦ 跨 repo [`cross-repo`](skills/ai-sdlc/references/cross-repo.md) | 跨 repo 協調:權威來源+本地指標、XCHG 協調變更、整合驗收 |
| ✦ CI/CD [`ci-cd`](skills/ai-sdlc/references/ci-cd.md)(**選用**) | pre-commit 初步檢查 + pipeline 權威門檻;含風險分級與身分檢查 gate |

> 抗 session 壓縮:含「Session 啟動檢查 + 不倚賴記憶以文件為準」。跨專案/跨 repo:Guideline/CHG/ACC 標頭有「專案」欄;跨 repo 用權威來源 + XCHG 協調。風險分級:CHG/ACC 有風險欄,驅動驗收與 CI 門檻嚴格度。

`ai-sdlc-team`(團隊版)= 上面**全部** + 兩份協作層 references,且**自含、不參照單人版**:

| reference | 處理 |
|-----------|------|
| `cross-agent` | 跨 agent 協作與交接(順序接力 + 並行多 agent),每個 agent 帶角色與讀寫權限 |
| `independent-acceptance` | 跨 agent / 多情境獨立驗收(驗收者 ≠ 實作者、且唯讀) |

可安裝版在 [`dist/`](dist/):

- 單人版:`ai-sdlc.skill`(英文)、`ai-sdlc.zh-tw.skill`(繁中)
- 團隊版:`ai-sdlc-team.skill`(英文)、`ai-sdlc-team.zh-tw.skill`(繁中)

## 目錄結構

```
ai-skills/
├── README.md                      # 本文件
├── .gitignore                     # 排除評測產物等
├── dist/                          # 可安裝的 .skill 發佈版
│   ├── ai-sdlc.skill / .zh-tw.skill            # 單人版(英文 / 繁中)
│   └── ai-sdlc-team.skill / .zh-tw.skill       # 團隊版(英文 / 繁中)
└── skills/                        # Skill 原始檔
    ├── ai-sdlc/                   # 單人版(自含)
    │   ├── SKILL.md / SKILL.zh-tw.md       # orchestrator(英文 / 繁中)
    │   ├── references/                     # 各檔 .md(英文)+ .zh-tw.md(繁中)
    │   │   ├── requirement-analysis · structure-design · modification-guide · acceptance-verification
    │   │   ├── doc-integrity            # 文檔抗漂移與驗證
    │   │   ├── agent-worklog            # 子代理工作日誌 + 錯誤知識庫
    │   │   ├── cross-repo               # 跨 repo 協調與一致性
    │   │   └── ci-cd                    # CI/CD:pre-commit + pipeline(選用)
    │   └── evals/evals.json       # 測試案例定義
    └── ai-sdlc-team/              # 團隊版(自含超集;團隊可為 AI agent)
        ├── SKILL.md / SKILL.zh-tw.md           # orchestrator(英文 / 繁中)
        └── references/                          # 上面 7 份 + 下面 2 份協作層
            ├── cross-agent                      # 跨 agent 協作與交接(角色+讀寫權限)
            └── independent-acceptance           # 跨 agent / 多情境獨立驗收(驗收者唯讀)
```

> 命名慣例:`.md` 為英文(預設),`.zh-tw.md` 為繁體中文。打包成 `.skill` 時只能含一個 `SKILL.md`,故發佈版按語言分為兩個檔(見 `dist/`)。一般 Skill 也可附 `scripts/`、`assets/`;本套件以指示文件為主,故未使用。

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
