@echo off
echo FFmpeg Installation Helper
echo ==========================
echo.

echo This script will help you install FFmpeg for better audio support.
echo.

echo Downloading FFmpeg...
echo.

REM Create temp directory
if not exist "temp" mkdir temp
cd temp

REM Download FFmpeg (Windows build)
echo Downloading FFmpeg for Windows...
curl -L -o "ffmpeg.zip" "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

if exist "ffmpeg.zip" (
    echo Extracting FFmpeg...
    powershell -command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force"
    
    REM Find the extracted folder
    for /d %%i in (ffmpeg-*) do (
        echo Found FFmpeg folder: %%i
        copy "%%i\bin\ffplay.exe" "..\ffplay.exe"
        copy "%%i\bin\ffmpeg.exe" "..\ffmpeg.exe"
        copy "%%i\bin\ffprobe.exe" "..\ffprobe.exe"
    )
    
    cd ..
    rmdir /s /q temp
    
    if exist "ffplay.exe" (
        echo.
        echo FFmpeg installed successfully!
        echo ffplay.exe, ffmpeg.exe, and ffprobe.exe are now in this folder.
        echo Audio playback should now work perfectly!
    ) else (
        echo.
        echo Installation failed. Please download FFmpeg manually from:
        echo https://ffmpeg.org/download.html
    )
) else (
    echo.
    echo Download failed. Please download FFmpeg manually from:
    echo https://ffmpeg.org/download.html
    echo.
    echo Extract ffplay.exe, ffmpeg.exe, and ffprobe.exe to this folder.
)

echo.
pause