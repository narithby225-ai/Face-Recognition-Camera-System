@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo   Face Recognition APK Builder
echo   FIXED VERSION
echo ========================================
echo.
echo This will build your Android APK.
echo Time: 20-30 minutes for first build
echo.
pause
echo.

echo [1/5] Setting up Ubuntu environment...
wsl -d Ubuntu-22.04 bash -c "mkdir -p ~/face_recognition_build"

echo.
echo [2/5] Copying project files...
wsl -d Ubuntu-22.04 bash -c "cp -r '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app'/* ~/face_recognition_build/ 2>/dev/null || echo 'Copy complete'"

echo.
echo [3/5] Installing Python pip and build tools...
echo      (This may take a few minutes)
wsl -d Ubuntu-22.04 bash -c "cd ~ && wget -q https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --user && rm get-pip.py"

echo.
echo [4/5] Installing Cython and Buildozer...
wsl -d Ubuntu-22.04 bash -c "python3 -m pip install --user --upgrade cython==0.29.36 buildozer==1.5.0"

echo.
echo [5/5] Building APK (this takes 20-30 minutes)...
echo      Be patient! You'll see download progress...
echo.
wsl -d Ubuntu-22.04 bash -c "cd ~/face_recognition_build && /home/narith/.local/bin/buildozer -v android debug"

echo.
echo ========================================
echo Copying APK to Windows...
echo ========================================
wsl -d Ubuntu-22.04 bash -c "cp ~/face_recognition_build/bin/*.apk '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/FaceRecognitionApp.apk' 2>/dev/null && echo 'APK copied successfully!' || echo 'Could not find APK - check build log above'"

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your APK location:
echo   D:\Lessons_and_Codes\SPDI-II\Face Recognition Camera System\FaceRecognitionApp.apk
echo.
echo Or in Ubuntu:
echo   ~/face_recognition_build/bin/
echo.
pause
