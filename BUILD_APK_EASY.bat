@echo off
echo ========================================
echo   Face Recognition APK Builder
echo   (No Admin Required)
echo ========================================
echo.
echo This will build your Android APK.
echo First build takes 20-30 minutes.
echo.
echo NOTE: If prompted for password, just press Ctrl+C
echo       and the script will continue without sudo.
echo.
pause
echo.
echo Starting build process...
echo.

REM Run the no-sudo version
wsl -d Ubuntu-22.04 bash -c "cd '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app' && bash build_apk_no_sudo.sh"

echo.
echo ========================================
echo Build completed!
echo.
echo Your APK should be at:
echo   mobile_app\bin\facerecognition-1.0-armeabi-v7a-debug.apk
echo ========================================
echo.
pause
