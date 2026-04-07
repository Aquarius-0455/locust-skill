# 🦗 Locust Skill for Claude Code

> **AI 驱动的高级 API 高并发压测框架**

本项目是一套基于 Locust 构建的自动化、配置驱动型压测方案。它集成了接口活性探测、多接口偏移权重管理、AI 性能分析以及自动化的 HTML 报告生成功能。

---

## 📂 项目结构 (Structure)

为了保持代码库的整洁与可移植性，项目采用了“零污染”设计模式：

*   **`config/`**：核心配置中心。
    *   `api_config.json`：**唯一**需要操作的文件，统一定义压测目标、Header 和并发策略。
*   **`scripts/`**：基础设施脚本（严禁直接修改逻辑）。
    *   `locust_client.py`：压测执行引擎。
    *   `api_validator.py`：接口活性嗅探（冒烟测试）。
    *   `report_analyzer.py`：AI 报告数据提取器。
    *   `response_viewer.py`：接口响应格式化预览。
*   **`examples/`**：压测配置模板库。
*   **`resources/`**：项目关联的外部材料（如 Swagger、Postman 脚本等）。
*   **`report/`**：压测结果存储（自动按时间戳保存本地 HTML 报告）。

---

## ⚡ 快速开始 (Quick Start)

1.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

2.  **配置任务**
    在 `config/api_config.json` 中配置您的接口请求信息。

3.  **运行压测**
    我（AI 助手）会自动按照以下流程执行：
    - **Step 1**: 执行 `python scripts/api_validator.py` 验证接口通畅。
    - **Step 2**: 经过您的确认后，启动 `python scripts/locust_client.py` 开始压测。
    - **Step 3**: 自动打开浏览器预览 HTML 报告。

---

## 🤖 AI 增强功能

您可以直接对我下达这类指令：
- “提取这个 cURL，帮我写入配置并执行冒烟测试。”
- “帮我分析一下刚才的压测报告，看看瓶颈在哪。”
- “系统性能达标了吗？” —— AI 将结合 P95 和失败率给出量化结论。

---

## 📜 维护准则

- **配置驱动**：一切更改应通过 `api_config.json` 完成，而非修改 Python 代码。
- **文档一致性**：`SKILL.md` 是 AI 的核心指令集，如果您需要调整 AI 的工作流逻辑，请修改该文件。

---

## ⚠️ 免责声明 (Disclaimer)
本项目仅供学习、研究与自动化测试使用。在进行压测前，请务必获得目标系统所有者的明确授权。
