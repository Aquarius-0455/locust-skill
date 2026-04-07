# -*- coding:UTF-8 -*-
"""
🔬 Locust 动态注入脚本 (AI 驱动版)
适配：根据配置文件动态生成压测任务
"""
import sys
import os
import json
import subprocess
import webbrowser
from locust.main import main
# 修复问题1：改用 HttpUser（基于 requests）替换 FastHttpUser
# FastHttpUser 的 geventhttpclient 会强制拼接 host，导致跨域 URL 请求地址错误
# HttpUser 内部使用 requests.Session，天然支持绝对地址，跨域压测无障碍
from locust import task, HttpUser, between

# 动态加载测试配置
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "api_config.json"))
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
except Exception as e:
    print(f"❌ 严重错误: 无法读取 {CONFIG_PATH}\n详细信息: {e}")
    sys.exit(1)

# --- 从配置项加载 ---
concurrency_cfg = config.get("concurrency", {})
USERS = concurrency_cfg.get("users", 20)
SPAWN_RATE = concurrency_cfg.get("spawn_rate", 2)
RUN_TIME = concurrency_cfg.get("run_time", "30s")
TARGET_TITLE = config.get("name", "AI 动态下发接口压测")

TARGET_ENDPOINTS = config.get("targets", [])
COMMON_HEADERS = config.get("headers", {})
EXTRACTED_HOST = config.get("host", "http://localhost")

class UniversalLoadTester(HttpUser):
    host = EXTRACTED_HOST  # 作为默认基准地址；如果任务使用绝对 URL 则会直接使用它
    wait_time = between(1.0, 2.0)
    tasks = [] # 动态任务池


# 将矩阵转化为 Locust 任务池
print(f"\n🧩 正在动态构建任务矩阵...")
for endpoint in TARGET_ENDPOINTS:
    def create_task(ep_config=endpoint):
        def dynamic_task(self):
            method = ep_config.get("method", "GET").upper()
            headers = {**COMMON_HEADERS, **ep_config.get("headers", {})}
            # verify=False: 防止内网/staging 环境 SSL 证书验证失败
            req_kwargs = {"headers": headers, "name": ep_config['name'], "verify": False}
            
            # 支持传入 JSON body (application/json)
            if "json" in ep_config:
                req_kwargs["json"] = ep_config["json"]
            # 支持传入 Form Data (application/x-www-form-urlencoded)
            if "data" in ep_config:
                req_kwargs["data"] = ep_config["data"]
                
            # 采用底层的 request 进行动态全量 HTTP 动词支持 (PUT/DELETE/PATCH 等均可)
            self.client.request(method, ep_config['url'], **req_kwargs)
            
        return dynamic_task

    # 按权重装载
    weight = endpoint.get('weight', 1)
    print(f"  📦 注册任务: [{endpoint['name']}] (权重: {weight})")
    for _ in range(weight):
        UniversalLoadTester.tasks.append(create_task(endpoint))

if __name__ == '__main__':
    from datetime import datetime
    import glob
    
    report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report'))
    os.makedirs(report_dir, exist_ok=True)
    
    # 1. 清理过期报告：只保留最新的五份以内
    try:
        existing_reports = sorted(glob.glob(os.path.join(report_dir, 'locust_report_*.html')), key=os.path.getmtime)
        # 如果已经存在 >=5 份，就删掉最老的，腾出位置给接下来这一份
        while len(existing_reports) >= 5:
            oldest = existing_reports.pop(0)
            os.remove(oldest)
    except Exception as e:
        print(f"⚠️ 自动清理旧报告失败: {e}")

    # 2. 动态生成当前任务报告名称
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f'locust_report_{timestamp}.html')
    
    sys.argv = [
        "locust", "-f", __file__, "--headless", 
        "-u", str(USERS), "-r", str(SPAWN_RATE), "-t", RUN_TIME, 
        "-H", EXTRACTED_HOST, "--html", report_path
    ]
    
    print(f"\n🌍 {TARGET_TITLE} 启动中...")
    print(f"🎯 主测目标: {EXTRACTED_HOST}")
    print(f"👥 并发兵力: {USERS} | ⏳ 持续时间: {RUN_TIME}")
    print(f"✅ 已装载 {len(TARGET_ENDPOINTS)} 个跨域接口任务，火力全开...")
    
    try:
        main()
    except SystemExit:
        pass
    finally:
        print(f"\n🌐 任务达成，测试报表已落盘！")
        if os.path.exists(report_path):
            try:
                webbrowser.open("file:///" + report_path.replace("\\", "/"))
            except Exception as e:
                print(f"⚠️ 报告已生成但自动打开失败: {e}")
        else:
            print("❌ 压测数据落盘失败。")
