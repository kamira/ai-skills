# ai-sdlc-suite — 一鍵大補帖

把 **ai-sdlc**(治理)+ **ai-sdlc-autopilot**(自動駕駛執行)+ **MCP server** + **hooks** 打包成一個 Claude Code plugin。MCP 與 hooks 皆為**選配**:不啟用時,兩個 skill 的核心契約(純 markdown+Python)照常運作於任何平台。

## 安裝(Claude Code)

```
/plugin marketplace add kamira/ai-skills
/plugin install ai-sdlc-suite@ai-skills
```

裝完即得:兩個 skill(隨 plugin 載入)、MCP server `ai-sdlc`(自動註冊)、三支 hooks(預設 warn 模式)。

## 內容物

| 元件 | 路徑 | 選配? |
|------|------|-------|
| ai-sdlc skill(治理) | `skills/ai-sdlc/` | 核心(建置複本;單一真相在 repo 頂層 `skills/`) |
| ai-sdlc-autopilot skill | `skills/ai-sdlc-autopilot/` | 核心(同上) |
| MCP server(五工具,唯讀) | `mcp/ai_sdlc_mcp.py` + `.mcp.json` | ✅ 選配 |
| hooks ×3 | `hooks/` | ✅ 選配(預設 warn) |
| CI 範本 | `ci-templates/` | ✅ 複製到目標專案用 |

## MCP 工具(全部唯讀)

- `governance_health` — 治理健康度(JSON)
- `doc_integrity_check` — 文檔抗漂移 lint
- `plan_check` — autopilot 計畫格式驗證
- `halt_gate` — 自主停點查詢(AUTO/HALT)
- `knowledge_search` — 知識庫範圍檢索(vocabulary 正規化 + tags 交集 + keywords 子串)

## Hooks 模式(env `AI_SDLC_HOOK_MODE`)

| 模式 | 行為 |
|------|------|
| `warn`(預設) | 只提示不阻擋:SessionStart 注入握手提醒;PreToolUse 對「受治理 repo 無進行中 CHG 的程式編修」發警示;Stop 提醒懸空驗收 |
| `block` | PreToolUse 直接擋下未治理編修;Stop 攔一次要求同輪收尾(防迴圈:第二次放行) |
| `off` | 全部靜默 |

Hooks 內部錯誤一律放行(exit 0)——治理工具自己不能成為故障點。

## CI 範本

`ci-templates/pre-commit-config.yaml` 與 `ci-templates/governance.yml`(GitHub Actions)——複製到目標專案,把 lint 從「存在」變「執行」。路徑假設 skill 位於 `skills/ai-sdlc/`,不同時改註解標示的兩處。

## 重建 plugin 內 skill 複本(維護者)

```
python3 plugins/build_suite.py   # 從 repo 頂層 skills/ 同步,冪等
```
