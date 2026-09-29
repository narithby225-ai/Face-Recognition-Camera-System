@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo   Face Recognition APK Builder
echo   SIMPLE METHOD
echo ========================================
echo.
echo This will:
echo  1. Copy project to Ubuntu home directory
echo  2. Build APK there (faster, no permission issues)
echo  3. Copy APK back to Windows
echo.
echo Time: 20-30 minutes for first build
echo.
pause
echo.

echo [1/4] Copying project to Ubuntu...
wsl -d Ubuntu-22.04 bash -c "mkdir -p ~/face_recognition_build && cp -r '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app'/* ~/face_recognition_build/"

echo.
echo [2/4] Installing build tools...
wsl -d Ubuntu-22.04 bash -c "python3 -m pip install --user --upgrade pip cython==0.29.36 buildozer==1.5.0"

echo.
echo [3/4] Building APK (this takes 20-30 minutes)...
echo      Please wait...
wsl -d Ubuntu-22.04 bash -c "cd ~/face_recognition_build && export PATH=$PATH:~/.local/bin && ~/.local/bin/buildozer -v android debug"

echo.
echo [4/4] Copying APK to Windows...
wsl -d Ubuntu-22.04 bash -c "cp ~/face_recognition_build/bin/*.apk '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/FaceRecognitionApp.apk' 2>/dev/null || echo 'APK not found - build may have failed'"

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo Your APK should be at:
echo   D:\Lessons_and_Codes\SPDI-II\Face Recognition Camera System\FaceRecognitionApp.apk
echo.
echo If not found, check for errors above.
echo.
pause
