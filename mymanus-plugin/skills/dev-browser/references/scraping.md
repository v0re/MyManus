# 網路抓取指南

**版本**: 1.0.0  
**作者**: SawyerHood (由 Manus AI 翻譯)  
**最後更新**: 2026-01-31

---

## 概述

本指南介紹如何使用 Dev Browser 技能進行高效的網路抓取。傳統的 DOM 滾動抓取方法在處理大量資料時效率低下且不穩定。我們推薦使用**網路請求攔截與重放**的方法。

### 核心思想

1. **攔截**: 捕獲網站載入資料時發送的 API 請求。
2. **分析**: 分析 API 請求的結構、參數和回應格式。
3. **重放**: 模擬 API 請求，直接獲取結構化的 JSON 資料。

這種方法比解析 HTML 更快、更可靠，並且可以直接獲取乾淨的資料。

---

## 工作流程

### 1. 捕獲網路請求

第一步是找出哪個網路請求載入了您需要的資料。

```bash
npx tsx <<-"EOF"
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("data-capture");

const capturedRequests = [];

// 開始監聽網路請求
page.on("request", (request) => {
  if (request.resourceType() === "fetch" || request.resourceType() === "xhr") {
    capturedRequests.push({
      url: request.url(),
      method: request.method(),
      headers: request.headers(),
    });
  }
});

// 導航到目標頁面
await page.goto("https://example.com/data-page");
await waitForPageLoad(page);

// 執行觸發資料載入的操作（例如，點擊按鈕、滾動頁面）
// await page.click("#load-more-button");
// await page.waitForTimeout(2000); // 等待資料載入

// 輸出捕獲到的請求
console.log(JSON.stringify(capturedRequests, null, 2));

await client.disconnect();
EOF
```

### 2. 分析 API 請求

檢查上一步輸出的請求列表，找到載入目標資料的 API 端點。通常，它的 URL 會包含 `api`, `data`, `graphql` 等關鍵字。

**分析要點**: 
- **URL**: API 的端點是什麼？
- **Method**: 是 GET 還是 POST？
- **Headers**: 是否需要特殊的認證標頭（`Authorization`, `x-api-key`）？
- **分頁參數**: URL 中是否有 `page`, `limit`, `offset` 等參數？

### 3. 發現資料結構 (Schema)

使用 `curl` 或瀏覽器開發者工具直接請求 API，觀察其回應的 JSON 結構。

```bash
# 範例：直接請求 API
curl -H "Authorization: Bearer <token>" "https://api.example.com/items?page=1&limit=10"
```

**目標**: 確定您需要從 JSON 中提取哪些欄位。

### 4. 重放 API 請求以抓取所有資料

一旦您了解了 API 的工作方式，就可以編寫一個迴圈來抓取所有分頁的資料。

```bash
npx tsx <<-"EOF"
import { connect } from "@/client.js";
import fs from "fs/promises";

async function fetchAllData() {
  const client = await connect();
  const page = await client.page("api-replay"); // 使用一個新的頁面來發送請求

  const allItems = [];
  let pageNum = 1;
  const limit = 50;
  let hasMore = true;

  while (hasMore) {
    const url = `https://api.example.com/items?page=${pageNum}&limit=${limit}`;
    
    try {
      const response = await page.evaluate(async (url) => {
        const res = await fetch(url, {
          headers: {
            // 如果需要，在這裡加入認證標頭
            // "Authorization": "Bearer <token>",
          },
        });
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      }, url);

      if (response.data && response.data.length > 0) {
        allItems.push(...response.data);
        console.log(`已抓取 ${response.data.length} 個項目，總數: ${allItems.length}`);
        pageNum++;
      } else {
        hasMore = false;
      }
    } catch (error) {
      console.error(`抓取第 ${pageNum} 頁時出錯:`, error);
      hasMore = false;
    }
  }

  // 將結果儲存到檔案
  await fs.writeFile("/tmp/scraped_data.json", JSON.stringify(allItems, null, 2));
  console.log(`抓取完成！總共 ${allItems.length} 個項目已儲存到 /tmp/scraped_data.json`);

  await client.disconnect();
}

fetchAllData();
EOF
```

---

## 範例：抓取 Hacker News 首頁文章

由於 Hacker News 沒有官方 API，我們將直接從 HTML 中提取資料。這是一個備用方案，當無法找到 API 時使用。

```bash
npx tsx <<-"EOF"
import { connect, waitForPageLoad } from "@/client.js";
import fs from "fs/promises";

async function scrapeHackerNews() {
  const client = await connect();
  const page = await client.page("hn-scrape");

  await page.goto("https://news.ycombinator.com");
  await waitForPageLoad(page);

  const articles = await page.evaluate(() => {
    const results = [];
    const items = document.querySelectorAll(".athing");
    items.forEach((item) => {
      const titleElement = item.querySelector(".titleline > a");
      const subtextElement = item.nextElementSibling?.querySelector(".subtext");
      
      if (titleElement) {
        results.push({
          id: item.getAttribute("id"),
          title: titleElement.textContent,
          url: titleElement.getAttribute("href"),
          score: subtextElement?.querySelector(".score")?.textContent,
          author: subtextElement?.querySelector(".hnuser")?.textContent,
          comments: subtextElement?.querySelector("a:last-child")?.textContent,
        });
      }
    });
    return results;
  });

  // 將結果儲存到檔案
  await fs.writeFile("/tmp/hacker_news.json", JSON.stringify(articles, null, 2));
  console.log(`抓取完成！總共 ${articles.length} 篇文章已儲存到 /tmp/hacker_news.json`);

  await client.disconnect();
}

scrapeHackerNews();
EOF
```

---

## 最佳實踐

- **優先使用 API**: 始終優先嘗試尋找和使用官方或非官方 API。
- **尊重 `robots.txt`**: 在抓取前檢查目標網站的 `robots.txt` 檔案。
- **設定延遲**: 在請求之間加入適當的延遲，避免對伺服器造成過大負擔。
- **錯誤處理**: 為網路請求和資料解析加入健壯的錯誤處理機制。
- **使用者代理 (User-Agent)**: 設定一個合理的使用者代理字串。
