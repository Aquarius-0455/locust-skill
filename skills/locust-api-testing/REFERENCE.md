# 🔬 Locust API Testing Pro - 参考指南 (Reference)

本文档定义了 `api_config.json` 的核心字段及其取值范围。该文件是框架唯一的驱动源（Single Source of Truth）。

---

## 🛠️ 配置字段详情

### 1. 全局配置 (`root`)
- **`name`**: `String` | 压测任务的显示标题。
- **`host`**: `String` | 目标服务器的基础域名。
- **`headers`**: `Object` | 全局通用的请求头。
- **`concurrency`**: `Object` | 并发执行策略。
  - **`users`**: `Int` | 目标最大并发用户数。
  - **`spawn_rate`**: `Int` | 每秒启动用户数（数值越大，加载越快）。
  - **`run_time`**: `String` | 运行时间，格式如 `"60s"`, `"5m"`, `"1h"`。

---

### 2. 目标接口配置 (`targets`)
- **`name`**: `String` | 接口别名。
- **`url`**: `String` | 完整 URL 或相对于 `host` 的路径。
- **`method`**: `String` | 支持 `GET`, `POST`, `PUT`, `DELETE`, `PATCH`。
- **`weight`**: `Int` | 任务权重（例如：10 个任务里该接口出现的比例）。
- **`headers`**: `Object` | (可选) 接口特有的请求头，将与全局请求头合并。
- **`json`**: `Object` | (可选) `application/json` 请求体。
- **`data`**: `Object` | (可选) `form-data` 格式请求体。

---

## 🛡️ 安全注意事项
- 框架已在 `scripts/debug_api.py` 及 `.gitignore` 中默认过滤了敏感数据。
- 自行提交代码至公开仓库前，请务必执行 `git status` 确认配置文件的脱敏情况。

---

## 🏁 流程验证
配置完成后，必须执行：
`python scripts/api_validator.py`
验证通过后，方可启动正式压测。
