# MyManus 增強版 - 技能市集

> 歡迎來到 MyManus 增強版的技能市集！這裡存放了所有移植自 Manus AI 的專業技能，旨在為您的 AI 代理提供更強大的領域專用能力。

## 概述

本目錄下的每一個子目錄都代表一個獨立的、可插拔的技能 (Skill)。這些技能與 MyManus 增強版的核心架構（如結構化規劃、進階訊息系統）無縫整合，讓您的 AI 代理能夠處理更複雜、更專業的任務。

所有技能均已完全繁體中文化，並遵循 MyManus 的文件格式。

## 可用技能列表

截至目前，已成功移植並增強以下 **6 個專業技能**：

| 技能名稱 | 核心功能 | 版本 | 狀態 |
|---|---|---|---|
| `stock-analysis` | 股票與公司財務分析 | 1.0.0 | ✅ 可用 |
| `excel-generator` | 專業 Excel 試算表建立 | 1.0.0 | ✅ 可用 |
| `similarweb-analytics` | 網站流量與參與度分析 | 1.0.0 | ✅ 可用 |
| `github-gem-seeker` | GitHub 開源工具與敏感資料搜尋 | 2.0.0 | ✅ 增強 |
| `internet-skill-finder` | 搜尋與推薦新的 AI 代理技能 | 1.0.0 | ✅ 可用 |
| `skill-creator` | 指導建立自訂技能 | 1.0.0 | ✅ 可用 |

### 1. 股票分析 (`stock-analysis`)
- **描述**：使用金融市場資料分析股票與公司，提供技術洞察、價格圖表、財報分析等。
- **詳情**：`stock-analysis/SKILL.md`

### 2. Excel 生成器 (`excel-generator`)
- **描述**：建立美觀且功能強大的 Excel 試算表，支援公式、圖表和資料分析。
- **詳情**：`excel-generator/SKILL.md`

### 3. SimilarWeb 分析 (`similarweb-analytics`)
- **描述**：利用 SimilarWeb 資料分析網站流量、來源、排名和使用者參與度。
- **詳情**：`similarweb-analytics/SKILL.md`

### 4. GitHub 寶藏搜尋器 (`github-gem-seeker`) - 增強版
- **描述**：在 GitHub 上尋找經過實戰檢驗的開源工具，並**新增了搜尋意外洩露的敏感資料與備份檔的功能**。
- **警告**：敏感資料搜尋功能僅限於合法的安全審計與授權測試。
- **詳情**：`github-gem-seeker/SKILL.md`

### 5. 網路技能搜尋器 (`internet-skill-finder`)
- **描述**：從 GitHub 等平台搜尋、評估並推薦新的 AI 代理技能，幫助您擴展代理的能力。
- **詳情**：`internet-skill-finder/SKILL.md`

### 6. 技能建立器 (`skill-creator`)
- **描述**：提供一個完整的指南，協助您從零開始建立自己的客製化技能。
- **詳情**：`skill-creator/SKILL.md`

## 如何使用這些技能

MyManus 增強版的 AI 代理能夠**自動**根據您的任務需求，載入並使用最合適的技能。

#### 範例 1：自動觸發 `stock-analysis`
```
請幫我分析一下特斯拉 (TSLA) 最近的股價表現和財務狀況。
```

#### 範例 2：自動觸發 `excel-generator`
```
我需要一份季度銷售報告的 Excel 表格，包含各產品的銷售額和一個總結圖表。
```

#### 範例 3：自動觸發 `github-gem-seeker` (敏感資料搜尋)
```
我正在進行安全審計，請幫我檢查我們的 GitHub 組織 `my-company-org` 是否有洩露的 `id_rsa` 檔案。
```
> **注意**：AI 代理會先要求您確認授權。

### 明確指定技能

您也可以在請求中明確指定要使用的技能，以獲得更精準的結果。

```
請使用 `similarweb-analytics` 技能，幫我比較 `website-a.com` 和 `website-b.com` 的流量來源。
```

## 如何安裝這些技能

這些技能已包含在 `mymanus-enhanced` 的發行版中。您只需按照主 `README.md` 或 `安裝指南.md` 中的指示，將 `enhanced/` 目錄下的 `prompts/` 和 `skills/` 兩個目錄（或其內容）複製到您的 MyManus 或 Claude Code 環境中即可。

### 目錄結構

確保您的 `skills` 目錄結構如下：

```
<your_mymanus_plugin_dir>/
└── skills/
    ├── mymanus/          # 核心增強技能
    │   └── SKILL.md
    ├── stock-analysis/   # 已移植的技能
    │   └── SKILL.md
    ├── excel-generator/
    │   └── SKILL.md
    ├── ... (其他技能)
    └── README.md         # 本檔案
```

## 擴展您的技能庫

- **尋找新技能**：使用 `internet-skill-finder` 技能來發現更多社群開發的技能。
- **建立自訂技能**：使用 `skill-creator` 技能來打造滿足您特定需求的專屬技能。

我們鼓勵您探索、使用並擴展這個技能生態系統，讓您的 AI 代理變得更加強大！
