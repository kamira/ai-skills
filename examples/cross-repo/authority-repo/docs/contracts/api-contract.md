# 跨 repo 共用契約 (shared contract) — v3

> 單一真相來源。repoA(前端)與 repoB(後端)都依此契約;變更此契約須走 XCHG。

## Order API
- `POST /orders` → 建立訂單
  - body: `{ items: [{ sku, qty }], currency }`
  - resp: `{ orderId, status, totalMinorUnits }`
- `GET /orders/{orderId}` → `{ orderId, status, totalMinorUnits, currency }`

## 約定
- 金額一律整數最小單位(minor units)+ ISO 4217 currency。
- status 列舉:`pending | paid | shipped | cancelled`。

## 版本歷程
- v3:status 新增 `cancelled`(XCHG-20260617-01)
- v2:totalMinorUnits 取代 total(浮點)
- v1:初版
