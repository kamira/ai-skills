# Changelog — ai-sdlc

本檔記錄 `ai-sdlc` skill 的版本變更。格式參考 Keep a Changelog;版本採語意化(references 內容微調→patch、新增 reference/機制→minor、流程或契約破壞性改動→major)。tag 採 skill 範圍 `ai-sdlc-vX.Y.Z`。版本號寫於 `skills/ai-sdlc/SKILL.md` 的 `metadata.version`。

## [1.13.0] — 2026-07-03

最後一次行為紀律(見 `docs/ai-sdlc/changes/CHG-20260703-02.md`)。

### Added
- **crash-only 紀律**:每個動作都當作 session 的最後一個——一步一落盤(動手前意圖落盤、做完立刻記結果),禁止批次補記;沒有東西只活在對話裡;正常結束=恰好方便的 crash。handshake 新增紀律節(進場假設由它保證);SKILL 原則 7(日常);cross-agent 交接清單註記「驗證非急救」(離場)。既有點狀機制(步驟勾選、worklog 先寫後做、當場驗收)收攏為本紀律的實例。evals +1(id 25),共 25。

## [1.12.1] — 2026-07-03

### Changed
- **source_quote 棄用**(CHG-lite:`docs/ai-sdlc/changes/CHG-20260703-01.md`):rule 為唯一作用表示;保真=記錄時使用者確認+爭議回問活人+git 歷史;引文是漂移面與 PII 向量。schema 標 deprecated、範例/模板移除;lint 容忍 legacy 條目(prospective)。

## [1.12.0] — 2026-07-03

命中機制(見 `docs/ai-sdlc/changes/CHG-20260702-10.md`)。

### Added
- **命中契約**(knowledge):`tags`=分類軸(受控詞彙、INDEX 主鍵);**`keywords`=命中軸**(schema 新欄,自由語言任何語言——使用者原詞/API 名/錯誤字串,露出為 INDEX 欄位,索引層即可命中);**`docs/knowledge/vocabulary.json`=橋與註冊處**(tag→別名;lint 驗條目 tags ⊆ 詞彙表,擋 tag 增殖;解析失敗 fail-loud;無檔豁免)。命中程序:任務側取鍵→別名正規化→tags 交集+keywords 子串;**召回優先於精準**。
- **未知欄位檢查**(lint):打錯欄名(`taggs`)=資料靜默消失,比照 constraint 擋下——「database-like」的正確拿法:檔名=主鍵、schema=DDL、lint=constraints、INDEX=物化視圖、vocabulary=維度表;儲存引擎維持純文字(git 可合併/AI 直讀/diff 可審計不可退讓),數千條再上衍生查詢快取(backlog)。
- evals +1(id 24),共 24。

## [1.11.0] — 2026-07-03

knowledge 條目正典改 JSON(見 `docs/ai-sdlc/changes/CHG-20260702-09.md`)。

### Added
- **JSON 正典條目**(拆檔模式):`entries/<id>.json`,schema `assets/knowledge_entry.schema.json`(必填 id/tier/rule/tags/status、enum 固定);**fail-loud**——解析不了/不合 schema 擋提交不跳過(靜默少一條規則比擋提交更糟);不用 YAML(隱性轉型 `1.10`→`1.1`、`no`→`false` 正是要消滅的誤讀)、不用 regex 解析 markdown(容錯即誤讀溫床);註解放欄位。單檔 md 模式保留給小專案;過渡期舊 .md 條目仍被讀。
- **分工原則明文**:全量解析屬腳本(index 生成/lint/健康度,模型 context 成本零);模型只讀生成的 INDEX(每條約一行)+ scope 內 3–5 個條目——知識庫越大淨 context 越省;命中 20+ 條=tags 太寬。
- `knowledge_index.py` 讀 JSON(壞檔 SystemExit);lint 新增 `check_knowledge_entries`;health 以結構化方式讀 JSON tier;evals +1(id 23),共 23。

