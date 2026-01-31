# GitHub Intelligence Collector

**版本**: 2.0.0  
**作者**: Manus AI  
**最後更新**: 2026-01-31

---

## 概述

GitHub Intelligence Collector 是一個專業的 Python 工具，用於在 GitHub 上搜尋潛在的敏感資料洩漏。

⚠️ **警告**: 此工具僅用於合法的安全研究、內部審計和教育目的。

---

## 功能特色

- ✅ **8 種憑證類型**: GitHub Token、AWS Key、OpenAI API Key 等
- ✅ **精確正則表達式**: 匹配真實憑證格式
- ✅ **自動假陽性過濾**: 排除文檔、範本、測試檔案
- ✅ **JSON 報告輸出**: 結構化的搜尋結果
- ✅ **統計資訊**: 顯示搜尋統計和發現摘要

---

## 安裝

無需額外安裝，工具已內建於 github-gem-seeker 技能中。

---

## 使用方式

### 列出所有支援的憑證類型

```bash
python3 github_intelligence_collector.py --list-types
```

**輸出**:
```
支援的憑證類型:
  1. github_token       - GitHub Personal Access Token (ghp_...)
  2. github_pat         - GitHub Fine-grained Token (github_pat_...)
  3. aws_key            - AWS Access Key (AKIA...)
  4. openai_key         - OpenAI API Key (sk-...)
  5. anthropic_key      - Anthropic API Key (sk-ant-...)
  6. google_key         - Google API Key (AIza...)
  7. stripe_key         - Stripe API Key (sk_live_...)
  8. slack_token        - Slack Token (xox...)
```

### 搜尋特定類型的憑證

```bash
python3 github_intelligence_collector.py --type github_token --limit 10
```

**參數**:
- `--type`: 憑證類型（必填）
- `--limit`: 搜尋結果數量（預設 20）
- `--output`: 輸出 JSON 檔案路徑（選填）

### 搜尋所有類型的憑證

```bash
python3 github_intelligence_collector.py --limit 20
```

### 輸出 JSON 報告

```bash
python3 github_intelligence_collector.py --type aws_key --output /tmp/aws_scan.json
```

---

## 輸出格式

### 終端輸出

```
=== GitHub Intelligence Collector ===
憑證類型: github_token
搜尋限制: 10

正在搜尋...
發現 5 個潛在洩漏

結果:
1. user/repo - config/secrets.yml
   URL: https://github.com/user/repo/blob/main/config/secrets.yml
   最後修改: 2026-01-30
   可能真實: 否 (Contains 'example' in path)

統計:
- 總發現數: 5
- 可能真實: 0
- 可能假陽性: 5
```

### JSON 輸出

```json
{
  "scan_time": "2026-01-31T23:00:00Z",
  "credential_type": "github_token",
  "total_found": 5,
  "likely_real": 0,
  "likely_false_positive": 5,
  "results": [
    {
      "repository": "user/repo",
      "file_path": "config/secrets.yml",
      "url": "https://github.com/user/repo/blob/main/config/secrets.yml",
      "last_modified": "2026-01-30",
      "likely_real": false,
      "reason": "Contains 'example' in path"
    }
  ]
}
```

---

## 假陽性過濾

工具會自動過濾以下類型的假陽性：

### 檔案路徑檢查

排除包含以下關鍵字的檔案：
- `readme`, `install`, `example`, `template`, `sample`
- `.md`, `test_`, `mock`, `security`, `scanner`

### 範例

| 檔案路徑 | 結果 | 原因 |
|---------|------|------|
| `config/secrets.yml` | ✅ 保留 | 可能是真實配置 |
| `docs/README.md` | ❌ 過濾 | 文檔檔案 |
| `examples/config.template.yml` | ❌ 過濾 | 範本檔案 |
| `tests/test_api.py` | ❌ 過濾 | 測試檔案 |
| `src/security_scanner.py` | ❌ 過濾 | 安全工具 |

---

## 支援的憑證類型

| 類型 | 正則表達式 | 範例 |
|------|-----------|------|
| GitHub Token | `ghp_[A-Za-z0-9]{36}` | `ghp_1234567890abcdefghijklmnopqrstuvwxyz` |
| GitHub Fine-grained | `github_pat_[A-Za-z0-9_]{82}` | `github_pat_11A...` |
| AWS Access Key | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| OpenAI API Key | `sk-[a-zA-Z0-9]{48}` | `sk-proj-...` |
| Anthropic API Key | `sk-ant-[a-zA-Z0-9-]{95,115}` | `sk-ant-api03-...` |
| Google API Key | `AIza[0-9A-Za-z-_]{35}` | `AIzaSyD...` |
| Stripe API Key | `sk_live_[0-9a-zA-Z]{24,}` | `sk_live_...` |
| Slack Token | `xox[baprs]-[0-9]{10,13}-[a-zA-Z0-9-]{24,}` | `xoxb-...` |

---

## 限制與注意事項

### 假陽性率高

經過實際驗證，大部分搜尋結果為假陽性（約 100%），原因包括：
- 文檔與教學內容
- 範本與腳本
- 測試與 Mock 資料
- 安全工具的模式定義

### GitHub 保護機制

GitHub 有自動 Secret Scanning 功能，會：
- 自動掃描提交的程式碼
- 撤銷洩漏的 GitHub Token
- 通知儲存庫擁有者和憑證提供者

### 真實洩漏的短暫生命週期

即使有真實洩漏，通常也會在幾分鐘到幾小時內被發現並刪除。

---

## 建議的使用場景

1. **內部安全審計**: 掃描自己組織的私有儲存庫
2. **持續監控**: 定期掃描新提交的程式碼
3. **教育與訓練**: 展示憑證洩漏的風險
4. **漏洞賞金計畫**: 負責任地披露發現的洩漏

---

## 進階用法

### 整合到 CI/CD

```yaml
# .github/workflows/secret-scan.yml
name: Secret Scan
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Secret Scan
        run: |
          python3 github_intelligence_collector.py --type github_token --limit 50 --output scan_results.json
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: scan-results
          path: scan_results.json
```

### 批次掃描多種類型

```bash
#!/bin/bash
TYPES=("github_token" "aws_key" "openai_key" "anthropic_key")

for type in "${TYPES[@]}"; do
    echo "Scanning for $type..."
    python3 github_intelligence_collector.py --type "$type" --limit 20 --output "${type}_scan.json"
done

echo "All scans complete!"
```

---

## 道德與法律聲明

⚠️ **重要提醒**: 

- 此工具僅用於合法的安全研究、內部審計和教育目的
- 未經授權掃描他人的儲存庫或使用發現的憑證是違法行為
- 使用者對其行為承擔全部法律責任
- 如發現真實洩漏，應負責任地通知相關方並協助修復

---

## 相關資源

- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - 專業的憑證掃描工具
- [GitLeaks](https://github.com/gitleaks/gitleaks) - Git 憑證洩漏偵測
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) - GitHub 官方文檔

---

## 授權

MIT License

---

## 聯絡方式

如有問題或建議，請透過 GitHub Issues 聯繫。
