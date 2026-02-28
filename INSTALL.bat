@echo off
setlocal enabledelayedexpansion

:: =======================================================
:: XTTSv2 Gradio Portable Installer (coqui-tts Edition)
:: =======================================================

echo [0/6] Checking for Microsoft Visual C++ Redistributable...
set "VC_REDIST_URL=https://aka.ms/vs/17/release/vc_redist.x64.exe"
powershell -Command "try { $reg = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64' -ErrorAction SilentlyContinue; if ($reg.Version -lt '14.30') { throw 'Old version' } echo 'VC++ Redist is already installed.' } catch { echo 'VC++ Redist is missing or outdated. Downloading...'; Invoke-WebRequest -Uri '%VC_REDIST_URL%' -OutFile 'vc_redist.x64.exe'; echo 'Installing VC++ Redist... Please wait.'; Start-Process -FilePath 'vc_redist.x64.exe' -ArgumentList '/install /quiet /norestart' -Wait; Remove-Item 'vc_redist.x64.exe'; echo 'VC++ Redist installed.' }"

echo [1/6] Preparing Python 3.10.9 Embedded...
set "PY_URL=https://www.python.org/ftp/python/3.10.9/python-3.10.9-embed-amd64.zip"
set "PY_DIR=python_embed"
set "ZIP_FILE=python_embed.zip"

if not exist "%PY_DIR%" (
    echo Downloading Python...
    powershell -Command "Invoke-WebRequest -Uri '%PY_URL%' -OutFile '%ZIP_FILE%'"
    echo Extracting Python...
    powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%PY_DIR%' -Force"
    del "%ZIP_FILE%"
)

echo [2/6] Configuring Python (Fixing ._pth)...
set "PTH_FILE=%PY_DIR%\python310._pth"
if exist "%PTH_FILE%" (
    (
        echo python310.zip
        echo .
        echo import site
    ) > "%PTH_FILE%"
)

echo [3/6] Bootstrapping pip...
if not exist "get-pip.py" (
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"
)
"%PY_DIR%\python.exe" get-pip.py --no-warn-script-location

echo [4/6] Creating virtual environment...
"%PY_DIR%\python.exe" -m pip install virtualenv --no-warn-script-location
if not exist "venv" (
    "%PY_DIR%\python.exe" -m virtualenv venv
)

echo [5/6] Installing dependencies (coqui-tts, torch cu128)...
call venv\Scripts\activate

:: Unified installation to avoid version conflicts and backtracking
echo Installing all dependencies... This may take a few minutes.
python -m pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu128 --no-cache-dir
python -m pip install -r requirements.txt

echo [6/6] Finalizing START_GRADIO.bat...
(
echo @echo off
echo call venv\Scripts\activate
echo python app.py
echo pause
) > START_GRADIO.bat

echo =======================================================
echo    Installation Complete!
echo    1. Use START_GRADIO.bat to launch the app.
echo    2. The first run might take a moment to download models.
echo =======================================================
pause

echo Starting application now...
venv\Scripts\python.exe app.py

pause
