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
| **ai-sdlc-autopilot** | 受治理的自動駕駛執行層(橋接 ai-sdlc):計畫(全域約束+逐 task 介面)→ 逐 task TDD+唯讀審查 → 驗收 → PR →(依風險)merge;停點由風險分級驅動,永遠停點不代行;附無 LLM 的 runner(plan-check/run/status,exit code 可接 cron/CI)。硬相依 ai-sdlc ≥ v1.17;方法論改寫自 Superpowers(MIT,出處聲明見 skill 內)。 | [`skills/ai-sdlc-autopilot/SKILL.md`](skills/ai-sdlc-autopilot/SKILL.md) |
| **intel-analysis** | 情報分析方法論(自 Notion 保真遷移,繁中):從利益到行動的十步驟框架(SKILL-01〜12)+ 六個擴展模組(定量/敘事/制度/歷史類比/供應鏈/長期趨勢)+ 機率分布工程與跨家族遷移測試;23 條核心紀律;**檔案化預測驗證帳本**(一鏈版本一 JSON 快照,`prediction_lint.py` fail-loud 驗證+INDEX 生成,`brier_report.py` Brier 校準)。 | [`skills/intel-analysis/SKILL.md`](skills/intel-analysis/SKILL.md) |

**單一 skill,自適應單人/團隊**:不需選版本。**自主偵測為預設、使用者可選擇或覆寫**——偵測到多 repo 就載 `cross-repo`、並行/交接就載 `cross-agent`、要派子代理就載 `agent-worklog`/`agent-hierarchy`、提出修改就載 `modification-guide`……;使用者明示時以明示為準(如「強制團隊模式」「這次不要 CI/CD」)。

references(16 份,依偵測/選擇載入):

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
| ✦ 審議會 [`review-panel`](skills/ai-sdlc/references/review-panel.md) | 中高風險決策審議:高=全席、中≥5 席(能 spawn 時);先獨立後交叉、跨模型分散、歧異調和或上呈、否決制 |
| ✦ 自主停點 [`autonomy`](skills/ai-sdlc/references/autonomy.md) | 自主執行的停點契約:風險×關卡→auto/halt + 永遠停點動作;附 `halt_gate.py` 與 `halt_policy.json` |
| ✦ CI/CD [`ci-cd`](skills/ai-sdlc/references/ci-cd.md)(**選用**) | pre-commit 初步檢查 + pipeline 權威門檻;含風險分級與身分檢查 gate |
| ✦ 進場握手 [`handshake`](skills/ai-sdlc/references/handshake.md) | 每次進場/接手的讀取順序(分支→Guideline→knowledge→coordination→CHG/ACC→結構)與回述確認 |
| ✦ 知識庫 [`knowledge`](skills/ai-sdlc/references/knowledge.md) | 修正指示納庫防再犯;更新即取代(每規則一現行版);高優先權;與需求衝突→三次確認+告知影響 |
| ✦ 分支隔離 [`branch-isolation`](skills/ai-sdlc/references/branch-isolation.md) | 需求/CHG/ACC 綁定分支;只採當前分支來源、不跨分支引用;僅在合併時匯入 |

> 抗 session 壓縮:含「Session 啟動檢查 + 不倚賴記憶以文件為準」。跨專案/跨 repo:Guideline/CHG/ACC 標頭有「專案」欄;跨 repo 用權威來源 + XCHG 協調。風險分級:CHG/ACC 有風險欄,驅動驗收與 CI 門檻嚴格度。

可安裝版在 [`dist/`](dist/):`ai-sdlc.skill`(英文)、`ai-sdlc.zh-tw.skill`(繁中)。

## 一鍵大補帖(Claude Code plugin)

比照 Superpowers 的發佈型態,本 repo 是 plugin marketplace,目前兩個大補帖:

```
/plugin marketplace add kamira/ai-skills
/plugin install ai-sdlc-suite@ai-skills      # 開發治理:兩個 skill + MCP 五工具 + hooks(warn/block/off)+ CI 範本
/plugin install intel-analysis@ai-skills     # 情報分析:十步驟框架 + 23 紀律 + 檔案化預測帳本(Brier 校準)
```

**MCP 與 hooks 皆選配**——不裝也不影響核心契約在任何平台運作。詳見 [`plugins/ai-sdlc-suite/README.md`](plugins/ai-sdlc-suite/README.md) 與 [`plugins/intel-analysis/README.md`](plugins/intel-analysis/README.md)。plugin 內 skills 為建置複本(單一真相在 `skills/`,由 `plugins/build_suite.py` 依 PLUGINS 對照表同步;CI 驗同步)。

## 目錄結構