### Fixed
- v1.10 交叉檢查 `file_ids` 只掃 `*.md`,JSON 條目被誤判為缺檔——fixture 抓出並修復。

## [1.10.0] — 2026-07-03

knowledge 規模化與語言正規化(見 `docs/ai-sdlc/changes/CHG-20260702-08.md`)。

### Added
- **拆檔模式**(knowledge):超過 ~30 條 → 一條目一檔 `docs/knowledge/entries/<id>.md`(檔名=id=第一層過濾;失效移 `entries/archive/`)——解單寫者熱點、merge 衝突、計數 diff 噪音。
- **生成式 INDEX**:`scripts/knowledge_index.py` 從條目 metadata 重生 `INDEX.md`(排序:user-confirmed→deep→shallow),**永不手改**;`--check` 驗新鮮;doc-integrity lint 雙向交叉驗「條目檔↔INDEX id」;governance_health 改 rglob 統計 entries/。檢索規則不變、與模式無關。
- **AI-friendly 語言正規化**:tags 一律小寫英文固定詞彙(token/grep/跨模型);規則行祈使句、一條一義、可測試措辭、附正反例;來源引文保留使用者原語言;shallow→deep 升級含語言正規化一次。
- evals +1(id 22),共 22。

## [1.9.0] — 2026-07-02

knowledge 自主觸發與生命週期(見 `docs/ai-sdlc/changes/CHG-20260702-07.md`)。

### Added
- **自主觸發(KN 模式記錄)**:同樣需求/目的第 2 次跨 CHG/需求出現 → AI 自主建 **shallow record**(證據=CHG 編號、計數落在條目內、跨 session);CHG 收尾時比對動機重複(modification-guide);SKILL 偵測表加線索。
- **生命週期單一階梯**:shallow(假說,套用要宣告,一句話可推翻)→ `applied ≥3` 無糾正升 **deep**(預設套用不逐次宣告、ack 列出、仍一句話可推翻)→ 使用者明說才轉 **DIR**(三次確認保護);永不自我升級;deep 被糾正降級留痕,反向規則轉 DIR。取代 v1.4「來源信度」段,一把尺不打架。
- **AI-friendly 檢索(INDEX)**:knowledge 檔首 INDEX(id/tier/tags/一句規則/狀態),條目帶 tags/scope 錨點;進場與派發**只讀索引+全域+scope 相交條目,不讀整份**(handshake 步驟 3 同步改寫)。
- 健康度:knowledge 階梯統計(DIR/deep/shallow;shallow 長期不升不退=review 訊號);evals +1(id 21),共 21。

## [1.8.0] — 2026-07-02

輕的更輕、重的更穩,以風險分級切換(見 `docs/ai-sdlc/changes/CHG-20260702-06.md`)。

### Added
- **新 reference `review-panel`(決策審議會)**:規則多到單 agent 吃不下 → 分席審議,每席只載一個領域(risk/impact/drift/compliance/security/consistency),一行判決(`[verdict]` 格式);**否決制**(硬規則席 fail 派發者不可推翻,推翻走確認閘);**風險縮放開席**(高=全席強制、中=三席、低=不開);**遞迴上捲**(每層:組包/裁決/一行摘要上交;硬 fail 不壓縮直達上層,任何中層不得吞);**降級**=序列自審同格式;判決入 CHG,lint 驗高風險必附。
- **單人快速路徑**(SKILL 明文):solo+白名單低風險=lite+預授權+自驗為**預設**;lite 資格改**白名單制**(文案/註解/樣式/有測試內部重構);**闖禍強制升級**(補完整 CHG+根因入 knowledge+該類預授權自動失效);預授權須窄、用量入健康度、AI 主動建議。
- **只讀自己的職責卡**:被派發 agent 只讀派發包中自己那張職責卡/席位列,完整目錄屬派發者(agent-hierarchy、review-panel)。
- **平台中立**:SKILL 明文全套為 markdown+Python,不限 Claude;`Agent` 工具改寫為「派生能力+平台等效」;遞迴深度上限改「依平台」。
- `role_refs.json` **v3**:六個 `seat-*` 角色;orchestrator 加載 review-panel。
- lint:高風險已實作 CHG 必附審議判決;健康度:lite 佔比、預授權使用次數。
- evals +3(id 18 審議會、19 fast path、20 role 卡範圍讀取),共 20。

