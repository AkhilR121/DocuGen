@echo off
echo ========================================
echo Starting DocuGen FastAPI Server
echo ========================================
echo.

REM Check if Poetry is installed
where poetry >nul 2>nul
if errorlevel 1 (
    echo ERROR: Poetry is not installed!
    echo Please install Poetry from: https://python-poetry.org/docs/#installation
    echo.
    echo Windows installation:
    echo ^(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing^).Content ^| py -
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist ".venv\Scripts\python.exe" (
    if not exist "venv\Scripts\python.exe" (
        echo Installing dependencies...
        poetry install
        if errorlevel 1 (
            echo Failed to install dependencies
            pause
            exit /b 1
        )
    )
)

REM Environment selection
set ENV_NAME=local
if "%1" neq "" set ENV_NAME=%1

echo.
echo Environment: %ENV_NAME%
echo Starting server on http://localhost:8080
echo Docs available at http://localhost:8080/docs
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Run the server
poetry run python run.py --env %ENV_NAME%
