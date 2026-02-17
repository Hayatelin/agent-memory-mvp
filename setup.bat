@echo off
REM ==============================================================================
REM AgentMem Installation Setup Script (Windows)
REM 一鍵安裝和配置 AgentMem
REM ==============================================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo           AgentMem - Quick Setup Script (Windows)
echo      ^>^>^> Automated Installation ^& Configuration ^<^<^<
echo ================================================================================
echo.

REM Check Python
echo [STEP] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    echo.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Check Git
echo [STEP] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git not found. Attempting to proceed anyway...
    echo.
    echo [INFO] If you need Git, visit: https://git-scm.com/download/win
    echo.
) else (
    for /f "tokens=3" %%i in ('git --version') do set GIT_VERSION=%%i
    echo [OK] Git %GIT_VERSION% found
    echo.
)

REM Clone repository
echo [STEP] Cloning AgentMem repository...
if exist "agent-memory-mvp" (
    echo [WARNING] Directory 'agent-memory-mvp' already exists.
    set /p OVERWRITE="Do you want to overwrite it? (y/n): "
    if /i "!OVERWRITE!"=="y" (
        rmdir /s /q agent-memory-mvp
        echo [INFO] Existing directory removed.
    ) else (
        echo [INFO] Using existing directory.
        goto :install_dependencies
    )
)

git clone https://github.com/Hayatelin/agent-memory-mvp.git
if errorlevel 1 (
    echo [ERROR] Failed to clone repository.
    echo [INFO] You can manually clone from: https://github.com/Hayatelin/agent-memory-mvp
    pause
    exit /b 1
)
echo [OK] Repository cloned successfully
echo.

:install_dependencies
echo [STEP] Installing Python dependencies...
cd agent-memory-mvp

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install requirements
if exist "requirements.txt" (
    echo [INFO] Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [WARNING] Some packages failed to install. Please check your internet connection.
    ) else (
        echo [OK] All dependencies installed successfully
    )
) else (
    echo [ERROR] requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Run initialization wizard
echo [STEP] Starting initialization wizard...
echo.

if exist "init_wizard.py" (
    python init_wizard.py
) else (
    echo [WARNING] init_wizard.py not found. Running manual setup...
    call :manual_setup
)

echo.
goto :show_next_steps

:manual_setup
echo [INFO] Setting up configuration manually...

REM Create config directory
if not exist "%USERPROFILE%\.agentmem" mkdir "%USERPROFILE%\.agentmem"

REM Check if config exists
if not exist "%USERPROFILE%\.agentmem\config.json" (
    echo [INFO] Generating default Agent ID...

    REM Create config file
    (
        echo {
        echo     "agent_id": "default-agent",
        echo     "api_url": "http://localhost:8000",
        echo     "database_type": "sqlite",
        echo     "database_url": "sqlite:///./agentmem.db"
        echo }
    ) > "%USERPROFILE%\.agentmem\config.json"

    echo [OK] Configuration file created at %USERPROFILE%\.agentmem\config.json
) else (
    echo [INFO] Configuration file already exists
)

exit /b 0

:show_next_steps
cls
echo.
echo ================================================================================
echo              ^>^>^> Installation Complete! ^<^<^<
echo ================================================================================
echo.

echo [INFO] Next steps to get started:
echo.
echo Step 1: Start the backend server (Terminal 1)
echo   cd agent-memory-mvp
echo   python -m src.main
echo.
echo Step 2: Start the Web UI (Terminal 2)
echo   cd agent-memory-mvp
echo   streamlit run ui/app.py
echo.
echo Step 3: Access the application
echo   * Web UI: http://localhost:8501
echo   * API: http://localhost:8000
echo   * API Docs: http://localhost:8000/docs
echo.

echo [INFO] Alternative ways to use AgentMem:
echo.
echo * Python SDK:
echo   python -c "from src.client import AgentMemClient; client = AgentMemClient()"
echo.
echo * Command Line Interface:
echo   python -m src.cli.main --help
echo.

echo [INFO] Useful documentation:
echo   * Quick Start: docs\QUICKSTART.md
echo   * Usage Guide: docs\USAGE_GUIDE.md
echo   * API Reference: docs\API_REFERENCE.md
echo   * Examples: docs\EXAMPLES.md
echo.

echo [INFO] Need help?
echo   * GitHub Issues: https://github.com/Hayatelin/agent-memory-mvp/issues
echo   * Documentation: https://github.com/Hayatelin/agent-memory-mvp#readme
echo.

echo ================================================================================
echo                     Happy coding! 🚀
echo ================================================================================
echo.

pause
