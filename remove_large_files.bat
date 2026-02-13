@echo off
echo ========================================
echo GitHub Upload Preparation Script
echo ========================================
echo.

REM Check if .git exists
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Add .gitignore first
echo [1/4] Adding .gitignore...
git add .gitignore

REM Remove large files if they exist in git
echo [2/4] Removing large files from Git tracking...
for /d %%i in (data outputs instance backend\instance) do (
    git rm -r --cached %%i 2>nul
)
git rm --cached backend\models\*.pkl 2>nul

REM Add all remaining files
echo [3/4] Adding project files...
git add .

echo [4/4] Checking status...
git status

echo.
echo ========================================
echo Preparation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. git commit -m "Initial commit"
echo 2. git remote add origin YOUR_GITHUB_URL
echo 3. git branch -M main
echo 4. git push -u origin main
echo.
pause
