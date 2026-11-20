import os
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

ARCHIVE_URL = "https://www.modelscope.cn/models/FlowerCry/gpt-sovits-7z-pacakges/resolve/master/GPT-SoVITS-v4-20250422fix.7z"
SAVE_ARCHIVE = Path("D:/GPT-SoVITS-v4.7z")
EXTRACT_DIR = Path("D:/")
WINRAR_EXE = Path("C:/Program Files/WinRAR/WinRAR.exe")


def download_package():
    print(f"=== 开始从魔搭社区高速拉取 GPT-SoVITS 完整环境整合包 ===")
    print(f"目标下载地址: {ARCHIVE_URL}")
    print(f"临时存储路径: {SAVE_ARCHIVE.resolve()}")

    if SAVE_ARCHIVE.exists() and SAVE_ARCHIVE.stat().st_size > 7 * 1024 * 1024 * 1024:
        print("[Check] 检测到已有完整压缩包，跳过下载步骤。")
        return

    req = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "Mozilla/5.0"})
    t0 = time.time()
    last_log = time.time()

    with urllib.request.urlopen(req) as resp, open(SAVE_ARCHIVE, "wb") as out_f:
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 4 * 1024 * 1024  # 4MB buffer

        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_f.write(chunk)
            downloaded += len(chunk)

            if time.time() - last_log > 5:
                mb_down = downloaded / (1024 * 1024)
                mb_tot = total / (1024 * 1024)
                speed = mb_down / max(1, time.time() - t0)
                pct = mb_down / mb_tot * 100 if mb_tot > 0 else 0
                print(f"[下载进度] {mb_down:.1f}MB / {mb_tot:.1f}MB ({pct:.1f}%) | 速度: {speed:.2f} MB/s")
                last_log = time.time()

    elapsed = time.time() - t0
    print(f"=== 下载完成！共计耗时 {elapsed:.1f} 秒 ===")


def extract_package():
    if not SAVE_ARCHIVE.exists():
        print(f"[Error] 压缩包不存在: {SAVE_ARCHIVE}")
        return

    print(f"=== 开始通过 WinRAR 解压到 D: 盘根目录 ... ===")
    t0 = time.time()
    cmd = [
        str(WINRAR_EXE),
        "x",
        "-ibck",
        "-y",
        "-o+",
        str(SAVE_ARCHIVE.resolve()),
        str(EXTRACT_DIR.resolve())
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"=== 解压完成，耗时 {time.time() - t0:.1f} 秒 ===")
        # 解压完成后清理 7.5GB 的压缩包，释放磁盘空间
        SAVE_ARCHIVE.unlink(missing_ok=True)
        print("[Cleanup] 已清理临时安装包。")
    except Exception as e:
        print(f"[Extract Error] 解压出错: {e}")


if __name__ == "__main__":
    download_package()
    extract_package()
    print("=== GPT-SoVITS 深度学习环境部署完毕 ===")
