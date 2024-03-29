<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant for foodpanda


使用本整合, 必須由你承擔任何風險.

## 安裝

你可以使用 [HACS](https://hacs.xyz/) 來安裝此整合元件. 步驟如下 custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/foodpanda` > Category: Integration

或是手動複製 `foodpanda` 到你的設定資料夾 (像是 /config) 下的 `custom_components` 目錄.

然後重新啟動 HA.

# 設定

** 使用 Home Assistant 整合**

1. 使用者介面, 設定 > 整合 > 新增整合 > foodpanda
   1. 如果整合沒有出在清單裡，請重新整理網頁
   2. 如果重新整理網頁後，整合還是沒有出在清單裡，請您清除瀏覽器的快取
2. 輸入 帳號和密碼 或是 輸入 tokens 如果是用 Fackbook 或 Google 登入 (香港/新加坡只能用 token 方法)
3. 如果是使用帳號/密碼登入，x-device 欄位是必要的. 你可以依照 [obtain_token](https://github.com/tsunglung/foodpanda/blob/master/docs/obtain_token.md#obtain-x-device) 取得 x-device 的值
4. 如果輸入都正確，就可以創建自動化，廣播外送進度到通訊軟體和 HomePod mini。

# 注意
使用 Facebook 和 Google 方式登入，需要截取 Tokens.

打賞

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/foodpanda/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/foodpanda/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/foodpanda/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |
