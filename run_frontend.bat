@echo off
echo ========================================================
echo Starting Federated Qwen + JEV Decision Console Frontend
echo Port: 5173
echo ========================================================

cd /d "%~dp0frontend"
"C:\Program Files\nodejs\npm.cmd" run dev
pause
