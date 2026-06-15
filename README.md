# AI Skills

整理與管理自建 AI Skills 的 repo。每個 Skill 是一個獨立資料夾,內含 `SKILL.md` 與相關資源,可被 Claude / Cowork 等代理工具載入使用。

## 什麼是 Skill

Skill 是一包可重複使用的能力:用自然語言寫成的指示、流程與資源檔。當使用者的需求符合 Skill 的觸發條件時,代理會載入該 Skill 的 `SKILL.md`,依其指示完成任務。

## 目錄結構

```
ai-skills/
├── README.md          # 本文件
└── skills/            # 所有 Skill 放這裡
    └── <skill-name>/
        ├── SKILL.md   # 必要:Skill 的說明與指示
        ├── scripts/   # 選用:輔助腳本
        └── assets/    # 選用:範本、參考資料
```

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

## 新增 Skill

1. 在 `skills/` 下建立資料夾,命名用小寫加連字號(如 `weekly-report`)。
2. 建立 `SKILL.md` 並填入 frontmatter 與指示。
3. 需要的話加入 `scripts/`、`assets/`。
4. commit。

## 命名規範

- 資料夾與 `name`:小寫、連字號分隔(kebab-case)。
- 一個 Skill 一個資料夾,職責單一。
