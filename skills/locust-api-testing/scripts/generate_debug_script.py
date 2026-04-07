# -*- coding:UTF-8 -*-
"""
🛠️ 调试脚本生成器 (Debug Script Generator)
功能：从 config/api_config.json 提取信息，生成一个完全独立、零配置依赖的 debug_api.py。
"""
import json
import os
import sys

def main():
    # 路径定义
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config", "api_config.json")
    OUTPUT_PATH = os.path.join(BASE_DIR, "scripts", "debug_api.py")

    if not os.path.exists(CONFIG_PATH):
        print(f"❌ 错误: 找不到配置文件 {CONFIG_PATH}")
        return

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 错误: 读取配置文件失败: {e}")
        return

    name = config.get("name", "Default Test")
    common_headers = config.get("headers", {})
    targets = config.get("targets", [])

    # 开始编写脚本
    content = f"""# -*- coding:UTF-8 -*-
\"\"\"
🚀 临时调试脚本 - 由项目自动生成
此脚本用于快速查看接口返回，不依赖外部环境。
生成时间: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}
\"\"\"
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
GLOBAL_HEADERS = {json.dumps(common_headers, indent=4, ensure_ascii=False)}

def test_interfaces():
    print("=" * 70)
    print(f"🔍 接口快速预览: {name}")
    print("=" * 70)
"""

    for i, t in enumerate(targets, 1):
        t_method = t.get("method", "GET").upper()
        t_url = t.get("url", "")
        t_name = t.get("name", f"Interface_{i}")
        t_headers = t.get("headers", {})
        t_json = t.get("json")
        t_data = t.get("data")

        content += f"""
    # --- [{i}/{len(targets)}] {t_name} ---
    print(f"\\n▶️  正在请求: {t_name}")
    print(f"   {t_method} {t_url}")
    
    try:
        resp = requests.request(
            method="{t_method}",
            url="{t_url}",
            headers={{**GLOBAL_HEADERS, **{json.dumps(t_headers, ensure_ascii=False)}}},
            verify=False,
            timeout=15,
            {f'json={json.dumps(t_json, ensure_ascii=False)},' if t_json else ''}
            {f'data={json.dumps(t_data, ensure_ascii=False)},' if t_data else ''}
        )
        
        print(f"✅ 状态码: {{resp.status_code}} {{resp.reason}}")
        
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
        print(f"❌ 请求异常: {{e}}")
        
    print("-" * 70)
"""

    content += """
if __name__ == "__main__":
    test_interfaces()
"""

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✨ 成功！调试脚本已生成至: {OUTPUT_PATH}")
        print(f"💡 您可以随时运行 'python debug_api.py' 来查看接口返回。")
    except Exception as e:
        print(f"❌ 错误: 生成调试脚本失败: {e}")

if __name__ == "__main__":
    main()
