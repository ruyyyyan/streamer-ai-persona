"""
Helper script to fetch and prepare voice material samples locally.
Note: Audio files are kept in local storage and excluded from Git commits via .gitignore.
"""

import os
import sys
import subprocess
from pathlib import Path


RAW_AUDIO_DIR = Path("data/raw_audio")


def ensure_dirs():
    RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[Init] Raw audio directory ready at: {RAW_AUDIO_DIR.resolve()}")


def check_ytdlp():
    try:
        subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception:
        return False


def download_from_url(url: str, output_name: str):
    ensure_dirs()
    if not check_ytdlp():
        print("[Error] yt-dlp 未安装，请先执行: pip install yt-dlp")
        return

    output_template = str(RAW_AUDIO_DIR / f"{output_name}.%(ext)s")
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", output_template,
        url
    ]
    print(f"[Download] 正在下载并提取音频: {url}")
    try:
        subprocess.run(cmd, check=True)
        print(f"[Success] 音频已成功保存至: {RAW_AUDIO_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"[Failed] 下载失败: {e}")


def print_material_guide():
    print("=" * 65)
    print("🎙️ 推荐素材获取与处理指南 (用于本地个人研究)")
    print("=" * 65)
    print("1. 电棍 (otto):")
    print("   - 开源活字印刷仓库资源: https://github.com/DSP-8192/HuoZiYinShua")
    print("   - HuggingFace 切片集: https://huggingface.co/datasets/XzJosh/audiodataset")
    print("\n2. 炫神:")
    print("   - HuggingFace Parrots 预训练发音人: https://huggingface.co/shibing624/parrots-gpt-sovits-speaker")
    print("\n3. 山泥若:")
    print("   - 推荐使用 B 站无 BGM 纯享切片或公开庭审原声（环境音最干净）")
    print("   - 运行示例: python scripts/fetch_materials.py <视频URL> shanniruo_sample")
    print("=" * 65)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        target_url = sys.argv[1]
        out_name = sys.argv[2]
        download_from_url(target_url, out_name)
    else:
        print_material_guide()
