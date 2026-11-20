import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import StreamerPipeline

def main():
    print("=== 测试 StreamerPipeline ===")
    pipeline = StreamerPipeline()
    test_message = "主播你这把选什么英雄上分？"
    print(f"模拟弹幕: {test_message}")
    
    result = pipeline.run("xuanshen", test_message, generate_video=False)
    print("\n--- 生成结果 ---")
    print(f"回复内容: {result['reply_text']}")
    print(f"音频路径: {result['audio_path']}")
    if result['audio_path'] and os.path.exists(result['audio_path']):
        size = os.path.getsize(result['audio_path'])
        print(f"音频大小: {size} 字节 (生成成功)")
    print("=================")

if __name__ == "__main__":
    main()