```
ai-skills/
├── README.md                      # 本文件
├── AGENTS.md                      # AI 進入點(root 錨點:必讀順序+不可協商規則,任何廠牌 agent 適用)
├── .claude-plugin/marketplace.json # plugin marketplace 清單(→ plugins/ai-sdlc-suite)
├── .github/workflows/governance.yml # 本 repo 治理 CI(雙語/py_compile/JSON/plan-check/複本同步)
├── plugins/                       # 一鍵大補帖(Claude Code plugin)
│   ├── ai-sdlc-suite/             # skills 複本(建置產物)+ mcp/(五工具 server)+ hooks/(warn|block|off)+ ci-templates/
│   └── build_suite.py             # 同步 skills 複本進 plugin(--check 供 CI 驗同步)
├── .gitignore                     # 排除評測產物等
├── dist/                          # 可安裝的 .skill 發佈版
│   ├── ai-sdlc.skill / .zh-tw.skill            # 英文 / 繁中
│   └── ai-sdlc-autopilot.skill / .zh-tw.skill  # autopilot 英文 / 繁中
├── docs/ai-sdlc-autopilot/        # autopilot 治理帳本(Guideline/structure/changes/acceptance/knowledge/CHANGELOG)
├── docs/ai-sdlc/                  # 治理與說明文件(非 skill 內容,不入封裝;依 skill 分目錄)
│   ├── CHANGELOG.md               # 版本變更記錄(ai-sdlc-vX.Y.Z)
│   ├── changes/                   # 變更記錄 CHG-YYYYMMDD-NN.md(本 repo 自身受治理)
│   ├── acceptance/                # 驗收報告 ACC-YYYYMMDD-NN.md
│   ├── knowledge/                 # 知識庫(INDEX + vocabulary.json;KN/DIR 條目)
│   ├── role-chart.svg             # 角色圖
│   └── evaluation-summary.md      # 評測總結(iteration/loop/壓縮/團隊/編制)
├── examples/ai-sdlc/              # 範例(依 skill 分目錄)
│   └── cross-repo/                # 跨 repo 範本專案(authority + 2 消費 repo + XCHG)
└── skills/                        # 每個 skill 一個子目錄(本 repo 不限於 ai-sdlc)
    ├── ai-sdlc-autopilot/         # 受治理自動駕駛(執行層+驅動層;硬相依 ai-sdlc)
    │   ├── SKILL.md / SKILL.zh-tw.md
    │   ├── references/            # 5 份雙語:execution-plan · tdd-loop · task-review · systematic-debugging · autopilot-loop
    │   ├── assets/autopilot_policy.json        # 風險×階段停點矩陣(永遠停點硬清單)
    │   ├── scripts/autopilot_runner.py         # 驅動器:plan-check / run / status(exit 0/1/2/3)
    │   ├── evals/evals.json
    │   └── THIRD-PARTY-NOTICES(.zh-tw).md      # Superpowers MIT 出處
    └── ai-sdlc/                   # 單一 skill(自適應單人/團隊)
        ├── SKILL.md / SKILL.zh-tw.md       # orchestrator(英文 / 繁中)
        ├── scripts/
        │   ├── bilingual_check.py          # 雙語成對結構檢查(.md ↔ .zh-tw.md)
        │   ├── cross_repo_check.py         # 跨 repo 指標漂移檢查(可接 pre-commit/CI)
        │   ├── doc_integrity_check.py      # 文檔抗漂移 7 項機器檢查:結構同步、CHG↔ACC、欄位、secrets、commit 錨定、knowledge bootstrap、重複性檢查欄(可接 pre-commit/CI)
        │   ├── governance_health.py        # 治理健康度報告(唯讀非閘門:懸空/暫停/通過率/knowledge 階梯/警示)
        │   ├── halt_gate.py                # 自主停點查詢:風險×關卡→AUTO/HALT
        │   ├── knowledge_index.py          # knowledge 拆檔模式的 INDEX 生成與 --check 驗新鮮
        │   └── role_loadout.py             # 角色→該載入 references 子集查詢
        ├── assets/
        │   ├── halt_policy.json            # 停點契約(可編輯)
        │   ├── knowledge_entry.schema.json # knowledge JSON 條目 schema(拆檔模式,fail-loud 驗證)
        │   └── role_refs.json              # 角色→references 對應(程式可讀單一真相)
        ├── references/                     # 16 份,各檔 .md(英文)+ .zh-tw.md(繁中):
        │   ├── requirement-analysis · structure-design · modification-guide · acceptance-verification
        │   ├── doc-integrity(抗漂移)· agent-worklog(子代理日誌+錯誤知識庫)
        │   ├── agent-hierarchy(代理編制階層)· cross-repo(跨 repo)
        │   ├── cross-agent(跨 agent 協作交接)· independent-acceptance(獨立驗收)
        │   ├── autonomy(自主執行停點契約)· ci-cd(選用:pre-commit + pipeline)
        │   ├── handshake(進場握手)· knowledge(修正指示知識庫)
        │   ├── review-panel(風險×席次審議會)
        │   └── branch-isolation(分支隔離)
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
