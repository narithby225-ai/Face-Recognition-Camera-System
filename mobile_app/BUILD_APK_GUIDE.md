# 📱 Build Face Recognition Android APK

## 🎯 Overview
This guide helps you build an Android APK from the Face Recognition System.

---

## 📋 Prerequisites

### Windows (Your Current System):
You need Linux to build APK with Buildozer. Options:
1. **WSL2 (Windows Subsystem for Linux)** - Recommended
2. **Virtual Machine** (Ubuntu/Linux Mint)
3. **Cloud Build Service** (GitHub Actions, CircleCI)

---

## 🚀 Method 1: Build Using WSL2 (Recommended)

### Step 1: Install WSL2
```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu-22.04
```

### Step 2: Enter WSL2
```powershell
wsl
```

### Step 3: Install Dependencies in WSL2
```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and build tools
sudo apt install -y python3 python3-pip git zip unzip openjdk-17-jdk
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y cmake libopenblas-dev liblapack-dev

# Install Android SDK dependencies
sudo apt install -y autoconf automake libtool pkg-config
sudo apt install -y zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5

# Install Cython and Buildozer
pip3 install --upgrade pip
pip3 install cython==0.29.36
pip3 install buildozer==1.5.0
```

### Step 4: Copy Project to WSL2
```bash
# In WSL2, navigate to your home directory
cd ~

# Copy files from Windows (adjust path as needed)
cp -r /mnt/d/Lessons_and_Codes/SPDI-II/Face\ Recognition\ Camera\ System/mobile_app ~/face_recognition_app
cd ~/face_recognition_app

# Copy dataset folder
cp -r /mnt/d/Lessons_and_Codes/SPDI-II/Face\ Recognition\ Camera\ System/dataset ./
```

### Step 5: Build APK
```bash
# Initialize buildozer (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Or build release APK (for production)
buildozer android release
```

### Step 6: Get Your APK
```bash
# APK will be in bin/ folder
ls -la bin/

# Copy APK to Windows
cp bin/*.apk /mnt/d/face_recognition.apk
```

---

## 🚀 Method 2: Online Build Service (Easiest)

### Use GitHub Actions (Free)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Mobile app ready"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

2. **Create GitHub Actions Workflow**:
Create `.github/workflows/build-apk.yml`:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython
        sudo apt-get update
        sudo apt-get install -y openjdk-17-jdk autoconf automake libtool
    
    - name: Build APK
      run: |
        cd mobile_app
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: face-recognition-app
        path: mobile_app/bin/*.apk
```

3. **Download APK** from GitHub Actions artifacts

---

## 🚀 Method 3: Use Docker (Cross-Platform)

```bash
# Pull buildozer Docker image
docker pull kivy/buildozer

# Run build in Docker
docker run --rm -v "$(pwd)/mobile_app:/app" kivy/buildozer android debug

# APK will be in mobile_app/bin/
```

---

## 📦 What Gets Built

Your APK will include:
- ✅ Face Recognition Engine
- ✅ Live Camera Feed
- ✅ ID & Name Display
- ✅ Welcome Screen
- ✅ Settings Panel
- ✅ All 43 Student Faces (from dataset/)

**APK Size**: ~100-150 MB (includes ML models)

---

## 🎯 Installation on Android

```bash
# Transfer APK to phone via:
# 1. USB Cable
# 2. Google Drive
# 3. Email
# 4. ADB

# Install via ADB (if phone connected):
adb install face_recognition.apk

# Or just click APK on phone to install
```

---

## ⚙️ App Permissions

The app will request:
- 📷 **Camera** - For face recognition
- 📂 **Storage** - To load dataset images
- 🌐 **Internet** - (Optional) For future API integration

---

## 🐛 Troubleshooting

### Build Errors:

**"Command not found: buildozer"**
```bash
pip3 install --upgrade buildozer
```

**"Android SDK not found"**
```bash
# Buildozer will download automatically on first build
# Just wait, it takes 10-20 minutes
```

**"Out of memory"**
```bash
# Increase WSL2 memory in .wslconfig
# Windows path: C:\Users\YourName\.wslconfig
[wsl2]
memory=4GB
```

### Runtime Errors on Phone:

**"App crashes on start"**
- Check camera permissions enabled
- Ensure dataset/ folder is bundled
- Check logs: `adb logcat`

---

## 📱 Testing the App

1. **Install APK** on Android phone
2. **Open app** - You'll see Welcome screen
3. **Tap "START CAMERA"** - Camera opens
4. **Point at student photo** - See recognition!
5. **Welcome screen appears** with ID and Name

---

## 🔄 Updating the App

To update students:
1. Add new photos to `dataset/` folder
2. Rebuild APK
3. Reinstall on phone

Or: Build backend API + auto-sync (future feature)

---

## 💡 Tips

- **First build takes 20-30 minutes** (downloads SDK)
- **Subsequent builds take 2-5 minutes**
- **Use debug APK for testing**, release for production
- **Sign release APK** before publishing to Play Store

---

## 🎉 Success!

Once built, your APK is ready to:
- ✅ Install on any Android phone (Android 5.0+)
- ✅ Recognize faces in real-time
- ✅ Show ID and Name instantly
- ✅ Work offline (no internet needed)
- ✅ Use at security checkpoints, reception, attendance

---

## 🆘 Need Help?

- Buildozer docs: https://buildozer.readthedocs.io/
- Kivy docs: https://kivy.org/doc/stable/
- Face recognition: https://github.com/ageitgey/face_recognition

---

**Built with ❤️ for SPDI-II Students**
