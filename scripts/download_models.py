"""
Helper script to download model checkpoints and weights
from ModelScope or Hugging Face Hub.
"""

def main():
    print("=" * 60)
    print("AI 虚拟主播项目 - 模型权重下载指南")
    print("=" * 60)
    print("1. GPT-SoVITS 语音克隆推理后端:")
    print("   请参考官方仓库部署独立服务: https://github.com/RVC-Boss/GPT-SoVITS")
    print("   启动 API 模式: python api.py -a 127.0.0.1 -p 9880")
    print("\n2. LivePortrait 动态肖像驱动后端:")
    print("   请参考官方仓库部署: https://github.com/KwaiVGI/LivePortrait")
    print("   或 SadTalker: https://github.com/OpenTalker/SadTalker")
    print("\n3. 大语言模型 (LLM):")
    print("   可使用本地 Ollama (如 qwen2.5) 或在线大模型 API (DeepSeek / OpenAI 兼容接口)。")
    print("=" * 60)

if __name__ == "__main__":
    main()
