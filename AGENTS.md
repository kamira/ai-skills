# AGENTS.md — AI entry point(任何 agent、任何廠商 / any agent, any vendor)

本 repo 收 AI skills;每個 skill 的治理記錄在 `docs/<skill>/` 底下(本 repo 慣例,取代預設的 root `docs/`)。

1. **動任何東西之前必讀**:`skills/ai-sdlc/SKILL.md`(治理流程本體)→ `docs/ai-sdlc/CHANGELOG.md` → `docs/ai-sdlc/knowledge/`(讀 INDEX,只載 scope 內條目)→ `docs/ai-sdlc/changes/`(未收尾 CHG 先處理)。
2. **單一真相**:skill 內容在 `skills/ai-sdlc/`(雙語成對:`.md` 英 / `.zh-tw.md` 繁中,必須同步;`scripts/bilingual_check.py` 驗證)。`dist/` 為打包產物,發版時重建。
3. **不可協商**:任何修改先開 CHG(`docs/ai-sdlc/changes/CHG-YYYYMMDD-NN.md`)再動手;commit message 帶 CHG 編號;同輪產出 ACC 收尾;時間一律 UTC+0。
