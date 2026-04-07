# -*- coding:UTF-8 -*-
"""
AI 接口验证引擎 (Health Checker)
同步验证：目标接口连通性。确认通畅后方可拉起压测。
"""
import os
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_endpoints():
    """执行接口前置冒烟测试 - AI 动态解析版"""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "api_config.json"))
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
        
    targets = config.get("targets", [])
    if not targets:
        print("⚠️ 未载入任何测试目标，跳过健康检查。")
        return True
        
    global_headers = config.get("headers", {})
    
    print("\n🚦 " + "="*20 + " 目标接口可达性检测 " + "="*20)
    
    all_passed = True
    for t in targets:
        try:
            print(f"  🔍 嗅探 [{t['name']}]: {t['url'][:50]}...")
            merged_headers = {**global_headers, **t.get("headers", {})}
            if t.get("method", "GET").upper() == "POST":
                resp = requests.post(t['url'], headers=merged_headers, json=t.get("json"), verify=False, timeout=10)
            else:
                resp = requests.get(t['url'], headers=merged_headers, verify=False, timeout=10)
                
            if resp.status_code < 400:
                print(f"  ✅ [{t['name']}] 通过 (HTTP {resp.status_code})")
            else:
                print(f"  ❌ [{t['name']}] 失败 (HTTP {resp.status_code}) 内容: {resp.text[:50]}")
                all_passed = False
        except Exception as e:
            print(f"  ❌ [{t['name']}] 错误: {e}")
            all_passed = False
            
    print("="*62 + "\n")
    return all_passed

if __name__ == "__main__":
    check_endpoints()
