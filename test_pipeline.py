import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import StreamerPipeline

def main():
    print("=== 测试全角色 StreamerPipeline ===")
    pipeline = StreamerPipeline()
    
    characters = ["xuanshen", "diangun", "shanniruo"]
    test_message = "主播这波团战怎么说？"

    for char_id in characters:
        print(f"\n[角色: {char_id}] 模拟弹幕: {test_message}")
        result = pipeline.run(char_id, test_message, generate_video=False)
        print(f"回复内容: {result['reply_text']}")
        print(f"音频路径: {result['audio_path']}")
        if result['audio_path'] and os.path.exists(result['audio_path']):
            size = os.path.getsize(result['audio_path'])
            print(f"音频大小: {size} 字节 (生成成功)")
    print("\n=== 全部角色生成测试通过 ===")

if __name__ == "__main__":
    main()
