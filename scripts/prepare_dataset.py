"""
Audio preprocessing utility tips:
1. Extract clean vocal tracks from raw recordings using UVR5 (Ultimate Vocal Remover).
2. Slice long recordings into 3-10 second segments using ffmpeg or pydub.
3. Transcribe audio segments using Whisper/FunASR for TTS training datasets.
"""

import sys

def main():
    print("[Audio Preprocessing]")
    print("推荐音频预处理流程：")
    print("1. 使用 UVR5 (Ultimate Vocal Remover) 去除背景音乐和杂音，保留干净干音。")
    print("2. 使用 Whisper 或 FunASR 自动生成标注文本。")
    print("3. 单条音频切片长度保持在 3~10 秒，总有效时长建议在 10 分钟至 1 小时之间。")

if __name__ == "__main__":
    main()
