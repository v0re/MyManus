# MyManus 外掛程式的 MCP 設定

MyManus 外掛程式會自動設定 Playwright MCP 伺服器以進行瀏覽器自動化。本指南涵蓋特定平台的設定和疑難排解。

## 自動設定

此外掛程式包含一個 `.mcp.json` 檔案，在安裝時會自動設定 Playwright。**macOS/Windows 無需手動設定。**

### Linux/WSL2 額外設定

Linux 和 WSL2 需要 X 伺服器來顯示瀏覽器。將 DISPLAY 環境變數新增到您的 MCP 設定中：

1. 開啟 Claude Code 設定 → MCP 伺服器
2. 找到 `playwright` 伺服器（由外掛程式自動設定）
3. 新增環境變數：
   ```json
   "env": {
     "DISPLAY": ":0"
   }
   ```

**X 伺服器設定：**
- **Linux**：X 伺服器通常隨桌面環境預先安裝
- **WSL2**：在 Windows 主機上安裝 VcXsrv 或 X410
- 測試 X 伺服器：`xclock`（應顯示一個時鐘視窗）

## 先決條件

- **Node.js** v18 或更高版本（包含 npx）
- 驗證：`node --version` 和 `npx --version`

## 疑難排解

### 瀏覽器未啟動

- 驗證 Node.js：`node --version`
- 在安裝外掛程式後重新啟動 Claude Code
- 檢查 Claude Code 日誌以獲取 MCP 錯誤

### DISPLAY 錯誤（僅限 Linux/WSL2）

- 安裝 X 伺服器（適用於 WSL2 的 VcXsrv）
- 將 `"DISPLAY": ":0"` 新增到 MCP 設定的 env 部分
- 在啟動 Claude Code 之前啟動 X 伺服器
- 測試：`xclock` 應顯示一個時鐘

### Playwright 工具不可用

- 重新啟動 Claude Code（MCP 伺服器在啟動時載入）
- 檢查外掛程式是否已安裝：`/plugin list`
- 手動測試 Playwright：`npx -y @automatalabs/mcp-server-playwright`

## 資源

- [Playwright MCP 伺服器](https://www.npmjs.com/package/@automatalabs/mcp-server-playwright)
- [Claude Code MCP 文件](https://docs.claude.com/en/docs/claude-code/mcp)
