# 📱 Build APK - Manual Steps (Guaranteed to Work!)

## 🎯 Follow These Steps Exactly

### Step 1: Open Ubuntu Terminal

In PowerShell, run:
```powershell
wsl -d Ubuntu-22.04
```

You should see something like:
```
narith@DESKTOP:~$
```

---

### Step 2: Create Build Directory

In Ubuntu terminal, run:
```bash
mkdir -p ~/face_recognition_build
cd ~/face_recognition_build
```

---

### Step 3: Copy Project Files

```bash
cp -r "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"/* .
ls
```

You should see: `main.py`, `buildozer.spec`, `facerecognition.kv`, etc.

---

### Step 4: Install pip (if not installed)

```bash
cd ~
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py
```

Wait for it to finish installing.

---

### Step 5: Install Buildozer

```bash
python3 -m pip install --user cython==0.29.36
python3 -m pip install --user buildozer==1.5.0
```

Verify installation:
```bash
ls ~/.local/bin/buildozer
```

Should show: `/home/narith/.local/bin/buildozer`

---

### Step 6: Go to Build Directory

```bash
cd ~/face_recognition_build
```

---

### Step 7: Build APK (This Takes 20-30 Minutes!)

```bash
~/.local/bin/buildozer -v android debug
```

**Now wait!** You'll see:
1. "Downloading Android SDK..." (~10 min)
2. "Downloading Android NDK..." (~5 min)
3. "Compiling..." (~10 min)
4. "Creating APK..." (~2 min)

☕ Grab coffee and be patient!

---

### Step 8: Check if APK Created

```bash
ls -lh bin/
```

You should see something like:
```
facerecognition-1.0-armeabi-v7a-debug.apk  (~150MB)
```

---

### Step 9: Copy APK to Windows

```bash
cp bin/*.apk /mnt/d/FaceRecognitionApp.apk
```

---

### Step 10: Verify on Windows

In PowerShell:
```powershell
dir D:\FaceRecognitionApp.apk
```

✅ **Success!** Your APK is ready!

---

## 📱 Install APK on Phone

1. Transfer `D:\FaceRecognitionApp.apk` to your phone
2. Tap the APK file
3. Allow "Install from Unknown Sources" if prompted
4. Install and open app
5. Grant camera permission
6. Tap "START CAMERA"
7. Test face recognition! 🎉

---

## 🐛 If Something Goes Wrong

### "wget: command not found"
```bash
sudo apt update
sudo apt install wget
```

### "buildozer not found"
```bash
# Use full path
~/.local/bin/buildozer --version
```

### "Permission denied"
```bash
chmod +x ~/.local/bin/buildozer
```

### Build fails
```bash
# Clean and retry
cd ~/face_recognition_build
rm -rf .buildozer
~/.local/bin/buildozer -v android debug
```

### "No space left"
```bash
# Check space (need 10GB)
df -h ~

# Clean if needed
rm -rf ~/face_recognition_build/.buildozer
```

---

## 📊 Build Progress

You'll see these messages during build:

**Stage 1: Setup**
```
[INFO] Check application requirements
[INFO] Ensure build layout
```

**Stage 2: SDK Download**
```
[INFO] Downloading Android SDK...
Downloading https://dl.google.com/android/...
```

**Stage 3: NDK Download**
```
[INFO] Downloading Android NDK...
Downloading https://dl.google.com/android/repository/...
```

**Stage 4: Compile**
```
[INFO] -> running python3 -m pythonforandroid.toolchain...
[INFO] Building for Android
```

**Stage 5: Package**
```
[INFO] Packaging for Android...
[INFO] APK facerecognition-1.0-armeabi-v7a-debug.apk available
```

---

## ✅ Success!

When you see this, you're done:
```
# Android packaging done!
# APK facerecognition-1.0-armeabi-v7a-debug.apk available in the bin directory
```

---

## 🔄 Rebuild After Changes

To rebuild after editing code:

```bash
cd ~/face_recognition_build

# Copy updated files
cp -r "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"/* .

# Clean (optional, for major changes)
rm -rf .buildozer

# Rebuild (much faster now - 2-5 min!)
~/.local/bin/buildozer android debug

# Copy to Windows
cp bin/*.apk /mnt/d/FaceRecognitionApp.apk
```

---

## 📝 Quick Reference

```bash
# Open Ubuntu
wsl -d Ubuntu-22.04

# Navigate
cd ~/face_recognition_build

# Build
~/.local/bin/buildozer -v android debug

# Copy to Windows
cp bin/*.apk /mnt/d/FaceRecognitionApp.apk

# Exit Ubuntu
exit
```

---

**Follow these steps and you WILL get your APK!** 🚀
