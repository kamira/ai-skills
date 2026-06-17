---
name: ci-cd
description: >
  選用:把 ai-sdlc 的文件治理接上 CI/CD,讓「文件即真實」由機器強制而非僅靠自律。當團隊專案
  有或要導入 CI/CD(GitHub Actions / GitLab CI / Jenkins 等)、想把驗收與結構一致性變成 PR 門檻
  時讀本檔。涵蓋治理產物對應自動化門檻、建議 gates 與平台中立範例。沒有 pipeline 的專案可略過。
---

# ci-cd(選用)— 把治理流程接上 CI/CD

> 語言 / Language: **繁體中文** · [English](ci-cd.md)

## 用途(選用)

若團隊專案有 CI/CD,把 ai-sdlc 的文件治理變成**自動化門檻**,讓「文件即真實」「每次變更留痕」「驗收對齊來源」由機器強制,而非只靠每個人自律。**沒有 pipeline 的小專案可略過本檔**,靠 ai-sdlc 流程自律即可。

## 何時讀

- 團隊專案已有或要導入 CI/CD
- 想把驗收、結構一致性變成 merge / PR 的門檻
- 多人/多 agent 協作,需要機器把關以免有人略過治理

## 治理產物 → 自動化門檻 對應

| ai-sdlc 產物 | CI/CD 對應 |
|--------------|-----------|
| 驗收條件(Guideline §7 / ACC) | 自動化測試;CI 跑測試作為門檻 |
| 變更記錄 CHG | PR 模板必填;PR 描述須連結對應 CHG |
| 結構文件 `docs/structure/` | 結構漂移檢查(見下) |
| 驗收報告 ACC | merge 門檻:無對應且通過的 ACC 不可合併 |

## 建議 gates(由寬到嚴,依團隊需要選用)

1. **測試必綠**:對應驗收條件,最基本。
2. **PR 必連 CHG**:PR 描述要含 `CHG-` 參照(對應「每次變更留痕」)。
3. **結構同步檢查**:若這次改了結構性程式(如 `src/models/**`、schema)卻沒同步 `docs/structure/`,警告或擋下(對應「文件即真實」)。
4. **驗收門檻**:存在對應本次變更、且結論為「通過」的 ACC,才可合併(對應「當場驗收」)。

導入時建議**從寬到嚴**:先上「測試必綠 + PR 連 CHG」,團隊習慣後再加結構同步與 ACC 門檻,避免一次太嚴卡住流程。

## 平台中立範例(pseudo)

以下為概念示意,可翻成任何 CI 平台(GitHub Actions / GitLab CI / Jenkins…)的等義設定:

```yaml
on: pull_request
jobs:
  governance:
    steps:
      - run: <跑測試>                      # gate 1:測試必綠
      - check: PR 描述含 "CHG-"             # gate 2:變更留痕
      - check: 若 changed_files 命中 src/models|schema 等結構性路徑,
               則 docs/structure/ 必須也有變更                # gate 3:結構同步
      - check: docs/acceptance 內存在對應本次 CHG 且結論=通過的 ACC  # gate 4:驗收門檻
```

GitHub Actions 對應做法舉例:用 `on: pull_request` 觸發;`gate 1` 跑測試步驟;`gate 2/3/4` 用一個腳本讀 PR body 與 `git diff --name-only` 比對路徑、並 grep `docs/acceptance/` 對應檔,任何一項不過就讓該 step 退出非零碼擋下合併。其他平台(GitLab CI 的 `rules` / Jenkins 的 stage)概念相同。

## 與既有流程的關係

CI/CD **不取代治理,而是強制治理被遵守**。ai-sdlc 定義「該產出什麼文件、該怎麼驗收」;本檔把這些變成機器可檢查的門檻。團隊版尤其需要它——人一多,光靠自律不可靠。選用:沒有 pipeline 時,靠 ai-sdlc 與 cross-agent 的流程自律即可。
