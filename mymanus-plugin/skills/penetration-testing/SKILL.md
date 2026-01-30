---
name: penetration-testing
description: "提供一個整合 Shodan、Nmap 和其他 Kali Linux 工具的滲透測試框架。當使用者提供域名或 IP 並表明意圖為滲透測試時使用。"
version: 1.0.0
---

# 滲透測試技能

> **警告**：本技能僅供授權的滲透測試、安全研究和教育目的使用。**嚴禁**在未經明確授權的情況下對任何系統進行測試。所有操作均會被記錄，任何非法使用將由使用者承擔全部法律責任。

本技能整合了 Shodan、Nmap 等強大的安全工具，為 AI 代理提供一個結構化的滲透測試工作流程。

## 白帽駭客模式

當此技能被啟動時，AI 代理將自動載入**專業白帽駭客 Prompt**（參見 `references/whitehat_prompt.md`），進入一個專注於漏洞發現與利用的工作模式。在此模式下，代理將：

-   **深度驗證漏洞**：不僅報告可疑漏洞，而是主動使用工具和自訂腳本進行驗證。
-   **編寫自訂程式碼**：當標準工具無法利用漏洞時，分析失敗原因並編寫 Python/Bash 腳本進行滲透。
-   **系統化思維**：遵循「觀察 → 假設 → 測試 → 分析 → 行動」的思考鏈，環環相扣。
-   **目標導向**：最終目標是取得系統控制權（shell、敏感檔案、權限提升），而非僅列出漏洞清單。

**範例情境**：當發現一個 SQL 注入點但 `sqlmap` 因 WAF 保護而失敗時，代理會手動分析注入點，測試不同的編碼和混淆技術，並編寫 Python 腳本繞過 WAF 進行資料提取。

## 核心能力

1.  **意圖確認**：當使用者提供域名或 IP 時，主動詢問其意圖，確保操作的合法性。
2.  **被動資訊收集 (Shodan)**：
    -   查詢 IP 或域名的 Shodan 報告。
    -   識別開放的連接埠、運行的服務、作業系統版本。
    -   搜尋已知的漏洞 (CVE)。
3.  **主動掃描 (Nmap)**：
    -   執行多種類型的 Nmap 掃描（TCP、UDP、SYN、服務版本探測、作業系統偵測）。
    -   使用 Nmap 指令碼引擎 (NSE) 進行更深入的漏洞掃描和利用。
4.  **漏洞分析**：
    -   將 Shodan 和 Nmap 的結果進行關聯分析。
    -   使用 `searchsploit` 等工具在本地漏洞資料庫中查找可利用的漏洞。
5.  **Web 應用程式測試 (Kali Tools)**：
    -   使用 `gobuster` 或 `dirb` 進行目錄和檔案爆破。
    -   使用 `nikto` 掃描 Web 伺服器的常見漏洞。
    -   使用 `sqlmap` 進行自動化的 SQL 注入測試。
6.  **報告生成**：將所有測試結果、發現的漏洞和修復建議匯總成一份專業的滲透測試報告。

## 工作流程

### 步驟 1：意圖確認與授權

當使用者提供一個目標（域名或 IP）時，**必須**首先執行此步驟。

```
[ASK:CONFIRM_OPERATION] 您提供的目標是 [目標]。請問您的意圖是什麼？

1.  **一般資訊查詢** (例如，查詢 DNS、WHOIS)
2.  **授權的滲透測試** (需要您確認已獲得目標系統的明確授權)

如果您選擇 2，請確認您是系統所有者或已獲得書面授權。任何未經授權的測試都是非法的。請輸入「我確認已獲得授權」以繼續進行滲透測試。
```

### 步驟 2：被動資訊收集

在獲得授權後，首先進行不直接與目標互動的被動資訊收集。

-   **[執行中]** 正在使用 Shodan 查詢 [目標]...
-   呼叫 `scripts/shodan_query.py --target [目標]`
-   分析 Shodan 返回的 JSON 結果，提取關鍵資訊。

### 步驟 3：主動掃描

根據被動收集的資訊，制定主動掃描策略。

-   **[ASK]** Shodan 報告顯示目標開放了以下主要連接埠：[連接埠列表]。我建議執行一個針對這些連接埠的 Nmap 服務版本探測掃描。是否繼續？
-   **[執行中]** 正在執行 Nmap 掃描...
-   呼叫 `scripts/nmap_scan.py --target [目標] --ports [連接埠列表] --type service_version`
-   儲存 Nmap 的 XML 輸出以供後續分析。

### 步驟 4：漏洞分析與利用

-   **[執行中]** 正在分析掃描結果，並在 Exploit-DB 中搜尋相關漏洞...
-   呼叫 `searchsploit [服務名稱] [版本號]`
-   **[ASK]** 發現潛在漏洞 [CVE-ID] (Exploit-DB ID: [EBD-ID])。該漏洞可能允許 [漏洞描述]。是否嘗試使用 Metasploit 或相關腳本進行驗證？

### 步驟 5：Web 應用程式測試

如果目標是一個 Web 應用程式，則執行此步驟。

-   **[執行中]** 正在使用 Nikto 和 Gobuster 掃描 Web 應用程式...
-   呼叫 `nikto -h [目標]`
-   呼叫 `gobuster dir -u http://[目標] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

### 步驟 6：生成報告

-   **[執行中]** 正在匯總所有發現並生成滲透測試報告...
-   將所有步驟的發現、日誌和建議整理到一個 Markdown 檔案中。
-   **[RESULT]** 針對 [目標] 的滲透測試已完成。詳細報告請見附件。
    -   附件：`penetration_test_report_[目標].md`

## 所需工具與環境

本技能假設 AI 代理運行在一個類似 Kali Linux 的環境中，並已安裝以下工具：

-   **Shodan CLI** (`shodan`)
-   **Nmap** (`nmap`)
-   **SearchSploit** (`searchsploit`)
-   **Nikto** (`nikto`)
-   **Gobuster** (`gobuster`)
-   **SQLMap** (`sqlmap`)
-   **Metasploit Framework** (`msfconsole`)

### Python 依賴

-   `shodan`
-   `python-nmap`
-   `lxml`

## 輔助腳本

-   `scripts/shodan_query.py`：用於與 Shodan API 互動。
-   `scripts/nmap_scan.py`：封裝常用的 Nmap 掃描命令。
-   `scripts/report_generator.py`：用於自動生成 Markdown 格式的報告。

## 白帽駭客 Prompt 參考

完整的白帽駭客行為模式與思考鏈請參閱：[references/whitehat_prompt.md](./references/whitehat_prompt.md)

此 Prompt 定義了當技能啟動時，AI 代理應採取的專業行為模式，包括：
-   角色與心態（目標導向、隱匿與精準、系統化思維）
-   當發現可疑漏洞時的完整驗證流程
-   當標準工具失敗時的自訂程式碼編寫策略
-   思考鏈 (Chain of Thought) 方法論

## 注意事項

-   **API 金鑰**：Shodan 和其他商業工具可能需要 API 金鑰。請確保已在環境變數中設定 `SHODAN_API_KEY`。
-   **掃描強度**：Nmap 掃描可能會觸發入侵檢測系統 (IDS)。在執行任何掃描之前，務必與目標系統管理員協調。
-   **法律風險**：重複強調，未經授權的測試是非法的。本技能的設計初衷是為了協助授權的安全專業人員，而非鼓勵非法駭客行為。
