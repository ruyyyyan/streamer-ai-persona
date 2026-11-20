# AI 虚拟主播与数字人多模态交互框架 (Streamer AI Persona)

本项目提供了一个轻量、模块化的虚拟主播 / AI 智能体开发框架，将**大模型人设对话**、**语音合成 (TTS)** 与 **数字人面部动画驱动** 串联整合，支持快速搭建具有独特对话风格与音色的互动数字人。

---

## 架构设计

整体工作流程分为三层解耦设计：

1. **对话生成层 (`src/llm`)**：负责角色扮演与文本回复生成。支持接入任意兼容 OpenAI 规范的 API（如 DeepSeek、通义千问等）或本地开源模型（如 Ollama）。
2. **语音渲染层 (`src/tts`)**：负责将文本转化为目标音色音频。默认内置 edge-tts 方便开箱即测，同时预留了对 GPT-SoVITS 等音色克隆服务的调用接口。
3. **视觉驱动层 (`src/video`)**：负责根据音频驱动静态人物立绘生成说话视频（支持对接 LivePortrait 或 SadTalker 等动态数字人后端）。
4. **交互层 (`webui.py`)**：基于 Gradio 构建的可视化测试界面。

---

## 快速上手

### 1. 安装环境依赖

建议在 Python 3.10+ 环境下运行：

```bash
pip install -r requirements.txt
```

### 2. 配置说明

- 角色与音色配置位于 `configs/characters.yaml`。
- 人设提示词（System Prompt）模板位于 `configs/prompts/` 目录下。你可以根据需要添加或修改不同角色的说话风格与设定。
- 如果需要调用大模型，可通过环境变量设置 API Key：
  ```bash
  # Windows PowerShell
  $env:OPENAI_API_KEY="your-api-key"
  $env:OPENAI_BASE_URL="https://api.deepseek.com" # 或其他兼容端点
  ```
  *(若未配置 API Key，系统将自动启用本地离线模拟模式以保障基础流程跑通)*

### 3. 启动交互界面

运行 WebUI：

```bash
python webui.py
```
启动后在浏览器中访问 `http://127.0.0.1:7860` 即可开始测试互动。

---

## 如何关联并推送到 GitHub

1. 在 GitHub 上点击右上角 **New** 新建一个空白仓库（例如命名为 `streamer-ai-persona`），不要勾选初始化 README。
2. 在本地项目根目录运行以下命令关联远程仓库并推送：

```bash
git remote add origin https://github.com/<你的用户名>/<仓库名称>.git
git branch -M main
git push -u origin main
```

---

## 声明与规范

1. 本项目为开源框架与技术演示，供个人研究、学术交流及本地开发参考。
2. 使用自定义角色与语音模型时，请遵守相关法律法规，尊重自然人的人格权、肖像权与声音权。
3. 严禁利用本项目从事商业侵权、造谣、欺诈或冒名传播等违法行为。发布合成内容时请遵守相关规定并明确注明 AI 生成标识。
