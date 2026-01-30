# MyManus Plugin for Claude Code

將 Claude Code 轉變為具備 MyManus 能力的自主代理——規劃、推理、執行和評估——所有這些都無需編寫任何程式碼。

## 概述

此外掛程式將 [MyManus](https://github.com/emsi/MyManus) 強大的代理行為帶到 [Claude Code](https://claude.com/claude-code)，這是 Anthropic 官方為 Claude 設計的 CLI。它將 MyManus 的結構化代理迴圈方法論與 Claude Code 強大的開發工具相結合，創造出一個真正自主的 AI 助理。

### 您將獲得

**來自 MyManus：**
- 🎯 結構化代理迴圈（規劃 → 執行 → 觀察 → 迭代）
- 🧠 多模組架構（規劃器、知識、資料來源）
- 🌐 透過 Playwright 實現瀏覽器自動化能力
- 📋 系統化的任務規劃和進度追蹤
- 📝 專業的寫作和研究工作流程
- 🔄 自主的錯誤處理和策略調整

**來自 Claude Code：**
- ⚡ 快速、原生的開發工具（Bash、Read、Write、Edit、Glob、Grep）
- 🔍 強大的網路研究（WebFetch、WebSearch）
- 🤖 針對複雜任務的專業代理
- 📊 內建任務管理（TodoWrite）
- 🔌 MCP 伺服器整合
- 🖥️ 跨平台支援（Linux、macOS、Windows）

**兩者結合：**
一個強大、自主的 AI 代理，可以研究、編碼、分析資料、撰寫報告和自動化複雜的工作流程——同時在每一步都讓您了解進度。

## 主要功能

### 1. 自主代理行為
與標準的 Claude 互動不同，MyManus 外掛程式實現了真正的自主操作：
- 獨立規劃複雜任務
- 無需持續監督即可執行多步驟工作流程
- 遇到障礙時調整策略
- 在標記任務完成前驗證結果

### 2. 瀏覽器自動化
透過 Playwright MCP 伺服器實現完整的網頁自動化：
- 導航複雜網站
- 填寫表單並與動態內容互動
- 處理大量使用 JavaScript 的應用程式
- 執行多步驟的網路研究工作流程
- 自動關閉 cookie 橫幅和彈出視窗

### 3. 結構化任務管理
內建規劃和追蹤：
- 對複雜請求自動進行任務分解
- 透過 TodoWrite 即時更新進度
- 清晰的狀態報告（待辦 → 進行中 → 已完成）
- 透明的策略變更和錯誤處理

### 4. 專業研究與寫作
針對資訊工作的專業工作流程：
- 多來源事實查核和驗證
- 深入研究並提供全面的文件
- 長篇幅文章和報告寫作
- 適當的引用和參考資料管理

### 5. 系統化編碼
有組織的開發實踐：
- 專案結構規劃
- 程式碼組織和文件
- 測試和驗證
- 錯誤處理和偵錯

## 安裝

### 先決條件

1. **Claude Code**：從 [claude.com/claude-code](https://claude.com/claude-code) 安裝
2. **Node.js**：Playwright MCP 伺服器需要（建議使用 v18 或更高版本）
3. **Git**：用於存取外掛程式儲存庫

### 快速安裝（推薦）

安裝 MyManus 外掛程式最簡單的方法是透過 Claude Code 的外掛程式系統：

1. **新增 MyManus 市集**（一次性設定）：
   ```
   /plugin marketplace add https://github.com/emsi/MyManus.git
   ```

2. **安裝外掛程式**：
   ```
   /plugin install mymanus@mymanus
   ```

3. **重新啟動 Claude Code** 以啟動外掛程式

4. **驗證安裝**：
   ```
   /help
   ```
   MyManus 技能現在應該可供 Claude 自動使用。

### 手動安裝（替代方案）

如果您喜歡手動安裝或出於開發目的：

#### 步驟 1：克隆儲存庫

```bash
git clone https://github.com/emsi/MyManus.git
```

#### 步驟 2：新增為本地外掛程式

在 Claude Code 中，新增本地外掛程式：

```
/plugin marketplace add /path/to/MyManus
/plugin install mymanus@local
```

#### 步驟 3：設定 Playwright MCP 伺服器

#### 對於 Linux/macOS：

1. 確保已安裝 Node.js 和 npx：
   ```bash
   node --version
   npx --version
   ```

2. 將 Playwright MCP 伺服器新增到 Claude Code 的 MCP 設定中：
   - 開啟 Claude Code 設定/偏好設定
   - 導航到 MCP 伺服器部分
   - 新增以下設定：

   ```json
   {
     "playwright": {
       "runtime": "node",
       "command": "npx",
       "args": [
         "-y",
         "@automatalabs/mcp-server-playwright"
       ]
     }
   }
   ```

3. **僅限 Linux/WSL2**：如果您正在使用 Linux 或 WSL2，您可能需要設定 DISPLAY 變數：
   ```json
   {
     "playwright": {
       "runtime": "node",
       "command": "npx",
       "args": ["-y", "@automatalabs/mcp-server-playwright"],
       "env": {
         "DISPLAY": ":0"
       }
     }
   }
   ```
   確保您正在運行 X 伺服器（在 WSL2 上，使用 VcXsrv 或 X410）。

#### 對於 Windows：

Windows 使用者通常不需要 DISPLAY 環境變數。使用此設定：

```json
{
  "playwright": {
    "runtime": "node",
    "command": "npx",
    "args": [
      "-y",
      "@automatalabs/mcp-server-playwright"
    ]
  }
}
```

### MyManus 技能如何運作

MyManus 外掛程式是作為一個 **Claude Code 技能**實現的，這意味著：

- **自動啟動**：當 Claude 偵測到需要自主代理行為、複雜規劃、研究或多步驟工作流程的任務時，會自動調用該技能
- **情境感知**：技能描述幫助 Claude 決定何時使用 MyManus 的能力
- **隨需載入**：技能僅在需要時載入，保持您的對話高效
- **無縫整合**：與 Claude Code 的現有功能無衝突地協同工作

您無需手動啟動技能——Claude 會根據您的請求在適當的時候使用它。

### 驗證安裝

使用觸發 MyManus 技能的範例來測試安裝：

**測試 1：簡單的瀏覽器自動化**
```
使用瀏覽器導航到 example.com 並告訴我您看到了什麼。
```

**測試 2：研究任務（觸發自主行為）**
```
研究 Rust 網頁框架的最新發展並建立一個比較表。
```

Claude 應該會：
- 自動建立一個 TodoWrite 計劃
- 進行系統化的研究
- 提供全面的結果

## 使用方法

### 基本用法

安裝後，只需正常使用 Claude Code。Claude 會自動為受益於自主代理行為的任務調用 MyManus 技能。

**簡單任務範例：**
```
研究最新的 Python 網頁框架並建立一個比較表。
```

Claude 將會：
1. 建立一個包含研究步驟的待辦事項清單
2. 使用網路搜尋尋找最新資訊
3. 訪問多個來源以獲取全面的資料
4. 將發現編譯成結構化表格
5. 在進展過程中將每個步驟標記為完成

**複雜任務範例：**
```
建立一個簡單的網頁應用程式，獲取天氣資料並用圖表顯示。
```

Claude 將會：
1. 規劃架構（後端、前端、API 整合）
2. 建立專案結構
3. 編寫後端程式碼以進行 API 呼叫
4. 建立帶有視覺化的前端
5. 測試應用程式
6. 提供部署說明
7. 透過 TodoWrite 全程向您更新進度

### 進階功能

#### 1. 使用瀏覽器自動化進行網路研究

對於複雜的網路互動：
```
使用瀏覽器在 Coursera 上找到排名前 5 的機器學習課程，
包括它們的評分、時長和註冊人數。
```

Claude 將使用 Playwright 來：
- 導航到 Coursera
- 處理 cookie 橫幅
- 搜尋機器學習課程
- 提取詳細資訊
- 系統地編譯結果

#### 2. 長篇寫作

對於研究報告和文章：
```
撰寫一篇關於人工智慧歷史的 3000 字文章，
並附上適當的引用和參考資料。
```

Claude 將會：
- 從多個權威來源進行研究
- 建立大綱
- 撰寫各個部分
- 適當地引用來源
- 編譯一篇完整、結構良好的文章

#### 3. 程式碼專案

對於開發任務：
```
建立一個 Python 腳本，監控一個目錄中的新檔案
並自動將它們備份到指定位置。
```

Claude 將會：
- 規劃實作
- 建立適當的專案結構
- 編寫文件齊全的程式碼
- 新增錯誤處理
- 建立測試
- 提供使用文件

### 獲得最佳結果的提示

1. **具體說明**：清晰的任務描述有助於更好的規劃
2. **允許自主**：相信代理迴圈能處理細節
3. **檢查進度**：觀看 TodoWrite 更新以追蹤進度
4. **提供回饋**：在需要時糾正方向，但讓 Claude 自行調整
5. **複雜任務**：將大型專案自行分解為主要階段，讓 Claude 自主處理每個階段

## 與獨立版 MyManus 的差異

| 功能 | 獨立版 MyManus | MyManus Plugin for Claude Code |
|---|---|---|
| **平台** | 帶有自訂設定的 Claude Desktop | Claude Code CLI |
| **安裝** | 需要手動設定沙箱 | 簡單的外掛程式安裝 |
| **檔案工具** | MCP 檔案系統伺服器 | 原生 Read/Write/Edit 工具 |
| **Shell 存取** | MCP shell 伺服器（沙箱化） | 原生 Bash 工具 |
| **瀏覽器** | Playwright MCP | Playwright MCP + WebFetch |
| **任務追蹤** | 手動 todo.md 檔案 | TodoWrite 工具 |
| **沙箱** | 自訂 claude_sandbox.sh | Claude Code 的內建安全性 |
| **網路搜尋** | 僅限瀏覽器 | 原生 WebSearch + 瀏覽器 |
| **最適合** | 桌面使用者、視覺化工作流程 | 開發者、CLI 愛好者 |

### 何時使用哪個版本

**如果您符合以下情況，請使用獨立版 MyManus：**
- 您偏好桌面 GUI 互動
- 您需要視覺化的專案選擇
- 您想要原始的沙箱環境
- 您已經在使用 Claude Desktop

**如果您符合以下情況，請使用 MyManus Plugin for Claude Code：**
- 您偏好 CLI/終端機介面
- 您是開發者或進階使用者
- 您想要與開發工具原生整合
- 您需要更快的工具執行速度
- 您想使用 git 對您的專案進行版本控制

## 疑難排解

### Playwright MCP 無法運作

**症狀**：瀏覽器未啟動或 Playwright 工具不可用

**解決方案**：
1. 驗證 Node.js 安裝：`node --version`
2. 檢查 MCP 設定是否已正確儲存
3. 完全重新啟動 Claude Code
4. 檢查日誌以獲取 MCP 伺服器錯誤
5. 在 Linux/WSL2 上：確保 X 伺服器正在運行且 DISPLAY 已設定
6. 嘗試手動安裝：`npx -y @automatalabs/mcp-server-playwright`

### 系統提示未載入

**症狀**：Claude 未表現出自主行為

**解決方案**：
1. 驗證外掛程式是否已安裝並啟用：`/plugin list`
2. 確保您已重新啟動 Claude Code
3. 檢查 `mymanus` 技能是否可用：`/help`
4. 明確請求技能：「使用 MyManus 技能...」

### 其他問題

對於任何其他問題，請在 [MyManus GitHub 儲存庫](https://github.com/emsi/MyManus/issues)上提出問題。
