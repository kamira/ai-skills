# Changelog — ai-sdlc

本檔記錄 `ai-sdlc` skill 的版本變更。格式參考 Keep a Changelog;版本採語意化(references 內容微調→patch、新增 reference/機制→minor、流程或契約破壞性改動→major)。tag 採 skill 範圍 `ai-sdlc-vX.Y.Z`。版本號寫於 `skills/ai-sdlc/SKILL.md` 的 `metadata.version`。

## [1.1.0] — 2026-06-18

### Added
- **角色職責目錄(role catalog)**:agent-hierarchy 內每個角色(orchestrator / A1 分析 / I1 實作主 / I1.x 實作子 / V1 驗收 / 整合者 / 審閱者)的職責、輸入、輸出、可做/不可做、對應階段、交給誰。
- **角色 → references 子集(機器可讀)**:`assets/role_refs.json`(角色基本載入集 + 情境追加 + 別名)、`scripts/role_loadout.py`(查詢)、agent-hierarchy 內對應人類視圖表(註明 JSON 為單一真相)。

### Changed
- `docs/` 與 `examples/` 改為依 skill 分目錄(`docs/ai-sdlc/`、`examples/ai-sdlc/`),因 repo 不限於 ai-sdlc;cross-repo 指引與範例內相對路徑同步更新。
- tag 命名改為 skill 範圍:原 `v1.0.0` 正名為 `ai-sdlc-v1.0.0`。

## [1.0.0] — 2026-06-17

首個正式版:由「單人版 + 團隊版兩個 skill」**合併為單一自適應 skill**(偵測到協作/多 repo/多 agent 自動升級;使用者可覆寫)。

### 核心
- 四階段流程:requirement-analysis → structure-design → modification-guide → acceptance-verification(含未通過回修迴圈、當場驗收不可交棒)。
- 抗 session 壓縮:Session 啟動檢查 + 「不倚賴記憶,以文件為準」。
- 偵測即載入(detect→load):依情境自動載入對應 reference;硬化偵測線索防漏報。

### references(12)
requirement-analysis、structure-design、modification-guide、acceptance-verification、doc-integrity、agent-worklog、agent-hierarchy、cross-repo、cross-agent、independent-acceptance、autonomy、ci-cd。

### 機制與腳本
- 抗漂移:`doc_integrity_check.py`(結構同步 + CHG↔ACC 連結)。
- 跨 repo:權威來源 + 本地指標 + XCHG + `cross_repo_check.py`。
- 自主停點契約:`halt_policy.json` + `halt_gate.py`(風險×關卡→auto/halt + 永遠停點動作)。
- 風險分級 × 身分檢查(驗收者 ≠ 實作者)× 跨模型審查。
- 子代理工作日誌 + 錯誤知識庫;代理編制(編號/固定範圍/不越權/遞迴授權)。
- CI/CD(選用):pre-commit + pipeline 門檻。
- 雙語(`.md` 英文 / `.zh-tw.md` 繁中);發佈 `dist/ai-sdlc.skill`、`ai-sdlc.zh-tw.skill`。
- 回歸集 `evals/evals.json`(skilltest)。

[1.1.0]: 對應 tag ai-sdlc-v1.1.0
[1.0.0]: 對應 tag ai-sdlc-v1.0.0
