@echo off
echo ========================================
echo DSA Problem Tracker - Quick Deploy
echo ========================================
echo.

echo Step 1: Checking Git...
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git not found! Please install Git first:
    echo https://git-scm.com/download/win
    exit /b 1
)
echo [OK] Git found

echo.
echo Step 2: Initializing Git repository...
if not exist .git (
    git init
    echo [OK] Git repository initialized
) else (
    echo [OK] Git repository already exists
)

echo.
echo Step 3: Adding files to Git...
git add .
echo [OK] Files added

echo.
echo Step 4: Creating commit...
git commit -m "Deploy DSA Problem Tracker" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Commit created
) else (
    echo [INFO] No changes to commit or already committed
)

echo.
echo ========================================
echo Ready to Deploy!
echo ========================================
echo.
echo Choose your platform:
echo   1. Railway (Recommended)
echo   2. Render
echo   3. Push to GitHub only
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Deploying to Railway...
    echo.
    where railway >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [INFO] Railway CLI not found. Installing...
        npm install -g @railway/cli
    )
    railway login
    railway init
    railway up
    railway open
) else if "%choice%"=="2" (
    echo.
    echo For Render deployment:
    echo 1. Push your code to GitHub first
    echo 2. Go to https://dashboard.render.com/
    echo 3. Click "New +" and select "Web Service"
    echo 4. Connect your GitHub repository
    echo 5. Use these settings:
    echo    - Build Command: pip install -r requirements.txt ^&^& python init_database.py ^&^& python init_auth.py
    echo    - Start Command: gunicorn app:app
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    set /p repo="Enter your GitHub repository URL: "
    git remote add origin %repo%
    git branch -M main
    git push -u origin main
    echo.
    echo [OK] Code pushed to GitHub!
    echo Now you can deploy from Railway or Render dashboard.
) else (
    echo Invalid choice!
    exit /b 1
)

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
