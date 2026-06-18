# 跨 repo 範本專案 (cross-repo template)

示範 `ai-sdlc` 的 cross-repo 機制:**權威來源 + 本地指標 + XCHG 協調變更 + 漂移檢查**。可直接複製當起點。

```
examples/cross-repo/
├── manifest.json                         # 給 cross_repo_check.py 用:authority + repos
├── authority-repo/                       # 權威:持有跨 repo 契約(單一真相)
│   └── docs/
│       ├── contracts/VERSION             # 目前契約版本(如 v3)
│       ├── contracts/api-contract.md     # 共用契約內容
│       └── changes/XCHG-20260617-01.md   # 跨 repo 協調變更(範例)
├── repoA/docs/authority.md               # 消費端指標:釘住 authority 版本
└── repoB/docs/authority.md               # 消費端指標:釘住 authority 版本
```

## 跑漂移檢查

```bash
python3 ../../../skills/ai-sdlc/scripts/cross_repo_check.py manifest.json
```

- 全部 repo 指標 == 權威版本 → 退出碼 0。
- 把 `authority-repo/docs/contracts/VERSION` 改成新版本(模擬契約升級),但某個 repo 的 `docs/authority.md` 沒跟上 → 該 repo 被標為漂移,退出碼 1(可接 pre-commit / CI 擋下)。

## 流程(契約變更時)

1. 權威先改契約、`VERSION` +1,開一筆 `XCHG-*`。
2. 各消費 repo 各開本地 `CHG-*` 跟進,把 `docs/authority.md` 指標更新到新版本。
3. 跑 `cross_repo_check.py` 確認無漂移;整合驗收通過後 XCHG 收尾。
