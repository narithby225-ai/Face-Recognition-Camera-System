# 🚀 START BUILDING YOUR APK - Simple Instructions

## ⚠️ IMPORTANT: You're in PowerShell, not Ubuntu!

The APK **must be built in Ubuntu/WSL2** (Linux), not Windows PowerShell.

---

## ✅ CORRECT WAY - Choose One:

### 🎯 **Method 1: Use the Automated Launcher (Easiest!)**

**Just double-click this file in Windows Explorer:**
```
BUILD_APK_START.bat
```

**OR run it in PowerShell:**
```powershell
.\BUILD_APK_START.bat
```

This will:
1. Open Ubuntu automatically
2. Run the build script
3. Build your APK

---

### 🎯 **Method 2: Open Ubuntu Manually**

**Step 1:** Open Ubuntu WSL2
```powershell
wsl -d Ubuntu-22.04
```

**Step 2:** You're now in Ubuntu! Run these commands:
```bash
# Navigate to project
cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"

# Make script executable
chmod +x build_apk.sh

# Run build
./build_apk.sh
```

---

## ❌ What Went Wrong?

You were running **Ubuntu commands** in **Windows PowerShell** - they don't work there!

### Ubuntu/Linux Commands (won't work in PowerShell):
- ❌ `cp bin/*.apk /mnt/d/` - Linux copy command
- ❌ `sudo apt install` - Linux package manager
- ❌ `rm -rf` - Linux remove command
- ❌ `./build_apk.sh` - Linux script execution

### These ONLY work inside Ubuntu (WSL2)!

---

## 🎯 Let's Start Correctly Now!

### Option A: Quick Start (Recommended)

**In PowerShell, run:**
```powershell
.\BUILD_APK_START.bat
```

**Or just double-click:** `BUILD_APK_START.bat` in File Explorer

---

### Option B: Manual Start

**Step 1:** Open Ubuntu
```powershell
# In PowerShell, type:
wsl -d Ubuntu-22.04
```

**Step 2:** Navigate and build (now you're in Ubuntu!)
```bash
cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app"
chmod +x build_apk.sh
./build_apk.sh
```

---

## 📊 What You'll See

### In PowerShell (when using .bat file):
```
========================================
  Face Recognition APK Builder
========================================

This will:
 1. Open Ubuntu in WSL2
 2. Navigate to mobile_app folder
 3. Start automated APK build

Opening Ubuntu WSL2...
```

### Then Ubuntu Opens and Shows:
```
========================================
  Face Recognition APK Builder
========================================

Step 1: Updating system packages...
Step 2: Installing Python and build tools...
Step 3: Installing Java Development Kit...
Step 4: Installing Cython and Buildozer...
Step 5: Verifying installation...
Step 6: Building APK...
```

---

## ⏱️ Timeline

**First Build:**
- Setup: 5 minutes
- Download SDK: 10 minutes
- Download NDK: 5 minutes
- Compile: 10 minutes
- Package: 2 minutes
- **Total: 20-30 minutes**

**Subsequent Builds:**
- **Total: 2-5 minutes** (SDK already downloaded)

---

## 📦 After Build Completes

### Your APK will be at:
```
mobile_app/bin/facerecognition-1.0-armeabi-v7a-debug.apk
```

### To copy to Windows (in Ubuntu terminal):
```bash
cp bin/*.apk /mnt/d/face_recognition.apk
```

### To find it in Windows:
```
D:\face_recognition.apk
```

---

## 🎯 READY? Let's Go!

### Choose your method:

**1. EASIEST (Recommended):**
- Double-click `BUILD_APK_START.bat` in File Explorer
- OR in PowerShell: `.\BUILD_APK_START.bat`

**2. MANUAL:**
- PowerShell: `wsl -d Ubuntu-22.04`
- Then in Ubuntu: `cd "/mnt/d/Lessons_and_Codes/SPDI-II/Face Recognition Camera System/mobile_app" && ./build_apk.sh`

---

## ✅ Success Indicators

**Build started successfully when you see:**
```
========================================
  Face Recognition APK Builder
========================================
Step 1: Updating system packages...
```

**Build completed successfully when you see:**
```
✅ APK BUILD COMPLETE!
Your APK is located at:
  /mnt/d/.../mobile_app/bin/facerecognition-1.0-armeabi-v7a-debug.apk
```

---

## 🐛 Troubleshooting

### "wsl command not found"
- WSL2 not installed properly
- Try: `wsl --install`

### "Ubuntu-22.04 not found"
- Try: `wsl -l` to see available distributions
- Use whatever Ubuntu version you have

### Build fails
- Check internet connection
- Check disk space (need 10GB free)
- Try the manual method

---

## 💡 Remember

- 🔴 **PowerShell** = Windows commands
- 🟢 **Ubuntu/WSL2** = Linux commands
- 📱 **APK build** = Must use Ubuntu!

---

**Ready to build? Run this now:**

```powershell
.\BUILD_APK_START.bat
```

**Or double-click the file in File Explorer!** 🚀
