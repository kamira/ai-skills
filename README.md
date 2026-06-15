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

| Skill | 說明 | 路徑 |
|-------|------|------|
| **ai-sdlc** | AI 開發治理流程套件:需求分析 → 結構設計 → 修改治理 → 驗收 的閉環流程,含繁中/英文雙版本 | [`skills/ai-sdlc/`](skills/ai-sdlc/README.md) |

`ai-sdlc` 套件內含 4 個子 skill:

| 子 skill | 階段 | 用途 |
|----------|------|------|
| [`requirement-analysis`](skills/ai-sdlc/requirement-analysis/SKILL.md) | 1. 需求分析 | 把需求轉成標準化 AI Guideline |
| [`structure-design`](skills/ai-sdlc/structure-design/SKILL.md) | 2. 結構設計 | 產出目錄/邏輯/設計/資料四種結構 |
| [`modification-guide`](skills/ai-sdlc/modification-guide/SKILL.md) | 3. 修改治理 | 影響分析、變更記錄、結構同步(變更時強制掛載) |
| [`acceptance-verification`](skills/ai-sdlc/acceptance-verification/SKILL.md) | 4. 驗收 | 依 Guideline 與修改指引驗收,未通過回修迴圈 |

## 目錄結構

```
ai-skills/
├── README.md                      # 本文件
├── .gitignore                     # 排除評測產物等
└── skills/                        # 所有 Skill 放這裡
    └── ai-sdlc/                   # AI 開發治理流程套件
        ├── README.md              # 套件說明(繁中)
        ├── README.en.md           # 套件說明(英文)
        ├── requirement-analysis/
        │   ├── SKILL.md           # 繁中
        │   └── SKILL.en.md        # 英文
        ├── structure-design/
        │   ├── SKILL.md
        │   └── SKILL.en.md
        ├── modification-guide/
        │   ├── SKILL.md
        │   └── SKILL.en.md
        ├── acceptance-verification/
        │   ├── SKILL.md
        │   └── SKILL.en.md
        └── evals/
            └── evals.json         # 測試案例定義
```

> 一般 Skill 也可附 `scripts/`(輔助腳本)與 `assets/`(範本、參考資料);本套件以指示文件為主,故未使用。

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
- **雙語(選用)**:主檔用 `SKILL.md`(維持觸發),另一語言放 `SKILL.en.md` 並於頂部互相連結。

## 新增 Skill

1. 在 `skills/` 下建立資料夾,命名用小寫加連字號(如 `weekly-report`)。
2. 建立 `SKILL.md` 並填入 frontmatter 與指示。
3. 需要的話加入 `scripts/`、`assets/`。
4. 更新本 README 的「Skill 一覽」與「目錄結構」。
5. commit。

## 命名規範

- 資料夾與 `name`:小寫、連字號分隔(kebab-case)。
- 一個 Skill 一個資料夾,職責單一。
