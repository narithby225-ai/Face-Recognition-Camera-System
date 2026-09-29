# 🚀 Build Android APK on Windows - Step by Step

## ✅ Prerequisites Check

You have:
- ✅ Windows 10/11
- ✅ WSL2 installed
- ✅ Ubuntu-22.04 running

Perfect! Let's build your APK.

---

## 📱 Method 1: Automated Build (Easiest)

### Step 1: Open Ubuntu Terminal

```powershell
# In PowerShell, open Ubuntu
wsl -d Ubuntu-22.04
```

### Step 2: Navigate to Project

```bash
# In Ubuntu terminal
cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"
```

### Step 3: Make Script Executable

```bash
chmod +x build_apk.sh
```

### Step 4: Run Build Script

```bash
./build_apk.sh
```

**This will:**
- ✅ Install all dependencies automatically
- ✅ Setup build environment
- ✅ Download Android SDK/NDK (~5GB)
- ✅ Build your APK

**Time:** 20-30 minutes first time, 2-5 minutes subsequent builds

---

## 📱 Method 2: Manual Build (Step by Step)

If you prefer to do it manually:

### Step 1: Open WSL Ubuntu

```powershell
wsl -d Ubuntu-22.04
```

### Step 2: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 3: Install Python & Build Tools

```bash
# Python and basics
sudo apt install -y python3 python3-pip git zip unzip

# Build tools
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Additional libraries
sudo apt install -y cmake libopenblas-dev liblapack-dev
sudo apt install -y autoconf automake libtool pkg-config
sudo apt install -y zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5
```

### Step 4: Install Java

```bash
# Install OpenJDK 17
sudo apt install -y openjdk-17-jdk

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc

# Verify
java -version
```

### Step 5: Install Cython & Buildozer

```bash
# Upgrade pip
pip3 install --upgrade pip

# Install Cython (specific version for compatibility)
pip3 install --user cython==0.29.36

# Install Buildozer
pip3 install --user buildozer==1.5.0

# Add to PATH
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc

# Reload bash
source ~/.bashrc

# Verify
buildozer --version
```

### Step 6: Navigate to Mobile App

```bash
cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"
```

### Step 7: Build APK

```bash
# First time: Initialize (creates .buildozer folder)
buildozer init

# Build debug APK
buildozer android debug
```

**What happens:**
1. Downloads Android SDK (~3GB)
2. Downloads Android NDK (~2GB)
3. Downloads Python-for-Android
4. Compiles your app
5. Creates APK in `bin/` folder

**Total time:** 20-30 minutes first time

---

## 📦 After Build Completes

### Find Your APK

```bash
# In Ubuntu terminal
ls -lh bin/

# You'll see something like:
# facerecognition-1.0-armeabi-v7a-debug.apk
```

### Copy to Windows

```bash
# Copy to Windows D: drive
cp bin/*.apk /mnt/d/face_recognition_app.apk
```

Now you can find it at: `D:\face_recognition_app.apk`

### Install on Phone

**Option 1: USB Transfer**
1. Connect phone to PC with USB
2. Copy APK to phone
3. Tap APK on phone to install
4. Enable "Install from Unknown Sources" if prompted

**Option 2: ADB Install (if phone connected)**
```bash
# Install ADB tools first
sudo apt install -y android-tools-adb

# Install APK
adb install bin/*.apk
```

**Option 3: Google Drive/Email**
1. Upload APK to Google Drive or email it
2. Download on phone
3. Install

---

## ⚡ Quick Reference

### Build Commands

```bash
# Navigate to project
cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"

# Clean build (if needed)
buildozer android clean

# Build debug APK
buildozer android debug

# Build release APK (for production)
buildozer android release
```

### Check Build Status

```bash
# Watch build progress
tail -f .buildozer/android/platform/build-*/build.log

# Check for errors
grep -i error .buildozer/android/platform/build-*/build.log
```

---

## 🐛 Common Issues & Fixes

### Issue 1: "buildozer: command not found"

```bash
# Add to PATH
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Issue 2: "JAVA_HOME not set"

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

### Issue 3: "Out of space"

```bash
# Check free space (need at least 10GB)
df -h

# Clean old builds
buildozer android clean

# Clean apt cache
sudo apt clean
```

### Issue 4: Build fails with "SDK not found"

```bash
# Remove and rebuild
rm -rf .buildozer
buildozer android debug
```

### Issue 5: "Permission denied"

```bash
# Make sure you're in the right directory
pwd

# Should show: /mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app
```

---

## 📊 Build Progress Guide

You'll see these stages:

1. **[INFO]** - Information messages (normal)
2. **Downloading Android SDK** - ~3GB download (first time)
3. **Downloading Android NDK** - ~2GB download (first time)
4. **Downloading Python-for-Android** - Build tools
5. **Compiling dependencies** - face_recognition, opencv, etc.
6. **Building APK** - Final assembly
7. **APK created** - Success! 🎉

**Be patient!** First build takes 20-30 minutes.

---

## ✅ Success Indicators

When build succeeds, you'll see:

```
# APK has been finalized
# APK facerecognition-1.0-armeabi-v7a-debug.apk available in the bin directory
```

Your APK is ready! 🎉

---

## 📱 APK Details

**File:** `bin/facerecognition-1.0-armeabi-v7a-debug.apk`  
**Size:** ~150-200 MB  
**Type:** Debug APK  
**Target:** Android 5.0+ (API 21+)  
**Architecture:** ARMv7a (most Android phones)

---

## 🔄 Rebuild After Changes

When you update your code:

```bash
# Navigate to mobile_app
cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"

# Clean (optional, for major changes)
buildozer android clean

# Rebuild
buildozer android debug
```

Subsequent builds are **much faster** (2-5 minutes) because SDK/NDK are already downloaded!

---

## 🎯 Next Steps After Building

1. ✅ Copy APK to phone
2. ✅ Install and test
3. ✅ Grant camera permissions
4. ✅ Test face recognition
5. ✅ Share with team!

---

## 💡 Pro Tips

- **First build:** Plan for 30 minutes, grab coffee ☕
- **Clean builds:** Only when necessary (very slow)
- **Keep terminal open:** Don't close during build
- **Check logs:** If fails, check last few lines for errors
- **Test on phone:** Desktop testing doesn't show all issues

---

## 📞 Need Help?

Check build logs:
```bash
cat .buildozer/android/platform/build-*/build.log | tail -n 50
```

Common error patterns:
- "No module named" → Dependency issue
- "SDK not found" → Remove .buildozer folder
- "Permission denied" → Check file permissions
- "Out of memory" → Free up disk space

---

**Ready to build? Run the automated script or follow manual steps!** 🚀
