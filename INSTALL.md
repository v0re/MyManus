# 安裝指南

> 本指南僅適用於 Linux。對於 Windows，請遵循 [WINDOWS 安裝指南](./WINDOWS_INSTALL.md)。macOS 安裝指南即將推出。

## 先決條件

- 一台 Linux 機器（建議使用 Ubuntu 22.04+）。
- 理論上任何 [MCP 用戶端](https://modelcontextprotocol.io/clients) 都可以，但本指南專為 [Linux Claude Desktop](https://github.com/emsi/claude-desktop) 設計。
- [claude.ai](https://claude.ai/) 訂閱或 LLM API 存取權限（任何高品質的 LLM 應該都可以，但建議使用 Claude 3.7）。
- `sudo` 權限以安裝套件。
- 沒錯，就這樣

## 安裝

Claude Desktop 是一個 Electron 應用程式。遵循本指南，您將下載並安裝 claude-desktop Windows 應用程式，將其重新打包為 Linux deb 套件，並安裝在您的機器上。
此外，將建立一個特殊的 claude_sandbox.sh 腳本，以在沙箱環境中運行 Claude Desktop。這使得給予 AI 存取本地檔案系統的權限更加安全。

### 安裝並運行 Claude Desktop
```bash
wget -O- https://raw.githubusercontent.com/emsi/claude-desktop/refs/heads/main/install-claude-desktop.sh | bash

~/sandboxes/claude_sandbox.sh

claude-desktop
```

這應該會建立由 MyManus 管理的 `~/sandboxes/claude-desktop/` 資料夾。

然後退出 Claude Desktop 應用程式並複製 MCP 工具設定：
```bash
cp claude_desktop_config.json ~/sandboxes/claude-desktop/.config/Claude/
```

### 在 Claude 應用程式中建立 MyManus 專案：

![新專案](./assets/Projects.png)

![建立 MyManus 專案](./assets/Create_Project.png)

![建立 MyManus 專案](./assets/Create_MyManus_Project.png)

![新增提示](./assets/Project_Instructions.png)

## 從[這裡](./prompts/prompt.md)貼上提示
到這裡：

![貼上提示](./assets/Set_Project_Instructions.png)

如果您遇到任何問題，請閱讀下一節。

## 手動逐步說明

1. 閱讀並遵循 https://github.com/emsi/claude-desktop 的說明
2. 閱讀 Linux 上的 MCP 說明 https://github.com/emsi/claude-desktop/blob/main/MCP_LINUX.md
3. 特別注意 https://github.com/emsi/claude-desktop/blob/main/MCP_LINUX.md#missing-display-variable
4. 建立並進入沙箱：`./claude_sandbox.sh`
5. 複製 MCP 伺服器設定：
`cp claude_desktop_config.json ~/sandboxes/claude-desktop/.config/Claude/`

6. 進入沙箱：`./claude_sandbox.sh`
7. 在沙箱中運行 Claude Desktop：`claude-desktop`

您可以在沒有沙箱的情況下運行 `claude-desktop`，但這樣 MCP 伺服器將可以存取您的本地檔案系統。

# 使用方法

開始新對話時，請確保選擇 MyManus 專案：

![選擇 MyManus 專案](./assets/MyManus_Use.png)


# 自動接受工具使用

如果您想自動接受工具使用，請閱讀[本指南](https://github.com/emsi/claude-desktop/blob/main/MCP_LINUX.md#auto-accepting-tools)
