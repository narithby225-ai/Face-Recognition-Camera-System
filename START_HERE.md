# ✅ START HERE - Your System Setup

## Good News! 
Python 3.14.3 is already installed on your system!

## Important: Use `py` instead of `python`

On your system, Python is accessed via the `py` command, not `python`.

---

## 🚀 Quick Start (Follow These Exact Steps)

### Step 1: Create Virtual Environment
```powershell
py -m venv venv
```

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an error about execution policy**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

### Step 3: Install Required Packages
```powershell
pip install opencv-python face-recognition numpy Pillow
```

This will take 2-5 minutes to download and install.

### Step 4: Test Installation
```powershell
py demo.py --demo 5
```

This will check if everything is working.

---

## 📝 Commands for YOUR System

Replace all `python` commands with `py`:

### ✅ Correct Commands for Your System:

```powershell
# Test camera
py main.py --test-camera

# Register a person
py register_face.py

# Start face recognition
py main.py

# View database
py main.py --show-database

# View statistics
py main.py --stats

# Database management
py manage_database.py --list
py manage_database.py --backup

# Run demos
py demo.py
```

---

## 🎯 Complete Setup Process (Copy & Paste)

```powershell
# 1. Create virtual environment
py -m venv venv

# 2. Activate it (if error, see troubleshooting below)
.\venv\Scripts\Activate.ps1

# 3. Install packages (this takes a few minutes)
pip install opencv-python face-recognition numpy Pillow

# 4. Test installation
py demo.py --demo 5

# 5. Register yourself
py register_face.py

# 6. Start face recognition
py main.py
```

---

## ⚠️ Troubleshooting

### Error: "Activate.ps1 cannot be loaded"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "No module named 'cv2'"
Make sure virtual environment is activated (you should see `(venv)` in prompt)
```powershell
.\venv\Scripts\Activate.ps1
pip install opencv-python
```

### Error: "face_recognition" installation fails
This package needs CMake. If it fails:
1. Download CMake: https://cmake.org/download/
2. Install it
3. Restart PowerShell
4. Try again: `pip install face-recognition`

### Camera not working
```powershell
py main.py --test-camera
```
Try different camera indices in `config/config.json` (0, 1, or 2)

---

## 📋 Installation Checklist

Run each command and check it works:

```powershell
# Check Python version
py --version
# Should show: Python 3.14.3

# Check pip (after activating venv)
pip --version
# Should show pip version

# Check OpenCV
py -c "import cv2; print('OpenCV OK')"

# Check face_recognition
py -c "import face_recognition; print('face_recognition OK')"

# Check numpy
py -c "import numpy; print('NumPy OK')"
```

---

## 🎮 After Installation

Once everything is installed:

1. **Register your first person:**
   ```powershell
   py register_face.py
   ```
   - Enter your name
   - Press SPACE 5 times to capture samples
   - Press Q when done

2. **Start face recognition:**
   ```powershell
   py main.py
   ```
   - Your face will be recognized with your name and ID!
   - Press Q to quit

3. **View who's registered:**
   ```powershell
   py main.py --show-database
   ```

---

## 💡 Remember

- Always use `py` instead of `python`
- Activate virtual environment before running: `.\venv\Scripts\Activate.ps1`
- You should see `(venv)` in your prompt when activated
- To deactivate: just type `deactivate`

---

## Next Steps

1. ✅ Run the setup commands above
2. ✅ Register yourself
3. ✅ Start face recognition
4. ✅ Read `QUICKSTART.md` for more features

Good luck! 🎉
