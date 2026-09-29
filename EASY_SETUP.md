# 🚀 Easy Setup Guide - Step by Step

## ✅ Python is Already Installed!
Your system has Python 3.14.3 installed (accessed via `py` command).

---

## 📋 Setup Instructions (5 Minutes)

### **Step 1: Set Execution Policy** (One-time setup)

Copy and paste this command:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Press `Y` when asked to confirm.

---

### **Step 2: Install Packages**

The virtual environment is already created! Now activate it and install packages:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# You should now see (venv) in your prompt

# Upgrade pip
python -m pip install --upgrade pip

# Install required packages (takes 3-5 minutes)
pip install opencv-python
pip install numpy
pip install Pillow
```

**Note about face-recognition**: This package is tricky on Windows. Let's try it:

```powershell
pip install face-recognition
```

**If it fails**, you have two options:

#### **Option A: Use pre-built wheel (Easier)**
1. Download from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x/releases
2. Find the right wheel for Python 3.14 and Windows 64-bit
3. Install: `pip install path\to\downloaded\file.whl`
4. Then: `pip install face-recognition`

#### **Option B: Install build tools (More reliable)**
1. Download CMake: https://cmake.org/download/
2. Install Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
3. Restart PowerShell
4. Try: `pip install face-recognition`

---

### **Step 3: Verify Installation**

```powershell
# Check each package
python -c "import cv2; print('OpenCV: OK')"
python -c "import numpy; print('NumPy: OK')"
python -c "import PIL; print('Pillow: OK')"
python -c "import face_recognition; print('Face Recognition: OK')"
```

If all show "OK", you're ready!

---

### **Step 4: Test the System**

```powershell
# Run demo
py demo.py --demo 5

# Test camera
py main.py --test-camera
```

---

## 🎯 Quick Commands After Setup

**Always activate virtual environment first:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Then use these commands:**
```powershell
# Register a person
py register_face.py

# Start face recognition
py main.py

# View database
py manage_database.py --list
```

---

## ⚡ Alternative: Simplified Version Without face-recognition

If you can't install `face-recognition`, I can create a simpler version using only OpenCV's face detection (without the recognition part). Let me know if you want this option!

---

## 🆘 Troubleshooting

### Virtual environment activation fails
```powershell
# Run this first
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1
```

### "pip: command not found" after activation
You need to activate the virtual environment first. Look for `(venv)` in your prompt.

### face-recognition installation takes forever
It's compiling dlib from source. This can take 10-20 minutes. Be patient!

### Installation fails with "Microsoft Visual C++ required"
Install Visual Studio Build Tools:
https://visualstudio.microsoft.com/downloads/
Choose "Desktop development with C++"

---

## 📞 Need Help?

If you get stuck:
1. Show me the error message
2. Tell me which step failed
3. I'll help you fix it!

---

## 🎉 Once Everything Works

```powershell
# Register yourself
py register_face.py
# Enter your name, press SPACE 5 times to capture

# Start recognition
py main.py
# Your face will be recognized with ID!
```

**Good luck!** 🚀
