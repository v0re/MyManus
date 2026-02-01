# MyManus 完整程式碼審查報告

**審查日期**: 2026-02-01
**審查範圍**: 整個 MyManus 儲存庫（所有原始碼、配置檔、文件）
**審查分支**: `claude/complete-code-review-WPr6P`

---

## 1. 專案概述

MyManus 是一個開源（AGPL-3.0）的自主 AI 代理框架，將 Claude 轉變為具備規劃、推理、執行與評估能力的自主代理。專案基於 Model Context Protocol (MCP) 架構，提供 9 個專門技能模組，涵蓋瀏覽器自動化、安全測試、GitHub 搜尋等功能。

**技術棧**: TypeScript, Node.js, Python, Playwright, Express, Hono, MCP

---

## 2. 嚴重安全漏洞

### 2.1 [嚴重] Shell 注入漏洞 — `github_intelligence_collector.py`

**檔案**: `mymanus-plugin/skills/github-gem-seeker/tools/github_intelligence_collector.py:95-106`

```python
def search_github(self, query: str, limit: int = 10) -> List[Dict]:
    cmd = f"gh search code '{query}' --limit {limit} --json repository,path,url,textMatches"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
```

**問題**: 使用 `shell=True` 搭配 f-string 格式化使用者輸入，允許 shell 命令注入。攻擊者可透過特殊字元（如 `'; rm -rf /; '`）在 `query` 參數中注入任意 shell 命令。

**影響**: 任意命令執行（RCE），可導致完全系統控制。

**建議修復**: 使用 `subprocess.run()` 的列表形式並設定 `shell=False`：
```python
cmd = ["gh", "search", "code", query, "--limit", str(limit),
       "--json", "repository,path,url,textMatches"]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
```

### 2.2 [嚴重] 第二處 Shell 注入 — `github_intelligence_collector.py`

**檔案**: `mymanus-plugin/skills/github-gem-seeker/tools/github_intelligence_collector.py:129-130`

```python
cmd = f"gh api repos/{repo_path}/contents/{file_path} --jq '.content' | base64 -d"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
```

**問題**: `repo_path` 和 `file_path` 來自 GitHub URL 解析，可被操縱來注入命令。管道運算子 (`|`) 本身就需要 `shell=True`，這使得整個命令鏈都暴露於注入風險。

**建議修復**: 拆分為兩個獨立的 `subprocess` 呼叫：
```python
gh_result = subprocess.run(
    ["gh", "api", f"repos/{repo_path}/contents/{file_path}", "--jq", ".content"],
    capture_output=True, text=True, timeout=10
)
decoded = base64.b64decode(gh_result.stdout).decode("utf-8")
```

### 2.3 [高] Express 伺服器綁定所有網路介面

**檔案**: `mymanus-plugin/skills/dev-browser/src/index.ts:194`

```typescript
const server = app.listen(port, () => {
    console.log(`HTTP API server running on port ${port}`);
});
```

**問題**: `app.listen(port)` 預設綁定到 `0.0.0.0`（所有網路介面），這意味著任何同一網路上的裝置都能存取此伺服器，包括瀏覽器控制 API 和 CDP WebSocket 端點。

**影響**: 遠端攻擊者可透過此 API 控制受害者的瀏覽器，包括瀏覽任何頁面、讀取已登入網站的資料。

