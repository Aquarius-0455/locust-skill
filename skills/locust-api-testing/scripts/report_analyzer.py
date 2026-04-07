import os
import glob
import re
import json
import sys

def get_latest_report(report_dir):
    try:
        reports = glob.glob(os.path.join(report_dir, "locust_report_*.html"))
        if not reports:
            return None
        return max(reports, key=os.path.getmtime)
    except Exception as e:
        print(f"Error finding latest report: {e}")
        return None

def extract_metrics(html_content):
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html_content, re.DOTALL)
    if len(scripts) < 2:
        return None
    
    # Locust report data is typically found injected in one of the scripts
    data_script = ""
    start_str = 'window.templateArgs = '
    
    for script in scripts:
        if start_str in script:
            data_script = script
            break
            
    if not data_script:
        return None
        
    end_str = 'window.theme ='
    start_idx = data_script.find(start_str)
    if start_idx == -1:
        return None
        
    start_idx += len(start_str)
    end_idx = data_script.find(end_str, start_idx)
    
    if end_idx == -1:
        raw = data_script[start_idx:].strip()
    else:
        raw = data_script[start_idx:end_idx].strip()
        
    # Remove trailing semicolon if exists
    if raw.endswith(';'):
        raw = raw[:-1].strip()
        
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None

def main():
    # ⚠️ 修复：必须第一时间设置输出编码，否则 Windows 终端遇到中文/Emoji 会崩
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_dir = os.path.join(base_dir, 'report')
    latest_report = get_latest_report(report_dir)
    
    if not latest_report:
        print("❌ 未找到测试报告，请先执行压测！")
        sys.exit(1)
        
    try:
        with open(latest_report, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f"❌ 无法读取报告文件: {e}")
        sys.exit(1)
        
    data = extract_metrics(html)
    if not data:
        print("❌ 无法从 HTML 报告中提取指标数据，报告格式可能已更改。")
        sys.exit(1)
        
    print(f"=== 📄 报告智能解析结果 ===")
    print(f"【报告文件】: {os.path.basename(latest_report)}")
    print(f"【测试目标】: {data.get('host')}")
    print(f"【压测时长】: {data.get('duration')}")
    print(f"【测试时间】: {data.get('start_time')} 至 {data.get('end_time')}")
    
    # ⚠️ 修复：user_count 是 [timestamp, value] 列表，需防御性取值，防止 None 或非列表崩溃
    history = data.get('history', [])
    peak_users = 0
    peak_rps = 0.0
    if history:
        for entry in history:
            uc = entry.get('user_count')
            if isinstance(uc, list) and len(uc) >= 2 and isinstance(uc[1], (int, float)):
                if uc[1] > peak_users:
                    peak_users = int(uc[1])
            rps_entry = entry.get('current_rps')
            if isinstance(rps_entry, list) and len(rps_entry) >= 2 and isinstance(rps_entry[1], (int, float)):
                if rps_entry[1] > peak_rps:
                    peak_rps = rps_entry[1]
    print(f"【峰值并发用户数 (Peak Users)】: {peak_users}")
    print(f"【历史峰值 RPS (Peak RPS)】: {peak_rps:.2f} req/s")
    
    print("\n--- 📈 接口性能统计 (Requests Statistics) ---")
    req_stats = data.get('requests_statistics', [])
    # 分离各接口与汇总行，多接口时先打印各接口，再打印汇总
    individual_stats = [s for s in req_stats if s.get('name') != 'Aggregated']
    aggregated_stats = [s for s in req_stats if s.get('name') == 'Aggregated']
    print(f"共检测到 {len(individual_stats)} 个接口")
    
    for stat in individual_stats + aggregated_stats:
        name = stat.get('name')
        method = stat.get('method')
        display_name = "🧮 汇总 (Aggregated)" if name == "Aggregated" else f"[{method}] {name}"
        
        reqs = stat.get('num_requests', 0)
        fails = stat.get('num_failures', 0)
        fail_rate = (fails / reqs * 100) if reqs > 0 else 0
        total_rps = stat.get('total_rps', 0)
        current_rps = stat.get('current_rps', 0)
        avg_rt = stat.get('avg_response_time', 0)
        min_rt = stat.get('min_response_time', 0)
        max_rt = stat.get('max_response_time', 0)
        median_rt = stat.get('median_response_time', 0)
        
        print(f"🔹 {display_name}:")
        print(f"   请求总数: {reqs} | 失败数: {fails} (失败率: {fail_rate:.2f}%)")
        print(f"   全程平均 RPS: {total_rps:.2f} | 压测结束瞬时 RPS: {current_rps:.2f}")
        print(f"   响应时间: 平均={avg_rt:.0f}ms | 中位数={median_rt:.0f}ms | 最小={min_rt:.0f}ms | 最大={max_rt:.0f}ms")

    print("\n--- ⏱️ 响应时间分布 (Percentiles) ---")
    rt_stats = data.get('response_time_statistics', [])
    individual_rt = [s for s in rt_stats if s.get('name') != 'Aggregated']
    aggregated_rt = [s for s in rt_stats if s.get('name') == 'Aggregated']
    
    for stat in individual_rt + aggregated_rt:
        name = stat.get('name')
        method = stat.get('method')
        display_name = "🧮 汇总 (Aggregated)" if name == "Aggregated" else f"[{method}] {name}"
        
        p50 = float(stat.get('0.5', 0) or 0)
        p90 = float(stat.get('0.9', 0) or 0)
        p95 = float(stat.get('0.95', 0) or 0)
        p99 = float(stat.get('0.99', 0) or 0)
        
        print(f"🔸 {display_name}:")
        print(f"   P50: {p50:.0f}ms | P90: {p90:.0f}ms | P95: {p95:.0f}ms | P99: {p99:.0f}ms")
        
    # [优化项]：顺便将干净的 JSON 数据落盘保存为 latest_metrics.json，方便 AI 环境或者后续程序直接调阅，杜绝 Windows 终端排版截断问题
    dump_path = os.path.join(report_dir, "latest_metrics.json")
    try:
        with open(dump_path, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)
        print(f"\n✅ 机器提纯版纯净 JSON 数据已备份至: {dump_path}")
    except Exception as e:
        pass
        
    print("\n===============================")
    print("🤖 请 Agent 根据以上数据，按照 SKILL.md 定义的格式，为用户输出最终的 AI 性能分析结论。")

if __name__ == '__main__':
    main()
