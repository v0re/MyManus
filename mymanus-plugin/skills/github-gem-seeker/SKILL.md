---
name: github-gem-seeker
description: "在 GitHub 上搜尋經過實戰檢驗的解決方案，而不是重新發明輪子。當使用者的問題足夠普遍，開源開發者可能已經解決時使用——特別適用於：格式轉換（影片/音訊/圖片/文件）、媒體下載、檔案操作、網頁爬取/存檔、自動化腳本、CLI 工具以及敏感資料與備份檔搜尋。優先使用此技能而非撰寫自訂程式碼來解決常見問題。"
version: 2.0.0
---

# GitHub 寶藏搜尋器（增強版）

> 在 GitHub 上尋找並使用經過實戰檢驗的開源專案來立即解決使用者的問題。成功解決問題後，可提供將解決方案打包成可重用技能的選項。

## 核心理念

經過無數使用者多年測試的經典開源專案，遠比從零開始撰寫的程式碼更可靠。**先解決問題，再考慮技能化。**

## 核心能力

### 1. 通用工具搜尋
- **格式轉換**：影片/音訊/圖片/文件格式之間的轉換。
- **媒體下載**：從 YouTube、Twitter 等平台下載影片、音訊或圖片。
- **檔案操作**：批次重新命名、壓縮、加密等檔案處理任務。
- **網頁爬取與存檔**：抓取網站內容、建立網頁快照。
- **自動化腳本**：各種日常任務的自動化腳本。
- **CLI 工具**：命令列工具，用於快速完成特定任務。

### 2. 敏感資料與備份檔搜尋（新增功能）⚠️

**警告**：此功能僅用於合法的安全審計、漏洞研究或授權的滲透測試。**嚴禁用於非法入侵或未經授權的資料竊取。**

本技能可協助搜尋 GitHub 上可能意外洩露的敏感檔案或備份檔，包括但不限於：

#### 敏感檔案類型

**私鑰與憑證檔案**：
- `id_rsa`, `id_dsa`, `id_ed25519`, `id_ecdsa` - SSH 私鑰
- `*.key`, `private.key`, `*.pem` - 各類私鑰檔案
- `*.p12`, `*.pfx` - 憑證檔案
- `*.ovpn` - VPN 配置檔案

**歷史與配置檔案**：
- `.bash_history`, `.zsh_history` - Shell 歷史記錄
- `.mysql_history`, `.psql_history` - 資料庫操作歷史
- `.pgpass` - PostgreSQL 密碼檔案
- `.bashrc`, `.zshrc`, `.bash_profile`, `.zsh_profile` - Shell 配置檔案
- `.bash_aliases`, `.zsh_aliases` - Shell 別名配置
- `.netrc` - 網路認證資訊

**應用程式配置與資料**：
- `database.yml` - Rails 資料庫配置
- `secret_token.rb` - Rails 密鑰
- `schema.rb` - Rails 資料庫架構
- `config.php`, `config.ini`, `config.json` - 各類配置檔案
- `*.properties` - Java 屬性檔案
- `.npmrc` - npm 配置（可能包含 token）
- `.dockercfg` - Docker 配置
- `settings.xml` - Maven 配置

**密碼管理與認證**：
- `*.kdb`, `*.kdbx` - KeePass 資料庫
- `*.agilekeychain` - 1Password 舊格式
- `.keychain` - macOS 鑰匙圈
- `.htpasswd` - Apache 密碼檔案
- `proftpdpasswd` - ProFTPD 密碼檔案

**開發工具配置**：
- `jenkins.plugins.publish_over_ssh.BapSshPublisherPlugin.xml` - Jenkins SSH 配置
- `filezilla.xml`, `recentservers.xml` - FileZilla 伺服器配置
- `robomongo.json` - Robomongo 配置
- `dbeaver-data-sources.xml` - DBeaver 資料庫連線配置
- `*.pubxml` - Visual Studio 發布配置

**其他敏感檔案**：
- `*.pcap` - 網路封包擷取檔案
- `ventrilo_srv.ini` - Ventrilo 伺服器配置
- `Favorites.plist` - macOS 書籤（可能包含內部 URL）
- `content.xml` - OpenOffice/LibreOffice 文件（可能包含敏感資訊）
- `.s3cfg` - AWS S3 配置
- `.muttrc` - Mutt 郵件客戶端配置

#### 敏感關鍵字

