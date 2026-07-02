---
name: handshake
description: >
  進場握手協定:每個 agent / session / 換手在動手前,先做一次「握手」——按固定順序讀既有 docs、
  抓出重點、並回述確認理解,才能安全接手。當你剛進場、接手既有專案、或跨 session/跨 agent 交接時
  讀本檔。定義讀什麼、順序、重點、以及進場回述(ack)格式。是 Session 啟動檢查的具體化。
---

# handshake — 進場握手協定

> 語言 / Language: **繁體中文** · [English](handshake.md)

## 用途

任何 agent 一進場(新 session、接手、換手)都先做「握手」:**按固定順序讀既有文件 → 抓重點 → 回述確認**,再開始工作。目的是讓交接可稽核、避免「沒讀就動手」造成的漂移與誤解。這是 Session 啟動檢查的可執行版。

## 從哪讀(固定順序)

1. **當前分支**:先確認在哪個 branch(見 branch-isolation);後續只引用該分支的需求/驗收。
2. **`docs/ai-guideline.md`**:現行 Guideline——目標、範圍、現行**版本號**、待確認項。
3. **`docs/knowledge/`**:已知錯誤與**使用者修正指示**(見 knowledge)——避免重犯;高權重。
4. **`docs/coordination.md`**:編制/claim——我的角色、鎖定範圍、讀寫權限、進行中的他人工作。
5. **`docs/changes/` + `docs/acceptance/`**:有無未收尾(CHG 未驗收 / 缺 ACC);先補再開新。
6. **`docs/structure/`**:現況結構,判斷是否與程式漂移(見 doc-integrity)。

## 重點(務必抓到)

- **當前分支** 與其範圍(不可引用其他分支需求)。
- **現行 Guideline 版本** 與待確認項。
- **我的角色 / 讀寫權限**(role_refs、tools allowlist)。
- **已知錯誤與修正指示**(knowledge,高權重)。
- **未收尾階段**(懸空的驗收)。
- **進行中的 claim**(避免撞車)。

## 回述確認(handshake ack — 動手前必做)

進場讀完後,**先用幾行回述你理解的狀態,再動手**:

```
[handshake] 分支:<branch> | 角色:<role>(RW:<scope>)
現行 Guideline:v<x>;未收尾:<CHG-… 待驗收 / 無>
已知須遵守(knowledge):<重點條目 / 無>
我接下來要做:<一句話>;停點:<依 autonomy,此關卡 auto/halt>
```

回述能讓人/上層在你動手前攔截誤解;跨 agent 時,這也是「我已正確接手」的憑證。

## 與既有流程的關係

- 具體化 Session 啟動檢查;讀取項對應 knowledge / branch-isolation / doc-integrity / coordination / autonomy。
- 機器輔助:用 `scripts/role_loadout.py` 取得該角色要載的 references;用 `scripts/doc_integrity_check.py` 掃未收尾與漂移。
- 讀到未收尾/漂移/衝突 → 依對應 reference 先處理,再開始新需求。
