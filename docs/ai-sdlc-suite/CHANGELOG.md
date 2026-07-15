# Changelog — ai-sdlc-suite(plugin)+ marketplace catalog

本檔記錄 `ai-sdlc-suite` plugin 與 **marketplace catalog**(`.claude-plugin/marketplace.json` 的 `metadata.version`)的版本。plugin 版本寫於 `plugins/ai-sdlc-suite/.claude-plugin/plugin.json`。

> **發佈鐵律**:任何 `plugins/**` 或 `skills/**`(被 bundle 的 skill)實質變動,**必同步 bump catalog `metadata.version`**——否則 client 認定目錄無變更、不重抓新版(「plugin 無法更新」)。由 `plugins/catalog_check.py` 於 CI 機械強制(非散文期望)。

## catalog 1.2.0 — 2026-07-15

catalog 版本一致性修正 + 機械強制(見 `docs/ai-sdlc-suite/changes/CHG-20260715-01.md`)。

- **修正**:marketplace `metadata.version` 自建立起凍在 1.0.0,期間 plugin 已到 1.1.0/1.2.0——client 因此無法偵測更新。bump 至 1.2.0。
- **新增機械強制**:`plugins/catalog_check.py`(`--check` 靜態:semver + 每 plugin entry.version==plugin.json;`--since REF` git:plugins/skills 變動則 catalog 必 bump);接入 governance CI。
- 補建本 CHANGELOG(plugin 版號原無對應記錄)。

## plugin [1.1.0] — 2026-07-15

隨 `ai-sdlc-autopilot` skill 升 1.1.0(實際操作驗收閘,見 `docs/ai-sdlc-autopilot/CHANGELOG.md` 1.1.0)。suite bundle 的 autopilot 內容變動 → plugin 1.0.0→1.1.0。

## plugin [1.0.0] — 2026-07-07

首發(見 `docs/ai-sdlc-suite/changes/CHG-20260707-01.md`)。

- 一鍵大補帖:bundle `ai-sdlc`(治理)+ `ai-sdlc-autopilot`(自動駕駛)兩個 skill 的建置複本 + MCP server(五個唯讀治理工具)+ hooks(warn/block/off)+ CI 範本。
- 後續 suite 帳本內部調整:CHG-20260707-02(build_suite 多 plugin 化 + marketplace 收錄 intel-analysis)、CHG-20260707-03(CI plan-check 僅適用計畫格式 CHG)——皆未動 plugin 對外版本。