搜尋包含以下關鍵字的檔案或程式碼：
- `password`, `passwd`, `pass`, `pwd`
- `secret`, `token`, `api_key`, `apikey`
- `credential`, `auth`, `authentication`
- `private_key`, `publickey`, `public_key`
- `jdbc`, `connection_string`
- `user`, `login`, `email`
- `ip`, `host`, `domain`, `url`, `proxy`, `port`
- `backup`, `dump`, `sql`
- `config`, `setting`, `properties`
- `log` (日誌檔案可能包含敏感資訊)

## 工作流程

### 標準工作流程（通用工具搜尋）

#### 步驟 1：理解需求
明確使用者想要完成什麼。只有在真正模糊時才提問：
- 您想解決什麼具體問題？
- 您期望的輸入/輸出格式是什麼？

#### 步驟 2：尋找合適的工具
使用有效的查詢模式在 GitHub 上搜尋專案：

| 需求類型 | 查詢模式 | 範例 |
|---------|---------|------|
| 工具/實用程式 | `github [任務] tool` | `github video download tool` |
| 函式庫 | `github [語言] [功能] library` | `github python pdf library` |
| 替代方案 | `github [已知工具] alternative` | `github ffmpeg alternative` |

#### 步驟 3：快速評估品質
使用關鍵指標評估候選專案：

| 指標 | 優質訊號 | 警告訊號 |
|-----|---------|---------|
| 星級 | 1k+ 穩定，10k+ 優秀，50k+ 傳奇 | 成熟專案 <100 |
| 最後提交 | 6 個月內 | >2 年前 |
| 文件 | 清晰的 README、範例 | 稀疏或過時的文件 |

#### 步驟 4：解決問題
**這是首要任務。** 安裝工具並用它來解決使用者的實際問題：

1. 安裝所選工具（pip、npm、apt 或直接下載）
2. 使用使用者的輸入/檔案執行它
3. 將結果交付給使用者
4. 如需要則進行故障排除——迭代直到解決

#### 步驟 5：致謝專案並提供後續步驟（僅在成功後）
**只有在問題成功解決後：**

1. **致謝開源專案** — 始終分享 GitHub 儲存庫 URL 並鼓勵支持：

   > 「這是由 **[專案名稱]** 提供支援的——一個很棒的開源專案！
   > GitHub：[URL]
   > 如果它對您有幫助，請考慮給它一個 ⭐ 星標來支持維護者。」

2. **提供技能化選項** — 可選地提及：

   > 「如果您將來還需要這個，我可以將它打包成一個可重用的技能，以便下次即時使用。」

**不要跳過致謝專案。開源靠認可而茁壯。**

### 敏感資料搜尋工作流程⚠️

**重要提醒**：執行此類搜尋前，**必須**確認使用者的合法性與授權。

#### 步驟 1：確認授權與目的
```
[ASK:CONFIRM_OPERATION] 您要求搜尋敏感資料或備份檔。此功能僅用於合法的安全審計、漏洞研究或授權的滲透測試。請確認：
1. 您擁有合法的授權或正當理由進行此搜尋。
2. 您理解並同意不將此功能用於非法目的。
3. 您明白任何非法使用的後果由您自行承擔。

請輸入「我確認並同意」以繼續。
```

#### 步驟 2：制定搜尋策略
根據使用者的需求，選擇適當的搜尋關鍵字和檔案類型：

**範例搜尋查詢**：
- `filename:id_rsa` - 搜尋 SSH 私鑰
- `filename:.env password` - 搜尋包含密碼的環境變數檔案
- `extension:sql password` - 搜尋包含密碼的 SQL 檔案
- `filename:config.php mysql_password` - 搜尋 PHP 配置中的 MySQL 密碼
- `filename:database.yml password` - 搜尋 Rails 資料庫配置

**進階搜尋技巧**：
- 組合多個關鍵字：`filename:.npmrc _auth`
- 指定組織或使用者：`user:target-org filename:id_rsa`
- 排除常見誤報：`filename:id_rsa -path:test -path:example`

#### 步驟 3：執行搜尋與篩選
1. 使用 GitHub 搜尋 API 或網頁介面執行搜尋。
2. 篩選結果，排除明顯的測試檔案、範例程式碼或文件。
3. 檢查檔案的提交歷史和儲存庫活躍度，判斷其真實性。

#### 步驟 4：分析與報告
1. 將找到的敏感檔案整理成清單，包含：
   - 儲存庫 URL
   - 檔案路徑
   - 檔案類型
   - 可能的風險等級