## [1.7.0] — 2026-07-02

確認閘與「先問不代決」(見 `docs/ai-sdlc/changes/CHG-20260702-05.md`)。

### Added
- **確認閘**(modification-guide 工作流步驟 6):任何風險等級的變更,動碼前都要把「動機/影響範圍/代決事項/風險分級」摘要給使用者確認;使用者可**預授權**某類變更(記為 knowledge directive)豁免逐次確認;自主連跑走 halt 契約——同一意圖、兩通道(autonomy 註記)。
- **「推不出的先問,不代決」總則**(SKILL 使用原則 6):文件與使用者指示推導不出的抉擇(新需求、範圍外相依、規格空白、兩可裁決)→ 列選項+建議問使用者;僅低風險可逆細節可先做並標「代決」供追認。
- **風險自評補洞**(modification-guide):高風險清單命中即高、不接受自評降級;使用者在確認閘覆核風險欄。
- **evals +2**(id 16 確認閘、id 17 規格空白先問)。

## [1.6.0] — 2026-07-02

十二項優先修正(見 `docs/ai-sdlc/changes/CHG-20260702-04.md`)。

### Added
- **慣例版本遷移**:CHG/ACC 模板加 `Skill: ai-sdlc vX.Y` 欄;doc-integrity 定「新規則只往後適用」(lint 硬性欄僅 v1.0 起即有者,嚴檢走旗標);handshake 加 skill 版本自檢(記錄比 skill 新=skill 過舊先升級)。
- **無 git 降級模式**(handshake):commit 錨定家族不適用時的替代(步驟勾選+worklog 為唯一中斷標記);lint 無 .git/shallow clone 給明確提示。
- **squash / rebase / PR 相容**(modification-guide+handshake):錨定主鍵=message 的 CHG 編號(活得過改寫),hash 盡力而為;squash commit 必帶 CHG 編號、trunk 以 squash 粒度掃描;收尾回填 trunk commit/PR 號。
- **並行實體隔離**(cross-agent):claim=邏輯鎖,真正並行每 agent 各用 git worktree/clone;claim=誰可以做、worktree=在哪做。
- **CHG-lite**(modification-guide):低風險一屏記錄+內嵌自驗取代獨立 ACC(僅限低風險);lint 加豁免(低風險+自驗字樣)。
- **Guideline pivot**(requirement-analysis):major 升版、FR 標棄用不重用、舊 CHG/ACC 對其引用版本仍有效。
- **批次核准**(autonomy):同一 CHG 其餘關卡可一次核准並記錄;永遠停點不可批次;驗收失敗即失效。
- **證據可重跑**(acceptance-verification):證據=指令+關鍵輸出或檔案/行號,敘述性「通過」視同未驗證;迴歸指向用反引號。
- **迴歸腐爛 lint**(doc_integrity_check.py):regression.md 反引號指向的檔案必須存在。
- **健康度閾值→行動**(governance_health.py):`--hanging-max`(3)/`--stale-max`(0)/緊急占比>10% 警示;`--gate` 可變閘門。
- **雙語結構檢查 `scripts/bilingual_check.py`**:en↔zh-tw 每對檔案比對 ##/###/fence 數,只改單邊即抓;首跑本 repo 16 對全平行。
- **evals +6**(id 10–15):中斷恢復、停滯 claim 接管、跨分支撞號合併、緊急通道、範圍握手、暫停交錯——補上 1.3–1.5 新機制的回歸案例。

### Fixed
- 欄位 lint 的 Risk regex 支援 lite 單行式(`| Risk: low |`)——fixture 實測抓出後修正。

## [1.5.0] — 2026-07-02

時間統一與握手分層(見 `docs/ai-sdlc/changes/CHG-20260702-03.md`)。

