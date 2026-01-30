# WINDOWS 安裝指南

## 先決條件

- 一台能夠運行 [Windows Subsystem for Linux (WSL2)](https://learn.microsoft.com/en-us/windows/wsl/install) 的現代 Windows 機器。
- 在 Windows 上安裝了 Claude Desktop 應用程式。

# WSL2 安裝

請遵循官方指南在您的 Windows 機器上安裝 WSL2：https://learn.microsoft.com/en-us/windows/wsl/install<br/>

**懶人包：`wsl --install` 然後重新啟動您的機器。**

## 從 MS Store 安裝 Ubuntu 22.04

前往 MS Store 並安裝最新版本的 Ubuntu 22.04 LTS。
![Ubuntu 22.04 LTS](./assets/ubuntu@msstore.png)

## 安裝

**在安裝之前，請確保您至少運行並關閉過一次 Claude Desktop 應用程式。**

### 安裝並運行 Claude 沙箱
從開始功能表打開您的 Ubuntu 22.04 LTS 並運行以下命令：

```bash
wget -O- https://raw.githubusercontent.com/emsi/claude-desktop/refs/heads/main/install-claude-desktop.sh | bash

~/sandboxes/claude_sandbox.sh
```

將此儲存庫中的 `windows_claude_desktop_config.json` 複製到 `%APPDATA%\Claude\` 資料夾 **並將其重新命名為 `claude_desktop_config.json`**。

![Claude 設定](./assets/appdata_claude.png)


### 在 Claude 應用程式中建立 MyManus 專案：

![新專案](./assets/Projects.png)

![建立 MyManus 專案](./assets/Create_Project.png)

![建立 MyManus 專案](./assets/Create_MyManus_Project.png)

![新增提示](./assets/Project_Instructions.png)

## 從[這裡](./prompts/prompt.md)貼上提示
到這裡：

![貼上提示](./assets/Set_Project_Instructions.png)

如果您遇到任何問題，請閱讀下一節。

# 使用方法

開始新對話時，請確保選擇 MyManus 專案：

![選擇 MyManus 專案](./assets/MyManus_Use.png)


# 自動接受工具使用

如果您想自動接受工具使用，請閱讀[本指南](https://github.com/emsi/claude-desktop/blob/main/MCP_LINUX.md#auto-accepting-tools)
