# MyManus Plugin for Claude Code 安裝指南

本指南涵蓋如何安裝並使用 MyManus 外掛程式與 [Claude Code](https://claude.com/claude-code)，這是 Anthropic 官方為 Claude 設計的 CLI。

## 概述

MyManus 外掛程式透過**基於技能的方法**為 Claude Code 帶來自主代理能力。與原始的 MyManus（適用於 Claude Desktop）不同，此外掛程式：

- ✅ **使用 Claude Code 的內建工具**（Bash、Read、Write、Edit、Glob、Grep）
- ✅ **依賴 Claude Code 的 MCP 整合**（無需獨立的檔案/shell 伺服器）
- ✅ **自動設定 Playwright MCP** 以進行瀏覽器自動化
- ⚠️ **除了 Claude Code 的標準功能外，沒有專門的沙箱**

## 先決條件

在安裝 MyManus 外掛程式之前，請確保您已具備：

1. **Claude Code**：從 [claude.com/claude-code](https://claude.com/claude-code) 安裝
2. **Node.js** v18 或更高版本：Playwright MCP 伺服器需要
   ```bash
   node --version  # 應顯示 v18.0.0 或更高版本
   ```
3. **Git**：用於存取外掛程式儲存庫

> * 請注意，如果您在安裝過程中遇到問題，claude code 可以並將會協助您完成安裝步驟！

## 安裝

### 步驟 1：新增 MyManus 市集

開啟 Claude Code 並執行：

```bash
/plugin marketplace add https://github.com/emsi/MyManus.git
```

這會將 MyManus 外掛程式市集新增到您的 Claude Code 設定中。

### 步驟 2：安裝外掛程式

```bash
/plugin install mymanus@mymanus
```

此外掛程式將被安裝，且 `.mcp.json` 檔案將自動設定 Playwright MCP 伺服器。

### 步驟 3：重新啟動 Claude Code

**重要**：您必須重新啟動 Claude Code 才能載入外掛程式和 MCP 伺服器。

```bash
# 退出 Claude Code
exit

# 再次啟動 Claude Code
claude
```

### 步驟 4：驗證安裝

檢查外掛程式是否成功載入：

```bash
/plugin list
```

您應該會在已安裝的外掛程式清單中看到 `mymanus`。

```
/doctor 
```
以驗證 MCP 伺服器是否正常運行。

## 使用 MyManus 技能

MyManus 外掛程式透過**技能**提供自主代理能力。Claude Code 中的技能設計為根據任務上下文**自動調用**，但您也可以**明確請求**它們。

### 自動調用（推薦）

當您給 Claude 一個複雜的多步驟任務時，它應該會自動識別並應用 MyManus 技能。例如：

```
研究 2024 年量子計算的最新發展，
撰寫一份包含引用的綜合報告，並建立一份摘要簡報。
```

Claude 將自動使用 MyManus 技能的結構化代理迴圈（規劃 → 執行 → 觀察 → 迭代）來處理這個複雜的任務。

### 明確調用

如果 Claude 沒有為複雜任務自動應用 MyManus 技能，您可以明確請求它：

**選項 1：直接請求**
```
使用 MyManus 技能研究 [主題] 並建立一份詳細報告。
```

**選項 2：提及代理行為**
```
作為一個自主代理，研究 2024 年排名前 10 的 AI 新創公司，
分析他們的產品，並建立一個比較表。
```

**選項 3：參考代理迴圈**
```
使用代理迴圈方法論，規劃並執行一個網頁爬取任務，
以從 example.com 收集產品資料。
```

### 何時使用 MyManus 技能

MyManus 技能非常適合：

- 🔍 **複雜的研究任務**，需要多個來源和事實查核
- 📝 **長篇寫作**，包含引用和參考資料
- 🌐 **網頁自動化**，使用瀏覽器互動
- 💻 **軟體開發專案**，包含規劃和測試
- 📊 **資料分析**，包含多個處理步驟
- 🤖 **多步驟工作流程**，需要自主執行

### 技能行為

當 MyManus 技能啟動時，它會：

1. **規劃任務**，使用 TodoWrite 進行透明的進度追蹤
2. **系統化執行**，遵循代理迴圈方法論
3. **驗證結果**，在標記任務完成前
4. **調整策略**，當遇到障礙時
5. **清晰報告**，在每一步都報告進度

## 與 Claude Desktop MyManus 的重要差異

### 檔案與 Shell 存取

- **Claude Desktop MyManus**：使用專門的 MCP 伺服器進行沙箱化的檔案/shell 存取
- **Claude Code MyManus**：使用 Claude Code 的**原生工具**（Bash、Read、Write、Edit）
- **影響**：除了 Claude Code 的標準安全模型外，沒有額外的沙箱

### 瀏覽器自動化

- **兩個版本**：都使用 Playwright MCP 伺服器進行瀏覽器自動化
- **Claude Code 版本**：透過 `.mcp.json` 自動設定（macOS/Windows 無需手動設定）

### 安全模型

⚠️ **重要**：Claude Code 外掛程式**不**提供專門的沙箱。它的操作權限和存取級別與 Claude Code 本身相同。

- 檔案操作使用 Claude Code 的原生工具
- Shell 命令透過 Claude Code 的 Bash 工具運行
- 瀏覽器自動化在您的本地機器上運行（不在專門的沙箱中）

**最佳實踐**：
- 在執行前審查複雜的命令
- 在受信任的開發環境中使用
- 對專案目錄外的檔案操作保持謹慎
- 監控瀏覽器自動化任務

## 疑難排解

### 外掛程式未載入

**症狀**：外掛程式未出現在 `/plugin list` 中

**解決方案**：
1. 驗證安裝：`/plugin list` 並尋找 `mymanus`
2. 檢查市集：`/plugin marketplace list`
3. 使用 `/doctor` 命令檢查問題
4. 向 claude 尋求幫助：「幫我排解 MyManus 外掛程式的安裝問題。我的 /doctor 輸出顯示...」

### 瀏覽器自動化無法運作

**症狀**：與瀏覽器相關的任務失敗或沒有瀏覽器視窗出現

**解決方案**：
1. 驗證 Node.js：`node --version`（需要 v18+）
2. 檢查 Claude Code 設定中的 MCP 設定
3. 要求 claude 測試 MCP 伺服器：「測試 Playwright MCP 伺服器設定。」

### 技能未使用

**症狀**：Claude 未對複雜任務使用 MyManus 代理行為

**解決方案**：
1. 明確請求技能：「使用 MyManus 技能...」
2. 提及自主行為：「作為一個自主代理...」
3. 參考特定能力：「使用瀏覽器自動化，導航到...」
4. 檢查外掛程式是否已啟用：`/plugin list`（應顯示 `mymanus` 為已啟用）

### MCP 伺服器錯誤

**症狀**：Playwright MCP 伺服器啟動失敗

**解決方案**：
1. 更新 npx 快取：`npx clear-npx-cache`
2. 手動測試：`npx -y @automatalabs/mcp-server-playwright`
3. 檢查 Claude Code 日誌以獲取詳細的錯誤訊息
4. 驗證 Node.js 安裝：`which node` 和 `which npx`

## 進階設定

### 與自訂 MCP 伺服器一起使用

MyManus 外掛程式可與您在 Claude Code 中設定的任何 MCP 伺服器一起使用。此外掛程式的 `.mcp.json` 僅新增 Playwright - 您現有的 MCP 設定保持不變。

### 停用自動 MCP 設定

如果您想手動管理 Playwright MCP：

1. 在安裝外掛程式前，在 Claude Code 設定中設定 Playwright
2. 此外掛程式的 `.mcp.json` 不會覆蓋現有的設定

---

**準備就緒！** 啟動 Claude Code 並給它一個複雜的任務，看看 MyManus 自主代理的實際表現。