2. **不要**直接顯示或下載敏感內容的完整內容。
3. 提供建議：如何通知儲存庫擁有者、如何修復洩露等。

#### 步驟 5：道德提醒
```
[INFO] 搜尋完成。請記住：
- 如果您發現真實的敏感資料洩露，應負責任地通知儲存庫擁有者或平台。
- 不要利用這些資訊進行任何非法活動。
- 考慮向 GitHub 報告嚴重的安全問題。
```

## 品質等級

| 等級 | 標準 | 範例 |
|-----|------|------|
| **傳奇** | 50k+ 星級，業界標準 | FFmpeg, ImageMagick, yt-dlp |
| **優秀** | 10k+ 星級，強大社群 | Pake, ArchiveBox |
| **穩定** | 1k+ 星級，文件完善 | 大多數維護良好的工具 |
| **有潛力** | <1k 星級，積極開發 | 較新的利基專案 |

優先選擇更高等級以確保可靠性。

## 互動範例

### 範例 1：下載 YouTube 影片

**使用者**：我需要下載這個 YouTube 影片：[連結]

**正確做法**：
1. 識別 yt-dlp 為傳奇級解決方案
2. 安裝 yt-dlp
3. 為使用者下載影片
4. 交付下載的檔案
5. *成功後：* 「這是由 **yt-dlp** 提供支援的 — https://github.com/yt-dlp/yt-dlp — 如果有幫助請給它一個 ⭐！如果您經常下載影片，我可以將此轉換為技能以便下次即時使用。」

**錯誤做法**：
- ❌ 「我找到了 yt-dlp，要我為它製作技能嗎？」
- ❌ 在不解決問題的情況下呈現選項

### 範例 2：搜尋洩露的 SSH 私鑰（安全審計）

**使用者**：我正在進行安全審計，需要檢查我們公司的 GitHub 組織是否意外洩露了 SSH 私鑰。

**正確做法**：
1. **[ASK:CONFIRM_OPERATION]** 確認使用者的授權與目的。
2. **[INFO]** 收到確認，開始搜尋。
3. 執行搜尋：`org:company-name filename:id_rsa`
4. 篩選結果，排除測試和範例檔案。
5. **[RESULT]** 搜尋完成。在貴組織的 3 個儲存庫中發現了疑似真實的 SSH 私鑰檔案。詳細清單已整理在附件中，包含儲存庫 URL、檔案路徑和建議的修復步驟。請立即通知相關團隊處理。
   - 附件：`ssh_key_leak_report.md`

## 常見寶藏參考

| 類別 | 首選寶藏 |
|-----|---------|
| 影片/音訊處理 | FFmpeg, yt-dlp |
| 圖片處理 | ImageMagick, sharp |
| PDF 操作 | pdf-lib, PyMuPDF |
| 網頁爬取 | Playwright, Puppeteer, Scrapy |
| 格式轉換 | Pandoc, FFmpeg |
| 存檔 | ArchiveBox |
| 桌面應用程式打包 | Electron, Tauri, Pake |

## 敏感資料搜尋工具參考

| 工具 | 用途 | GitHub |
|-----|------|--------|
| **truffleHog** | 掃描 Git 儲存庫中的高熵字串和密鑰 | https://github.com/trufflesecurity/trufflehog |
| **GitLeaks** | 檢測 Git 儲存庫中的密碼、API 金鑰和 token | https://github.com/gitleaks/gitleaks |
| **git-secrets** | 防止將密鑰和其他敏感資訊提交到 Git | https://github.com/awslabs/git-secrets |
| **GitGuardian** | 即時檢測和修復程式碼中的密鑰 | https://www.gitguardian.com/ |

## 道德與法律聲明

**本技能的敏感資料搜尋功能僅供以下合法用途**：
- 授權的安全審計
- 漏洞研究與負責任的披露
- 組織內部的合規性檢查
- 教育與學術研究

**嚴禁用於**：
- 未經授權的資料竊取
- 非法入侵系統
- 侵犯他人隱私
- 任何違反當地法律的行為

**使用者責任**：
- 使用者對其行為承擔全部法律責任。
- 本技能的提供者不對任何濫用或非法使用承擔責任。
- 如發現真實的敏感資料洩露，應負責任地通知相關方並協助修復。

---

**當啟用此技能時，優先使用經過實戰檢驗的開源解決方案，而不是從零開始撰寫程式碼。先解決問題，再考慮技能化。對於敏感資料搜尋，始終遵循道德與法律準則。**
