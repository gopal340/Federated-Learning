@echo off
echo ========================================================
echo Starting Federated Qwen + JEV Decision Engine Backend
echo Device: NVIDIA CUDA (RTX 2050)
echo Port: 8000
echo ========================================================

cd /d "%~dp0backend"
"C:\Users\adavi\anaconda3\envs\sdp\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
