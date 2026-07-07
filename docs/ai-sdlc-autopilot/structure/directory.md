# 目錄結構 — ai-sdlc-autopilot

- 專案:ai-skills / skill: ai-sdlc-autopilot
- 版本:v1.0 | 日期:2026-07-06(UTC+0)

```
skills/ai-sdlc-autopilot/
├── SKILL.md / SKILL.zh-tw.md        # orchestrator:定位、相依宣告、Detect→load、停點總表、NOTICE
├── references/                       # 5 份,各 .md(英)+.zh-tw.md(繁中)結構平行
│   ├── execution-plan               # 計畫格式:Global Constraints + 逐 task Interfaces/test + checkbox
│   ├── tdd-loop                     # 紅綠重構;測試先行;ACC 證據行慣例
│   ├── task-review                  # 每-task 唯讀審查(單 reviewer 雙判定)+ 末端整支 review
│   ├── systematic-debugging         # 連續失敗時的假說→驗證迴圈;根因入 knowledge
│   └── autopilot-loop               # 驅動契約:狀態機、停點查詢、續作、落帳
├── assets/
│   └── autopilot_policy.json        # 風險×階段→auto/confirm/halt;永遠停點清單(不可放寬)
├── scripts/
│   └── autopilot_runner.py          # plan-check / run / status;exit 0/1/2/3;--dry-run
├── evals/evals.json                 # 行為評測案例
└── THIRD-PARTY-NOTICES.md           # Superpowers(MIT © 2025 Jesse Vincent)方法論出處

docs/ai-sdlc-autopilot/               # 本 skill 的治理帳本(repo 慣例:依 skill 分目錄)
├── ai-guideline.md                  # 需求分析產物(v1.0 已確認)
├── structure/{directory,logical,data}.md
├── changes/ · acceptance/           # CHG / ACC
├── knowledge/                       # 先建(空 INDEX 合法)+ vocabulary.json
└── CHANGELOG.md                     # skill 版本記錄(ai-sdlc-autopilot-vX.Y.Z)
```

歸屬原則:**方法論在 references、策略在 assets、機械在 scripts、帳本在 docs/**;plan 不另立目錄——它是目標專案 CHG 的修改指引段(單一帳本,見 logical)。
