# -*- coding:UTF-8 -*-
"""
🔍 接口响应快速预览脚本 (One-Off Response Viewer)
功能：读取 config/api_config.json，逐一发送请求并打印格式化后的响应结果。
用途：在压测前确认 Token 是否过期、接口数据是否正确、调试 Headers 等。
"""
import os
import json
import requests
import urllib3
import sys

# Windows 终端乱码修复
if sys.stdout.encoding != 'utf-8':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "api_config.json")

def main():
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ 配置文件不存在: {CONFIG_PATH}")
        return

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")
        return

    targets = config.get("targets", [])
    common_headers = config.get("headers", {})
    
    print(f"\n🚀 开始探测 [{config.get('name', 'Default')}] 中的接口响应...")
    print("=" * 60)

    for i, target in enumerate(targets, 1):
        name = target.get("name", "Unknown")
        url = target.get("url")
        method = target.get("method", "GET").upper()
        
        print(f"【{i}/{len(targets)}】测试接口: {name}")
        print(f"➡️  Method: {method}")
        print(f"➡️  URL: {url}")
        
        headers = {**common_headers, **target.get("headers", {})}
        
        req_kwargs = {
            "headers": headers,
            "verify": False,
            "timeout": 10
        }
        
        if "json" in target:
            req_kwargs["json"] = target["json"]
        if "data" in target:
            req_kwargs["data"] = target["data"]

        try:
            resp = requests.request(method, url, **req_kwargs)
            print(f"⬅️  Status: {resp.status_code} {resp.reason}")
            
            # 尝试 JSON 解析并美化打印
            try:
                body = resp.json()
                print("📝 Response Body (JSON):")
                print(json.dumps(body, indent=2, ensure_ascii=False))
            except:
                print("📝 Response Body (Text/HTML):")
                print(resp.text[:1000] + ("..." if len(resp.text) > 1000 else ""))
                
        except Exception as e:
            print(f"❌ 请求发生异常: {e}")
        
        print("-" * 60)

    print("\n✅ 所有接口探测完成！")

if __name__ == "__main__":
    main()
