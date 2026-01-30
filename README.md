# MyManus

<div align="center">
  <img src="./assets/MyManus.png" alt="MyManus">
</div>

MyManus 是一個 100% 免費、0% 編碼、**本地化**、**安全**的代理環境，類似於 [Manus AI](https://manus.im/)，完全圍繞模型上下文協議 [MCP](https://modelcontextprotocol.io/introduction) 實作。

MyManus 使用沙箱技術來保護您的系統，並允許 AI 代理使用瀏覽器、建立檔案、執行命令等。

MyManus 在本地機器上安全地運行瀏覽器，而不是在一些脆弱的雲端伺服器上，這使得它快速、免費且可靠。

得益於其神奇的 [提示](./prompts/prompt.md)，MyManus 能夠自行規劃、推理、執行、評估和處理所有問題。

研究、編碼、資料分析、生產力、生活，應有盡有。根據工具集的不同，它可以用於您能想像到的任何任務。

您所需要的只是一個 [Claude Desktop](https://github.com/emsi/claude-desktop) 應用程式（或任何其他 [MCP 用戶端](https://modelcontextprotocol.io/clients)）和一些現有的 [MCP 伺服器](https://modelcontextprotocol.io/examples)，以設定您的終極代理環境，讓 AI 代理完成您能想像到的所有任務。無需編寫任何程式碼。無需購買額外的軟體（除了現有的 [claude.ai](https://claude.ai/) 訂閱或 LLM API）。

---

# 安裝選項

## 適用於 Claude Code（推薦）

MyManus 現在可作為 [Claude Code](https://claude.com/claude-code) 的外掛程式使用，這是 Anthropic 的官方 CLI！

**[→ Claude Code 安裝指南](./INSTALL_CLAUDECODE.md)**

## 適用於 Claude Desktop

要為 Claude Desktop 應用程式安裝 MyManus：

**[→ 安裝指南 (Linux/macOS)](./INSTALL.md)**
**[→ Windows 安裝指南](./WINDOWS_INSTALL.md)**

---

# [使用指南](./USAGE.md)
要使用 MyManus，請遵循[使用指南](./USAGE.md)。

# [範例](./EXAMPLES.md)

要查看 MyManus 的實際操作，請查看[範例](./EXAMPLES.md)。

---

# 技能市集

MyManus 現在包含一個內建的**技能市集**，提供 8 個專業技能，全部為繁體中文：

## 📊 資料與分析
- **stock-analysis** (v1.0.0) - 股票與公司財務分析
- **excel-generator** (v1.0.0) - 專業 Excel 試算表建立
- **similarweb-analytics** (v1.0.0) - 網站流量與參與度分析

## 🔍 工具搜尋
- **github-gem-seeker** (v2.0.0) - 在 GitHub 上搜尋經過實戰檢驗的解決方案和敏感資料
- **internet-skill-finder** (v1.0.0) - 搜尋並推薦代理技能

## 🛠️ 開發工具
- **skill-creator** (v1.0.0) - 互動式技能建立指南

## 🔒 安全與滲透測試
- **penetration-testing** (v1.0.0) - 整合式滲透測試框架（Shodan + Nmap + Kali 工具）
  - 包含專業的**白帽駭客提示**
  - 深度漏洞驗證
  - 當標準工具失敗時自訂程式碼生成
  - 系統化思考鏈：觀察 → 假設 → 測試 → 分析 → 行動

所有技能都位於 `mymanus-plugin/skills/` 中，並在 MyManus 啟動時自動載入。

更多資訊，請參閱 [mymanus-plugin/skills/README.md](./mymanus-plugin/skills/README.md)。
