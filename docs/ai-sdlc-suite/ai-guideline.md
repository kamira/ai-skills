# AI Guideline — ai-sdlc-suite(一鍵大補帖:plugin + MCP + hooks + CI)

- 專案:ai-skills / ai-sdlc-suite(整合發佈層,非新 skill)
- 分支(Branch):claude/quirky-margulis-cad156
- 版本:v1.0
- 日期:2026-07-07
- 狀態:已確認(使用者:「MCP + hook 為選配 如果能像superpower那樣一整包的大補帖也行」)

## 1. 背景與目標

核心契約(兩個 skill)已平台中立,但強制層與供給層尚未接線:lint 無 CI 接線、session 內無即時強制(hook)、無 shell 的 agent 接不上(MCP)。目標:比照 Superpowers 的發佈型態,把「ai-sdlc + ai-sdlc-autopilot + MCP server + hooks + CI 範本」打包成 **Claude Code plugin(marketplace 直裝)**;MCP 與 hook 為**選配適配層**——不裝也不影響核心契約運作。

## 2. 範圍

### 納入
- 本 repo 成為 plugin marketplace(root `.claude-plugin/marketplace.json`);plugin `plugins/ai-sdlc-suite/`
- MCP server(stdio、stdlib):governance_health / doc_integrity_check / plan_check / halt_gate / knowledge_search 五工具
- Claude Code hooks ×3(選配,預設 warn 模式):SessionStart 握手提醒、PreToolUse 未開 CHG 編修警示、Stop 懸空驗收攔截
- CI 範本(pre-commit + GitHub Actions)供目標專案複製;**本 repo 自身接上 governance workflow(dogfood)**
- build_suite.py:發版時同步兩個 skill 複本進 plugin(同 dist 慣例:單一真相在 skills/,plugin 為建置產物)

### 不納入(明確排除)
- 不改兩個 skill 本體;不強制 hook(warn 為預設,block 需 env 顯式開啟)
- SQLite FTS 快取(knowledge 條目未達門檻,留待 MCP v2)
- 非 Claude Code 平台的 hook 對應(MCP 與 CI 已跨平台)

## 3. 利害關係人
| 角色 | 關注點 |
|------|--------|
| 使用者 | 一鍵安裝;選配可關;不被 hook 干擾正常工作 |
| 無 shell 的 agent | 經 MCP 取得治理能力(lint/health/knowledge 檢索) |
| 目標專案 | CI 範本即複製即用;lint 從「存在」變「執行」 |

## 4. 功能需求
| 編號 | 需求 | 優先級 | 備註 |
|------|------|------|------|
| FR-1 | marketplace + plugin 清單:`/plugin marketplace add kamira/ai-skills` 後可 `/plugin install ai-sdlc-suite` | P0 | 兩 skill 隨 plugin 載入 |
| FR-2 | MCP server 五工具,newline-delimited JSON-RPC stdio,stdlib-only | P0 | knowledge_search 原生實作(vocabulary 正規化+tags 交集+keywords 子串) |
| FR-3 | hooks 三支,warn/block/off 三模式(env `AI_SDLC_HOOK_MODE`,預設 warn),內部錯誤一律 exit 0 | P0 | Stop 攔截需防迴圈(stop_hook_active) |
| FR-4 | CI 範本 ×2 + 本 repo `.github/workflows/governance.yml`(bilingual+py_compile+JSON+plan-check) | P0 | dogfood:lint 接線缺口在本 repo 先補 |
| FR-5 | build_suite.py 同步 skills 複本入 plugin(排除 __pycache__),可重跑 | P0 | plugin 內容=建置產物,單一真相不變 |

## 5. 非功能需求
| 類別 | 要求 |
|------|------|
| 選配性 | 不裝 plugin/不開 hook/不接 MCP,核心 skill 照常運作 |
| 安全 | hooks 不做網路呼叫、<200ms 快路徑;MCP 工具唯讀(不寫任何檔) |
| 可維護性 | 全 stdlib;MCP server 單檔;hooks 各 <120 行 |
| 授權 | 大補帖概念致敬 Superpowers(方法論出處聲明已在 autopilot skill 內) |

## 6. 限制與假設
- 假設:Claude Code plugin 格式(.claude-plugin/plugin.json + hooks/hooks.json + .mcp.json + skills/)
- 限制:hook 僅 Claude Code 生效;其他平台以 MCP+CI 補位
- 待確認:無

## 7. 驗收條件
- [ ] AC-1 MCP smoke:initialize → tools/list(5 工具)→ tools/call(governance_health、knowledge_search、halt_gate)回有效 JSON
- [ ] AC-2 hooks smoke:三支以合成 stdin JSON 執行皆 exit 0;pre_edit_gate 在 block 模式對「受治理 repo+無進行中 CHG」回 deny、warn 模式回 systemMessage;stop_closeout 對 stop_hook_active=true 直接放行
- [ ] AC-3 build_suite 同步後 plugin/skills 兩複本齊(bilingual_check 對複本仍過);重跑冪等
- [ ] AC-4 manifests JSON valid;README 收錄安裝法;本 repo governance workflow 語法有效(YAML 可載入)
- [ ] AC-5 py_compile 全部新 python OK;核心 skill 檔案零改動(git diff 確認)

## 8. AI 開發約定
- 治理文件在 `docs/ai-sdlc-suite/`;knowledge 隨本 Guideline 同步建立(先建規則)
- 後續修改走 modification-guide;commit 帶 `ai-sdlc-suite CHG-…` 前綴;UTC+0
