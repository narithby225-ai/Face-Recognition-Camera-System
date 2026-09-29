@echo off
echo ========================================
echo   Face Recognition APK Builder
echo   FINAL STEP - Install Java and Build
echo ========================================
echo.
echo You're almost done!
echo Just need to install Java and build.
echo.
echo This will take 20-30 minutes for the build.
echo.
pause
echo.

echo [1/3] Installing Java JDK...
wsl -d Ubuntu-22.04 bash -c "sudo apt-get install -y openjdk-17-jdk"

echo.
echo [2/3] Building APK (20-30 minutes - be patient!)...
echo      You'll see download progress for SDK and NDK...
echo.
wsl -d Ubuntu-22.04 bash -c "cd ~/face_recognition_build && /home/narith/.local/bin/buildozer -v android debug"

echo.
echo [3/3] Copying APK to Windows...
wsl -d Ubuntu-22.04 bash -c "cp ~/face_recognition_build/bin/*.apk '/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/FaceRecognitionApp.apk' 2>/dev/null && echo 'SUCCESS! APK copied!' || echo 'Could not find APK'"

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your APK should be at:
echo   D:\Lessons_and_Codes\SPDI-II\Face Recognition Camera System\FaceRecognitionApp.apk
echo.
echo Install it on your phone and test!
echo.
pause