### Added
- **分層握手(handshake)**:完整握手(單人進場/主 agent/接手整專案/無派發者的對等並行)vs **範圍握手**(被派發的 subagent;四鍵 = branch + 結構位置 + 需求切片 + 鎖定位置)。subagent 只讀主 agent 組的**派發包**+自己範圍,不讀其他分支、其他模組的 claim/worklog;**全域 knowledge 穿透範圍**(唯一例外);scoped ack 回派發者,由其比對四鍵後才准動手;代價與補償控制(影響分析/整合驗收/V1)明文化。agent-hierarchy 上層職責與 I1.x 輸入、cross-agent 對等例外同步。
- **時間慣例 UTC+0**:治理文件一切時間戳(編號/檔名日期、標頭日期、worklog 時刻、claim/租約)一律 UTC+0 且寫明;租約逾期與「同日」序號以 UTC+0 判定。模板(CHG/ACC/knowledge/worklog/claim)標注;`governance_health.py` 改用 UTC 時鐘並在報告標明。

## [1.4.0] — 2026-07-02

九項機制:「掉了也追得回、追得早」(缺口分析與取捨見 `docs/ai-sdlc/changes/CHG-20260702-02.md`)。

### Added
- **commit 錨定**:CHG/ACC 模板加 `Commit/PR` 欄;「commit 粒度」規則(碼+CHG+ACC 同 commit/PR、message 帶 CHG 編號);handshake 加 commit 歷史掃描(錨點→HEAD 未引用 CHG 的 commit=未治理);`doc_integrity_check.py --commits-since`。
- **累積迴歸集**(acceptance-verification):`docs/acceptance/regression.md` 登記歷次 ACC 可腳本化條件;中/高風險驗收必跑受影響範圍,弄壞舊條件=未通過;風險分級表同步。
- **緊急通道**(modification-guide + autonomy):人宣告緊急→先修後補(24h 內追溯 CHG+ACC);違規=不補記,不是用車道;人為宣告即停點核准,契約仍只加嚴。
- **mini-handshake(session 中重新對齊)**:每個 autonomy 關卡、驗收前、察覺壓縮跡象、長 session 定期——重讀 Guideline+進行中 CHG 並發兩行 ack;SKILL 原則 5 掛明確觸發點。
- **文件污染防護**:knowledge 條目加「信度」(使用者確認=拘束力/agent 推斷=建議性、首次套用要說);doc-integrity 清單加「不含 secrets」與「保護名單文件不得默默改」;agent-worklog 加 secrets 消毒。
- **模板 schema lint**(doc_integrity_check.py):CHG/ACC 必填欄檢查(`--require-branch`/`--require-commit` 加嚴;`--no-field-lint`/`--no-secret-scan` 逃生口);docs/ secrets 掃描。
- **決策假設欄**(modification-guide):決策表加「前提假設」;影響分析須查先前 CHG 假設是否被推翻。
- **暫停-恢復協定**:CHG 狀態加「暫停(原因+恢復條件)」;啟動檢查列出、有意識恢復;lint 視暫停為合法 WIP 不判懸空。
- **治理健康度 `scripts/governance_health.py`**:狀態分佈、懸空、暫停、停滯 claim、緊急/文件同步次數、ACC 通過率、迴歸集規模、歸檔量;`--json`;唯讀不設閘門。

### Changed
- `doc_integrity_check.py` 大改版(欄位 lint、暫停狀態、secrets、commit 掃描);fixture 實測通過(髒/淨兩組)。

## [1.3.0] — 2026-07-02

補強「非正常結束」路徑(缺口分析與細節見 `docs/ai-sdlc/changes/CHG-20260702-01.md`)。

