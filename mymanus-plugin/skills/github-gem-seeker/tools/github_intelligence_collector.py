#!/usr/bin/env python3
"""
GitHub Intelligence Collector v2.0
精確的敏感資料蒐證工具 - 減少假陽性

作者: Manus AI (White Hat Mode)
日期: 2026-01-31
"""

import subprocess
import json
import re
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class GitHubIntelCollector:
    """GitHub 敏感資料蒐證器"""
    
    # 精確的憑證模式（使用正則表達式）
    CREDENTIAL_PATTERNS = {
        "github_token": {
            "pattern": r"ghp_[A-Za-z0-9]{36}",
            "description": "GitHub Personal Access Token",
            "risk": "HIGH",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md"]
        },
        "github_oauth": {
            "pattern": r"gho_[A-Za-z0-9]{36}",
            "description": "GitHub OAuth Token",
            "risk": "HIGH",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md"]
        },
        "aws_access_key": {
            "pattern": r"AKIA[0-9A-Z]{16}",
            "description": "AWS Access Key ID",
            "risk": "CRITICAL",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md"]
        },
        "slack_token": {
            "pattern": r"xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,32}",
            "description": "Slack Token",
            "risk": "HIGH",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md"]
        },
        "openai_api_key": {
            "pattern": r"sk-[a-zA-Z0-9]{48}",
            "description": "OpenAI API Key",
            "risk": "HIGH",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md"]
        },
        "anthropic_api_key": {
            "pattern": r"sk-ant-api03-[a-zA-Z0-9\-_]{95}",
            "description": "Anthropic API Key",
            "risk": "HIGH",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md"]
        },
        "private_key_rsa": {
            "pattern": r"-----BEGIN RSA PRIVATE KEY-----[\s\S]{100,}-----END RSA PRIVATE KEY-----",
            "description": "RSA Private Key (Complete)",
            "risk": "CRITICAL",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md", "test_"]
        },
        "jwt_token": {
            "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
            "description": "JWT Token",
            "risk": "MEDIUM",
            "exclude_files": ["README", "INSTALL", ".example", ".template", ".sample", ".md", "test_"]
        }
    }
    
    # 高風險檔案類型（真實配置檔案）
    HIGH_RISK_FILES = [
        "*.env",
        "config.yml",
        "database.yml",
        "credentials.json",
        "secrets.json",
        ".npmrc",
        ".dockercfg",
        "id_rsa",
        "id_dsa",
        "id_ed25519"
    ]
    
    def __init__(self):
        self.results = []
        self.stats = {
            "total_searches": 0,
            "total_findings": 0,
            "verified_findings": 0,
            "false_positives": 0
        }
    
    def search_github(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 GitHub CLI 搜尋"""
        try:
            cmd = f"gh search code '{query}' --limit {limit} --json repository,path,url,textMatches"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
            return []
        except Exception as e:
            print(f"[ERROR] 搜尋失敗: {e}", file=sys.stderr)
            return []
    
    def is_false_positive(self, file_path: str, exclude_patterns: List[str]) -> bool:
        """檢查是否為假陽性"""
        file_lower = file_path.lower()
        
        for pattern in exclude_patterns:
            if pattern.lower() in file_lower:
                return True
        
        # 檢查是否為測試檔案
        if any(x in file_lower for x in ["test_", "_test", "mock", "example", "sample", "template"]):
            return True
        
        return False
    
    def extract_credential_from_content(self, url: str, pattern: str) -> Tuple[bool, str]:
        """從檔案內容中提取憑證"""
        try:
            # 使用 gh api 獲取原始內容
            repo_path = url.replace("https://github.com/", "").split("/blob/")[0]
            file_path = "/".join(url.split("/blob/")[1].split("/")[1:])
            
            cmd = f"gh api repos/{repo_path}/contents/{file_path} --jq '.content' | base64 -d"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                content = result.stdout
                matches = re.findall(pattern, content)
                if matches:
                    # 返回第一個匹配（截斷顯示）
                    credential = matches[0]
                    if len(credential) > 100:
                        credential = credential[:50] + "..." + credential[-20:]
                    return True, credential
            
            return False, ""
        except Exception as e:
            return False, f"Error: {e}"
    
    def collect_intelligence(self, credential_type: str = None, limit: int = 10):
        """收集情報"""
        patterns_to_search = {}
        
        if credential_type:
            if credential_type in self.CREDENTIAL_PATTERNS:
                patterns_to_search[credential_type] = self.CREDENTIAL_PATTERNS[credential_type]
            else:
                print(f"[ERROR] 未知的憑證類型: {credential_type}")
                return
        else:
            patterns_to_search = self.CREDENTIAL_PATTERNS
        
        print(f"\n{'='*70}")
        print(f"  GitHub Intelligence Collector v2.0 - 精確蒐證模式")
        print(f"{'='*70}\n")
        
        for cred_type, cred_info in patterns_to_search.items():
            print(f"[*] 搜尋: {cred_info['description']} (風險: {cred_info['risk']})")
            self.stats["total_searches"] += 1
            
            # 構建搜尋查詢（使用正則表達式）
            query = f"/{cred_info['pattern']}/"
            
            # 搜尋
            findings = self.search_github(query, limit)
            
            if not findings:
                print(f"    └─ 未發現洩漏\n")
                continue
            
            print(f"    └─ 發現 {len(findings)} 個潛在洩漏，正在驗證...\n")
            
            for finding in findings:
                repo = finding['repository']['nameWithOwner']
                path = finding['path']
                url = finding['url']
                
                # 檢查假陽性
                if self.is_false_positive(path, cred_info['exclude_files']):
                    self.stats["false_positives"] += 1
                    print(f"    [SKIP] {repo}/{path} (假陽性)")
                    continue
                
                # 提取真實憑證
                has_credential, credential = self.extract_credential_from_content(url, cred_info['pattern'])
                
                if has_credential:
                    self.stats["verified_findings"] += 1
                    result = {
                        "type": cred_type,
                        "description": cred_info['description'],
                        "risk": cred_info['risk'],
                        "repository": repo,
                        "file_path": path,
                        "url": url,
                        "credential_preview": credential[:20] + "..." if len(credential) > 20 else credential,
                        "discovered_at": datetime.now().isoformat()
                    }
                    self.results.append(result)
                    print(f"    [FOUND] {repo}/{path}")
                    print(f"            憑證預覽: {result['credential_preview']}")
                    print(f"            URL: {url}\n")
                else:
                    self.stats["false_positives"] += 1
                    print(f"    [SKIP] {repo}/{path} (無法提取憑證)")
            
            self.stats["total_findings"] += len(findings)
            print()
    
    def generate_report(self, output_file: str = "intelligence_report.json"):
        """生成報告"""
        report = {
            "metadata": {
                "tool": "GitHub Intelligence Collector v2.0",
                "generated_at": datetime.now().isoformat(),
                "statistics": self.stats
            },
            "findings": self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*70}")
        print(f"  蒐證完成")
        print(f"{'='*70}")
        print(f"  總搜尋次數: {self.stats['total_searches']}")
        print(f"  總發現數: {self.stats['total_findings']}")
        print(f"  驗證通過: {self.stats['verified_findings']}")
        print(f"  假陽性: {self.stats['false_positives']}")
        print(f"  報告已儲存: {output_file}")
        print(f"{'='*70}\n")


def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub Intelligence Collector v2.0")
    parser.add_argument("--type", help="憑證類型 (github_token, aws_access_key, etc.)")
    parser.add_argument("--limit", type=int, default=10, help="每種類型的搜尋限制")
    parser.add_argument("--output", default="intelligence_report.json", help="輸出檔案")
    parser.add_argument("--list-types", action="store_true", help="列出所有憑證類型")
    
    args = parser.parse_args()
    
    collector = GitHubIntelCollector()
    
    if args.list_types:
        print("\n可用的憑證類型:\n")
        for cred_type, cred_info in collector.CREDENTIAL_PATTERNS.items():
            print(f"  {cred_type:20s} - {cred_info['description']} ({cred_info['risk']})")
        print()
        return
    
    # 執行蒐證
    collector.collect_intelligence(args.type, args.limit)
    
    # 生成報告
    collector.generate_report(args.output)


if __name__ == "__main__":
    main()
