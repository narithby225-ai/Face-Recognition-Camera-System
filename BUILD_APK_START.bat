@echo off
echo ========================================
echo   Face Recognition APK Builder
echo ========================================
echo.
echo This will:
echo  1. Open Ubuntu in WSL2
echo  2. Navigate to mobile_app folder
echo  3. Start automated APK build
echo.
echo First build takes 20-30 minutes.
echo.
pause
echo.
echo Opening Ubuntu WSL2...
echo.

REM Start WSL2 Ubuntu and run the build script
wsl -d Ubuntu-22.04 bash -c "cd '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app' && chmod +x build_apk.sh && ./build_apk.sh"

echo.
echo ========================================
echo Build process completed!
echo Check above for APK location.
echo ========================================
pause