**建議修復**:
```typescript
const server = app.listen(port, "127.0.0.1", () => {
    console.log(`HTTP API server running on http://127.0.0.1:${port}`);
});
```

**對比**: `relay.ts` 中的 Hono 伺服器已正確預設綁定到 `127.0.0.1`（第 107 行），這兩個模組的安全策略不一致。

### 2.4 [高] 瀏覽器上下文中使用 `eval()`

**檔案**: `mymanus-plugin/skills/dev-browser/src/client.ts:417`

```typescript
const snapshot = await page.evaluate((script: string) => {
    const w = globalThis as any;
    if (!w.__devBrowser_getAISnapshot) {
        eval(script);  // <-- eval() 使用
    }
    return w.__devBrowser_getAISnapshot();
}, snapshotScript);
```

**問題**: 在瀏覽器上下文中使用 `eval()` 注入腳本。雖然腳本來源是內部生成的（非使用者輸入），但 `eval()` 在安全審計中通常被標記為高風險。如果腳本生成過程被污染（例如透過供應鏈攻擊），這將成為 XSS 的入口點。

**建議**: 考慮使用 `page.addScriptTag()` 或 `page.addInitScript()` 替代 `eval()`。

### 2.5 [中] 憑證預覽洩露

**檔案**: `mymanus-plugin/skills/github-gem-seeker/tools/github_intelligence_collector.py:202`

```python
"credential_preview": credential[:20] + "..." if len(credential) > 20 else credential,
```

**問題**: 將找到的憑證前 20 個字元儲存到報告中。對於許多憑證格式（如 `ghp_`、`AKIA`），前 20 個字元可能包含足夠資訊來重建或利用該憑證。

**建議**: 只儲存憑證類型和是否匹配的布爾值，不要儲存任何實際內容。

---

## 3. 程式碼品質問題

### 3.1 TypeScript 原始碼（dev-browser）

#### 3.1.1 `browser-script.ts` — 巨型字串模板

**檔案**: `mymanus-plugin/skills/dev-browser/src/snapshot/browser-script.ts`（878 行）

**問題**: 整個 ARIA 快照系統（DOM 工具、YAML 序列化、角色工具、快照邏輯）以 JavaScript 字串模板的形式內嵌在 TypeScript 檔案中。這導致：

- **無型別安全**: 字串中的 JS 程式碼沒有 TypeScript 型別檢查
- **無 IDE 支援**: 無語法高亮、自動補全、重構支援
- **難以測試**: 內嵌程式碼無法被單獨單元測試
- **維護困難**: 約 800 行的字串模板，任何修改都容易引入語法錯誤
- **未使用的匯入**: 檔案開頭匯入了 `fs` 和 `path`（第 12-13 行），以及讀取 `snapshotDir`（第 29 行），但這些在當前實作中完全沒有使用

**建議**: 使用建構工具（如 esbuild）將瀏覽器腳本作為獨立的 TypeScript 檔案編寫和編譯，然後在執行期讀取已編譯的 JS 檔案。

#### 3.1.2 `inject.ts` — 重複匯出

**檔案**: `mymanus-plugin/skills/dev-browser/src/snapshot/inject.ts`

此檔案與 `src/snapshot/index.ts` 的內容完全相同——都只是從 `browser-script.ts` 重新匯出。

```typescript
// inject.ts 和 index.ts 的內容一模一樣：
export { getSnapshotScript, clearSnapshotScriptCache } from "./browser-script";
```

**建議**: 移除其中一個冗餘檔案。

#### 3.1.3 `client.ts` — 連線管理

**檔案**: `mymanus-plugin/skills/dev-browser/src/client.ts:252-283`

`ensureConnected()` 方法使用了一個 mutex 模式來防止競態條件，這是好的做法。但如果初始連線成功後瀏覽器斷開，`connectingPromise` 會被設為 `null`，下次呼叫會重新連線。然而，舊的 `browser` 引用可能沒有被清理，`browser.close()` 也不會被呼叫。

**建議**: 在 `ensureConnected()` 中，當偵測到舊連線斷開時，先清理舊的 browser 引用。

#### 3.1.4 `index.ts` — 伺服器缺乏速率限制

**檔案**: `mymanus-plugin/skills/dev-browser/src/index.ts`

Express 伺服器上的 API 端點沒有任何速率限制或認證機制。任何能存取該端口的人都可以無限制地建立新頁面、關閉頁面或存取瀏覽器的 CDP 端點。

**建議**: 至少加入一個簡單的 token 認證或只允許 localhost 存取。

#### 3.1.5 `relay.ts` — 硬編碼延遲

**檔案**: `mymanus-plugin/skills/dev-browser/src/relay.ts:395`

```typescript
await new Promise((resolve) => setTimeout(resolve, 200));
```

在建立新標籤頁後使用固定 200ms 延遲來等待 `Target.attachedToTarget` 事件。在較慢的系統上可能不夠，在較快的系統上又是不必要的等待。

**建議**: 改用事件驅動的方式等待目標註冊。

### 3.2 Python 原始碼

#### 3.2.1 `github_intelligence_collector.py` — URL 解析脆弱

**檔案**: `mymanus-plugin/skills/github-gem-seeker/tools/github_intelligence_collector.py:126-127`

```python
repo_path = url.replace("https://github.com/", "").split("/blob/")[0]
file_path = "/".join(url.split("/blob/")[1].split("/")[1:])
```

**問題**: 使用字串操作解析 GitHub URL，沒有錯誤處理。如果 URL 格式不符預期（不包含 `/blob/`），會拋出 `IndexError`。

**建議**: 使用 `urllib.parse` 進行 URL 解析，並加入適當的錯誤處理。

#### 3.2.2 `github_intelligence_collector.py` — 正則表達式作為搜尋查詢

**檔案**: `mymanus-plugin/skills/github-gem-seeker/tools/github_intelligence_collector.py:168`

```python
query = f"/{cred_info['pattern']}/"
```

**問題**: GitHub Code Search API 不支援正則表達式語法作為查詢。將 Python 正則表達式模式（如 `ghp_[A-Za-z0-9]{36}`）直接當作搜尋查詢會導致搜尋結果不準確或為空。

**建議**: 使用 GitHub 支援的搜尋語法，例如搜尋憑證前綴字串（如 `ghp_`）。

---

## 4. 架構與設計問題

### 4.1 Express + Hono 雙框架混用

**檔案**: `package.json`（同時依賴 `express` 和 `hono`）

`index.ts`（伺服器模式）使用 Express，而 `relay.ts`（擴充套件模式）使用 Hono。兩個框架完成類似的工作（HTTP + WebSocket 伺服器），但使用了不同的 API 和慣例。

**影響**:
- 增加了套件體積（兩個 HTTP 框架）
- 維護者需要熟悉兩套 API
- 安全配置不一致（如綁定地址的問題）

**建議**: 統一使用一個框架。考慮到 `relay.ts` 中 Hono + WebSocket 的整合更乾淨，可以考慮全部遷移到 Hono。

### 4.2 技能模組缺乏腳本實作

以下技能在文件中引用了不存在的腳本：

| 技能 | 引用的腳本 | 實際狀態 |
|------|-----------|---------|
| `penetration-testing` | `scripts/shodan_query.py` | 不存在 |
| `penetration-testing` | `scripts/nmap_scan.py` | 不存在 |
| `penetration-testing` | `scripts/report_generator.py` | 不存在 |

**影響**: 使用者按照文件操作時會遇到找不到腳本的錯誤。

### 4.3 SKILL.md 與 prompt.md 大量內容重複

`mymanus-plugin/skills/mymanus/SKILL.md`（679 行）與 `prompts/prompt.md`（393 行）有超過 80% 的內容重複。兩者都定義了代理的行為、搜尋系統、瀏覽器系統、訊息系統等。

**影響**: 修改一處時容易忘記同步更新另一處，導致行為不一致。

**建議**: 選擇一個作為權威來源（Single Source of Truth），另一個引用或繼承。

### 4.4 `prompt.md` 中的沙箱路徑假設

**檔案**: `prompts/prompt.md:374-387`

```
/home/agent/
|-- Documents
|   |-- CODE
|   `-- NOTES
`-- Downloads
```

Prompt 假設執行環境為 `/home/agent/` 下的特定目錄結構，但 Claude Code 使用者的實際工作目錄可能完全不同。

---

## 5. 配置與部署問題

### 5.1 MCP 伺服器來自非正式 fork

**檔案**: `claude_desktop_config.json:15-19`

```json
"sandbox": {
    "command": "uvx",
    "args": ["mcp-server-shell @ git+https://github.com/emsi/mcp-server-shell"]
}
```

**問題**: `mcp-server-shell` 從 `emsi` 的 GitHub fork 安裝，而非官方來源。如果此 fork 被入侵或惡意修改，將直接影響所有使用者的系統安全。

**建議**: 在文件中說明為什麼需要使用 fork 而非官方版本，並考慮鎖定到特定 commit hash。

### 5.2 `package.json` 使用過於寬鬆的版本範圍

**檔案**: `mymanus-plugin/skills/dev-browser/package.json`

所有依賴都使用 `^` 範圍（如 `"playwright": "^1.49.0"`）。對於像 Playwright 這樣的瀏覽器自動化工具，次要版本更新有時會引入破壞性變更（特別是瀏覽器版本更新）。

**建議**: 對關鍵依賴（尤其是 Playwright）使用精確版本鎖定。

### 5.3 缺少 `package-lock.json` 或等效的鎖定檔案管理

儲存庫中同時存在 `package-lock.json` 和 `bun.lock`，表示專案在 npm 和 bun 之間不確定。應該選擇一個套件管理器並記錄在文件中。

---

## 6. 測試覆蓋率

### 6.1 現有測試

只有 `dev-browser` 技能包含測試（`src/snapshot/__tests__/snapshot.test.ts`），共 8 個測試案例，涵蓋：
- 基本快照生成
- 互動元素的 ref 分配
- ref 持久化
- 連結 URL 包含
- 表單元素
- 巢狀結構
- 禁用元素
- 核取方塊狀態

### 6.2 缺失的測試

- `index.ts`（Express 伺服器）— 無 API 端點測試
- `client.ts` — 無連線管理、頁面操作測試
- `relay.ts` — 無 CDP 命令路由、WebSocket 通訊測試
- `github_intelligence_collector.py` — 完全沒有測試
- 所有 SKILL.md 中引用的工作流程 — 無整合測試

**建議**: 優先為 Express API 端點和 Python 工具增加測試。

---

## 7. 文件品質

### 7.1 優點
- 所有文件統一使用繁體中文，語言一致
- README 提供了清晰的安裝步驟
- 範例目錄包含 3 個詳細的使用範例
- 技能文件結構統一（YAML frontmatter + Markdown）

### 7.2 問題
- `penetration-testing` 引用了不存在的 Python 腳本
- `INSTALL.md` 和 `INSTALL_CLAUDECODE.md` 有部分重複內容
- `dev-browser` 版本號為 `0.0.1` 但技能的 SKILL.md 缺少版本號
- `prompt.md.backup` 不應該被追蹤在版本控制中

---

## 8. 許可證合規性

專案使用 AGPL-3.0 許可證，但依賴的部分開源專案使用不同的許可證：
- Playwright: Apache-2.0（相容）
- Express: MIT（相容）
- Hono: MIT（相容）

**結論**: 依賴的許可證與 AGPL-3.0 相容，無合規問題。

---

## 9. 總結與優先修復建議

### 必須立即修復（P0 — 安全）
1. **Shell 注入漏洞**: `github_intelligence_collector.py` 中的兩處 `subprocess.run(shell=True)`
2. **Express 伺服器綁定地址**: `index.ts` 中 `app.listen()` 應綁定到 `127.0.0.1`

### 應盡快修復（P1 — 安全 + 品質）
3. 移除或遮蔽憑證預覽功能
4. 替換 `eval()` 為更安全的腳本注入方式
5. 統一 Express/Hono 框架使用

### 建議改善（P2 — 品質）
6. 將 `browser-script.ts` 中的內嵌 JS 提取為獨立的 TypeScript 檔案
7. 移除 `inject.ts` 冗餘檔案
8. 為 `penetration-testing` 補充引用的 Python 腳本或修正文件
9. 消除 `SKILL.md` 與 `prompt.md` 之間的內容重複
10. 增加測試覆蓋率，特別是 API 端點和 Python 工具

### 低優先度（P3 — 改善）
11. 統一套件管理器（npm vs bun）
12. 鎖定 Playwright 版本
13. 移除 `prompt.md.backup` 從版本控制
14. 修正 `relay.ts` 中的硬編碼延遲

---

**審查者**: Claude Code (Opus 4.5)
**審查方法**: 完整原始碼閱讀 + 靜態分析
