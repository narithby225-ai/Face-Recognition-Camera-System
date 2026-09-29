# 🚀 HOW TO RUN THE PROJECT

## ✅ Status: All packages are installed and ready!

I've verified that all required packages are installed:
- ✅ OpenCV (version 5.0.0)
- ✅ NumPy (version 2.5.3)
- ✅ Pillow (version 12.3.0)
- ✅ face-recognition (version 1.3.0)
- ✅ dlib (version 20.0.1)

---

## 🎯 Option 1: Simple Face Detection (Works Immediately!)

This uses only OpenCV for basic face detection:

```powershell
.\venv\Scripts\python.exe simple_face_detection.py
```

**What it does:**
- Opens your camera
- Detects faces in real-time
- Shows bounding boxes around faces
- No registration needed - just works!

**Controls:**
- Press `Q` to quit

---

## 🎯 Option 2: Full Face Recognition System

### Step 1: Register Yourself

```powershell
.\venv\Scripts\python.exe register_face.py
```

**What to do:**
1. Enter your name when prompted
2. Position your face in the camera view
3. Press `SPACE` bar 5 times to capture samples
4. Press `Q` when done

The system will assign you a unique ID automatically!

### Step 2: Start Face Recognition

```powershell
.\venv\Scripts\python.exe main.py
```

**What happens:**
- Camera opens
- Your face is recognized with your name and ID
- Unknown faces are marked in red

**Controls:**
- `Q` - Quit
- `R` - Reload database
- `S` - Save screenshot
- `D` - Toggle debug mode

---

## 🗄️ Database Management

### View Who's Registered

```powershell
.\venv\Scripts\python.exe main.py --show-database
```

### View Statistics

```powershell
.\venv\Scripts\python.exe main.py --stats
```

### Manage Database

```powershell
.\venv\Scripts\python.exe manage_database.py --list
```

---

## 🎥 Test Your Camera First

```powershell
.\venv\Scripts\python.exe main.py --test-camera
```

If camera doesn't work:
1. Close other apps using camera (Zoom, Teams, etc.)
2. Edit `config/config.json` and try different camera source: 0, 1, or 2
3. Check Windows camera permissions

---

## 📋 Quick Command Reference

```powershell
# Simple detection (no registration needed)
.\venv\Scripts\python.exe simple_face_detection.py

# Register person
.\venv\Scripts\python.exe register_face.py

# Start recognition
.\venv\Scripts\python.exe main.py

# Test camera
.\venv\Scripts\python.exe main.py --test-camera

# View database
.\venv\Scripts\python.exe main.py --show-database

# Database management
.\venv\Scripts\python.exe manage_database.py --list
```

---

## 🔧 Troubleshooting

### Camera won't open
- Make sure no other app is using the camera
- Try: `.\venv\Scripts\python.exe simple_face_detection.py`
- Edit `config/config.json`, change `"source": 0` to `"source": 1` or `"source": 2`

### "face_recognition_models" error
If you see this error, the full face recognition might not work yet.
Use the simple detection instead:
```powershell
.\venv\Scripts\python.exe simple_face_detection.py
```

### Window appears then closes immediately
This is normal for camera apps - they need to stay running.
The window will show your camera feed.
Press `Q` to close it properly.

---

## 🎉 Recommended First Run

**Start with the simple version:**

```powershell
.\venv\Scripts\python.exe simple_face_detection.py
```

This will:
1. Open your camera
2. Show real-time face detection
3. No setup needed!

Press `Q` when you want to quit.

---

## 💡 Tips

1. **Lighting**: Make sure you have good lighting
2. **Distance**: Sit 2-3 feet from camera
3. **Face forward**: Look at the camera directly
4. **No mask/glasses**: For best detection, remove if possible

---

## 🆘 Still Having Issues?

Run this diagnostic:

```powershell
.\venv\Scripts\python.exe -c "import cv2; print('OpenCV:', cv2.__version__); cap = cv2.VideoCapture(0); print('Camera:', cap.isOpened()); cap.release()"
```

This will tell you if your camera is accessible.

---

## 📞 Next Steps

1. Try simple detection first: `.\venv\Scripts\python.exe simple_face_detection.py`
2. If that works, try registration: `.\venv\Scripts\python.exe register_face.py`
3. Then run full system: `.\venv\Scripts\python.exe main.py`

**Have fun with your Face Recognition System!** 🎉
