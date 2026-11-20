import os
import sys
import time
import zipfile
import urllib.request
import urllib.parse
from pathlib import Path

TARGETS = [
    ("山泥若.zip", "shanniruo"),
    ("炫狗.zip", "xuanshen"),
    ("电棍.zip", "diangun")
]

BASE_DIR = Path("d:/manbo物理教学/streamer-ai-persona/data/raw_audio")
BASE_URL = "https://huggingface.co/datasets/XzJosh/audiodataset/resolve/main/"


def download_file(filename: str, out_folder: str):
    folder_path = BASE_DIR / out_folder
    folder_path.mkdir(parents=True, exist_ok=True)
    zip_path = BASE_DIR / filename

    encoded_name = urllib.parse.quote(filename)
    url = BASE_URL + encoded_name

    print(f"[{out_folder}] 开始下载: {filename} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    start_time = time.time()
    with urllib.request.urlopen(req) as resp, open(zip_path, "wb") as out_f:
        total_size = int(resp.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024  # 1MB
        last_log = time.time()

        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_f.write(chunk)
            downloaded += len(chunk)
            if time.time() - last_log > 2:
                mb_down = downloaded / (1024 * 1024)
                mb_tot = total_size / (1024 * 1024)
                print(f"[{out_folder}] 进度: {mb_down:.1f}MB / {mb_tot:.1f}MB ({mb_down/mb_tot*100:.1f}%)")
                last_log = time.time()

    elapsed = time.time() - start_time
    print(f"[{out_folder}] 下载完成，耗时 {elapsed:.1f} 秒。正在解压...")

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(folder_path)
        print(f"[{out_folder}] 解压完成！解压目录: {folder_path.resolve()}")
    except Exception as e:
        print(f"[{out_folder}] 解压失败: {e}")
    finally:
        if zip_path.exists():
            zip_path.unlink()  # 删除压缩包节省磁盘空间


def main():
    print("=== 开始批量下载主播语音切片数据集 ===")
    for filename, folder in TARGETS:
        download_file(filename, folder)
    print("=== 全部素材下载解压完成！ ===")


if __name__ == "__main__":
    main()
