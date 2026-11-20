@echo off
echo ========================================================
echo   正在启动 GPT-SoVITS 本地神经网络推理服务 (RTX 3070 加速)
echo ========================================================
cd /d "D:\GPT-SoVITS-v4-20250422fix"
.\runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
pause
