@echo off
echo ========================================================
echo   Starting GPT-SoVITS Inference Service (Port 9880)
echo ========================================================
cd /d "D:\GPT-SoVITS-v4-20250422fix"
.\runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
pause
