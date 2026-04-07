# -*- coding:UTF-8 -*-
"""
🚀 临时调试脚本 - 由项目自动生成
此脚本用于快速查看接口返回，不依赖外部环境。
生成时间: 2026/04/07 周二 11:57
"""
import requests
import json
import urllib3
import sys

# 修复编码问题
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 基础全局配置
GLOBAL_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer <REDACTED_ACCESS_TOKEN>",
    "cookie": "access_token=\"<REDACTED_ACCESS_TOKEN>\"; current_user_id=<REDACTED_USER_ID>; current_tenant_code=<REDACTED_TENANT_ID>",
    "locale": "en-US",
    "referer": "https://<REDACTED_DOMAIN>/automation/product-designated-warehouse",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-tenant-id": "<REDACTED_TENANT_ID>",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

def test_interfaces():
    print("=" * 70)
    print(f"🔍 接口快速预览: SKU Warehouse Page Query Load Test")
    print("=" * 70)

    # --- [1/1] sku_warehouse_page ---
    print(f"\n▶️  正在请求: sku_warehouse_page")
    print(f"   GET https://<REDACTED_DOMAIN>/api/linker-oms/opc/app-api/sku-warehouse/page?pageNo=1&pageSize=10&merchantNo=<REDACTED_MERCHANT_NO>")
    
    try:
        resp = requests.request(
            method="GET",
            url="https://<REDACTED_DOMAIN>/api/linker-oms/opc/app-api/sku-warehouse/page?pageNo=1&pageSize=10&merchantNo=<REDACTED_MERCHANT_NO>",
            headers={**GLOBAL_HEADERS, **{}},
            verify=False,
            timeout=15,
            
            
        )
        
        print(f"✅ 状态码: {resp.status_code} {resp.reason}")
        
        try:
            # 尝试格式化 JSON 输出
            data = resp.json()
            print("📝 响应正文 (JSON):")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            # 非 JSON 输出
            print("📝 响应正文 (TEXT):")
            print(resp.text[:1000] + ("..." if len(resp.text) > 1000 else ""))
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        
    print("-" * 70)

if __name__ == "__main__":
    test_interfaces()
