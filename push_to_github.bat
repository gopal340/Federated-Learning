@echo off
echo ========================================================
echo Pushing Federated Learning Project to GitHub:
echo https://github.com/gopal340/Federated-Learning
echo ========================================================
cd /d "%~dp0"

echo.
echo Running: git push -u origin main --force
echo If prompted, select "manager" or sign in with your GitHub account in browser.
echo.

git push -u origin main --force

echo.
echo ========================================================
echo Finished! Press any key to close.
echo ========================================================
pause
