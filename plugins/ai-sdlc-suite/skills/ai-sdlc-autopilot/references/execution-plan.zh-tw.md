---
name: execution-plan
description: >
  autopilot 的可執行計畫格式:一個約束所有 task 的全域約束塊,加上逐 task 的介面行
  (consumes/produces)與 test 行,以 checkbox 追蹤。計畫寫在目標專案的 CHG(修改指引段)
  ——永不另立檔案。撰寫或驗證計畫時、第一個 task 施工前讀本檔。
---

# execution-plan — 機器能駕駛的計畫

> 語言 / Language: **繁體中文** · [English](execution-plan.md)

## 為什麼是這個格式

計畫能驅動自動駕駛,前提是每個 task **可獨立執行、可獨立檢核**:一個只看到「全域約束+單一 task 條目」的 agent 要能把它做出來;一個只看到「同一份簡報+diff」的 reviewer 要能判定它。散文計畫(「然後改善 API」)兩項都不及格。

## 格式(寫在 CHG 的修改指引段內)

```markdown
### Global Constraints(全域約束——每個 task 都要遵守)
- <可測試措辭的約束——「一律 X」,絕不是「盡量 X」>

### Tasks(checkbox=續作點)
- [ ] T1. <標題>
  - interfaces: consumes <輸入/前置> / produces <輸出/交付>
  - test: <驗證方式——指令或可斷言條件>
- [ ] T2. ...

### Acceptance operation(末端操作測試——程式類變更必附)
- operate: <怎麼把變更真的跑起來/操作——指令或步驟>
- observe: <什麼可觀察行為確認可用>
- pass: <通過標準>
```

**純文件 CHG** 無可操作面時,整節改為一行標頭欄:`Acceptance-operation: n/a (docs-only)`。

## 規則(plan-check 機器強制)

- 必有 **Global Constraints** 節。版本下限、命名規則、精確值都放這——任何約束*每個* task 的東西。把適用的 knowledge 全域條目與 Guideline 約束摺進來,讓 task 簡報自包含。
- 每個 task 必帶 **`interfaces:` 行**(消耗什麼、產出什麼——task 可組合、可審查的關鍵)與 **`test:` 行**(指令或可斷言條件;純文件 task 改寫可重跑的檢核)。
- Task 編號 **T1..Tn 連續**;每個 task 的大小以一次 agent 執行可完成為準(夠小;若一個 task 需要自己的計畫,就是太大——拆)。
- 勾選在 **task 通過 review 的當下**寫入——它們是任何中斷後的續作點(crash-only 紀律)。
- **`### Acceptance operation`** 宣告末端操作測試(`operate`/`observe`/`pass`)。這**不是** task 級 `test:` 行——task 測試是單元/build 級,這一個把整個變更真的跑一次。plan-check 只在缺它時*提示*(非阻斷);**run** 階段的操作驗收才強制(程式 CHG 缺它又無 `docs-only` 標記,會在驗收前停——見 autopilot-loop)。

## 與帳本的關係

計畫**就是** CHG 的修改步驟——一份產物、一個真相。plan-check(`autopilot_runner.py plan-check`)是機器閘;過不了的計畫永遠不會開跑(exit 2)。