### Added
- **working-tree 對帳**:handshake 步驟 1 加 `git status`、步驟 5 加「未提交變更必須對應到某 CHG 的修改步驟,對不上視為漂移」;ack 格式加 worktree 行;SKILL Session 啟動檢查插入同款第 3 步。
- **claim 租約與停滯接管**(cross-agent):claim 是租約非永久佔有;逾時且 worklog/協調檔無更新即為停滯,可留痕接管——解掛掉的 agent 造成的死鎖。並行時建議「一 claim 一檔」避免協調檔本身的競態。
- **跨分支編號與合併規則**(branch-isolation):CHG/ACC 編號只在同分支內唯一,撞號於合併時重編;合併本身開 merge-CHG 並重掛匯入記錄的 Branch 欄;cherry-pick 只帶碼不帶文件=未治理變更,須在目標分支補 CHG;切換分支視同重新進場、重做握手。
- **中斷點標記**(modification-guide):修改步驟模板改 checkbox,每完成一步立刻打勾,勾選狀態即中斷後續作點;觸發清單明列「回滾也是 CHG」。
- **漂移裁決與歸檔**(doc-integrity):新增「以哪邊為準」裁決規則(文件=意圖、程式=現實,追 CHG 鏈決定修正方向,意圖不明問使用者);新增「成長與歸檔」段(收尾記錄歸檔 + INDEX 索引,進場只掃未歸檔)。
- **入口錨點**(SKILL 文件存放慣例):第一次建 `docs/` 時在目標專案 CLAUDE.md / AGENTS.md 加指引,讓不認識本 skill 的 session 也被導入流程。

### Changed
- SKILL 偵測表 handshake 列補「working tree」;啟動檢查由 3 步改 4 步。



### Added
- **進場握手 `handshake`**:每次進場/接手的固定讀取順序(分支 → Guideline → knowledge → coordination → 未收尾 CHG/ACC → 結構)、重點與回述確認格式,讓 AI 一進場就對齊既有約束。
- **修正指示知識庫 `knowledge`**:把「修正指示(非需求變更)」納入知識庫防止再犯;entry 分 error/directive;更新即取代(每條規則僅一個現行版);**高優先權**;與使用者需求衝突時走**三次確認 + 告知影響層面**再依決定,並回寫知識庫。需求變更走 CHG、修正指示走 knowledge。
- **分支隔離 `branch-isolation`**:需求/CHG/ACC 綁定分支;驗證與需求只能引用**當前分支**來源,不得引用其他分支開出的需求;跨分支內容僅在合併時匯入;與 cross-repo 區分。

### Changed
- **結構調整/需求更新後修正 Guideline**:requirement-analysis 加「Guideline 維護(變更後回修)」段;modification-guide 工作流第 4 步改為「同步結構文件 + 回修 Guideline」。
- Guideline / CHG / ACC 模板新增 **Branch 欄**。
- SKILL 偵測即載入表新增三列(進場→handshake、修正/衝突→knowledge、多分支→branch-isolation);`assets/role_refs.json` 升為 v2(common 基本集含 handshake/knowledge/doc-integrity + multi_branch 情境);`scripts/role_loadout.py` 加 `--multi-branch` 並合併 common 集;agent-hierarchy 角色→references 表同步。

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

[1.13.0]: 對應 tag ai-sdlc-v1.13.0
[1.12.0]: 對應 tag ai-sdlc-v1.12.0
[1.11.0]: 對應 tag ai-sdlc-v1.11.0
[1.10.0]: 對應 tag ai-sdlc-v1.10.0
[1.9.0]: 對應 tag ai-sdlc-v1.9.0
[1.8.0]: 對應 tag ai-sdlc-v1.8.0
[1.7.0]: 對應 tag ai-sdlc-v1.7.0
[1.6.0]: 對應 tag ai-sdlc-v1.6.0
[1.5.0]: 對應 tag ai-sdlc-v1.5.0
[1.4.0]: 對應 tag ai-sdlc-v1.4.0
[1.3.0]: 對應 tag ai-sdlc-v1.3.0
[1.2.0]: 對應 tag ai-sdlc-v1.2.0
[1.1.0]: 對應 tag ai-sdlc-v1.1.0
[1.0.0]: 對應 tag ai-sdlc-v1.0.0
