# Line Bot 轉換 TODO

## POC（目前進行中）

- [x] 探索現有專案架構
- [x] 建立 `line_bot_handler.py` webhook 處理邏輯
- [x] 在 `flask_app.py` 加入 `/linebot/webhook` 路由
- [ ] 建立 `.env` / `SETTING.ini` 填入 Line Bot 憑證
- [ ] 本地測試（用 ngrok 或 cloudflare tunnel 暴露 localhost）
- [ ] 測試訂單文字解析流程（貼文字 → 確認 → 寫入 Google Sheets）

---

## Phase 2：基本功能完善

- [ ] 查詢訂單（輸入日期 → 列出當天所有訂單）
- [ ] 訂單狀態追蹤（待確認 / 已出貨）
- [ ] 多管理員支援（限定特定 Line 帳號才能操作）
- [ ] 輸入驗證與錯誤提示（地址/電話格式不正確時提醒）
- [ ] 到貨提醒推播（對顧客 Line 帳號推播）

---

## Phase 3：進階功能

- [ ] Flex Message 美化訂單預覽卡片
- [ ] Quick Reply 按鈕（上午/下午、轉帳/貨到付款）
- [ ] 多輪對話逐步填寫（逐欄引導）
- [ ] 訂單搜尋（依姓名或電話）
- [ ] 匯出當日訂單為 CSV 並傳回 Line
- [ ] 部署到正式環境（Railway / Render / GCP）

---

## 技術筆記

### 需要的環境變數
```
LINE_CHANNEL_SECRET=...
LINE_CHANNEL_ACCESS_TOKEN=...
```

### 本地測試流程
1. `pip install line-bot-sdk`
2. 填入 `SETTING.ini` 的 Line Bot 憑證
3. 啟動 Flask：`python flask_app.py`
4. 用 ngrok 暴露：`ngrok http 8080`
5. 將 ngrok URL + `/linebot/webhook` 填入 Line Developer Console Webhook URL
