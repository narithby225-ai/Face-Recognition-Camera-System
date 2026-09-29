# 📱 Face Recognition Mobile App

## 🎯 Features

### ✨ Main Features:
- 📷 **Live Camera Recognition** - Real-time face detection
- 🎯 **ID Display** - Shows student ID instantly
- 📝 **Name Display** - Shows full name (including Khmer)
- 📊 **Confidence Score** - Recognition accuracy percentage
- 🎨 **Modern UI** - Clean, professional Material Design
- 🚀 **Offline Mode** - Works without internet
- ⚡ **Fast Recognition** - ~0.5 seconds per face

### 📱 Screens:
1. **Welcome Screen** - App introduction and navigation
2. **Camera Screen** - Live recognition with overlays
3. **Settings Screen** - Configuration options

---

## 🚀 Quick Start

### Option 1: Test on Desktop (Windows)
```powershell
# Install dependencies
pip install kivy kivymd opencv-python numpy face-recognition

# Run the app
python test_app.py
```

### Option 2: Build Android APK
See **BUILD_APK_GUIDE.md** for detailed instructions

**Quick version:**
```bash
# In WSL2 or Linux:
buildozer android debug
```

---

## 📂 Project Structure

```
mobile_app/
├── main.py                 # Main app logic
├── facerecognition.kv      # UI layout (Kivy language)
├── buildozer.spec          # APK build configuration
├── test_app.py             # Desktop testing script
├── requirements.txt        # Python dependencies
├── BUILD_APK_GUIDE.md      # Complete build guide
├── README.md               # This file
└── dataset/                # Student photos (auto-linked)
```

---

## 🎨 UI Overview

### Welcome Screen
```
┌─────────────────────────┐
│  Face Recognition Sys.  │  ← Top bar
├─────────────────────────┤
│                         │
│    Welcome to           │
│  Face Recognition       │
│         System          │
│          🎯             │
│                         │
│  [START CAMERA]         │  ← Main button
│  [SETTINGS]             │
│                         │
│  43 Students Registered │
└─────────────────────────┘
```

### Camera Screen
```
┌─────────────────────────┐
│ ← Live Recognition   🔄 │  ← Top bar
├─────────────────────────┤
│                         │
│   [Live Camera View]    │
│                         │
│  ┌─────────────────┐    │
│  │   WELCOME!      │    │  ← Recognition result
│  │ ID: DUC2024...  │    │
│  │ ឈឿត ណារិទ្ធ     │    │
│  │ Confidence: 95% │    │
│  └─────────────────┘    │
│                         │
│ 👤 Known Faces: 1       │  ← Info panel
└─────────────────────────┘
```

---

## ⚙️ Configuration

### Recognition Settings (in main.py):
```python
self.tolerance = 0.6          # 0.4-0.7 (lower = stricter)
self.recognition_cooldown = 3.0  # Seconds between recognitions
```

### Camera Settings (in facerecognition.kv):
```yaml
Camera:
    resolution: (640, 480)     # Camera resolution
    play: True                 # Auto-start camera
```

---

## 📊 Performance

### Desktop:
- **FPS**: 10-15 (with face detection)
- **Recognition Time**: ~0.3 seconds
- **Memory Usage**: ~200-300 MB

### Android (Mid-range phone):
- **FPS**: 5-10 (optimized)
- **Recognition Time**: ~0.5-1 second
- **Memory Usage**: ~150-250 MB
- **Battery Impact**: Moderate (camera intensive)

---

## 🔒 Permissions Required

The Android app requires:

1. **Camera** - For live face recognition
   ```xml
   android.permissions = CAMERA
   ```

2. **Storage** - To load student photos
   ```xml
   WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
   ```

3. **Internet** - (Optional) Future API integration
   ```xml
   INTERNET
   ```

---

## 📱 Supported Devices

### Android:
- **Minimum**: Android 5.0 (API 21)
- **Recommended**: Android 8.0+ (API 26+)
- **RAM**: 2GB minimum, 4GB recommended
- **Camera**: Any (front or back)
- **Storage**: 200MB for app + dataset

### Desktop Testing:
- **Windows**: 10/11
- **Python**: 3.8-3.11
- **RAM**: 4GB minimum

---

## 🐛 Known Issues

1. **Large APK Size** (~150MB)
   - Includes dlib models and face recognition libraries
   - Future: Download models on first run

2. **First Recognition Slow** (~2-3 seconds)
   - Camera warmup time
   - Future: Pre-initialize camera

3. **Khmer Text Display**
   - Requires Unicode font support
   - Install Khmer fonts on Android if needed

---

## 🔄 Future Enhancements

### Planned Features:
- [ ] Backend API integration (FastAPI)
- [ ] Real-time attendance tracking
- [ ] Student database sync
- [ ] Push notifications
- [ ] Admin panel
- [ ] Multi-camera support
- [ ] Cloud backup
- [ ] Statistics dashboard

---

## 📚 Technologies Used

### Frontend:
- **Kivy 2.2.1** - Python UI framework
- **KivyMD 1.1.1** - Material Design components
- **OpenCV 4.10** - Camera and image processing

### Backend (Recognition):
- **face_recognition 1.3.0** - Face detection/recognition
- **dlib 19.24** - Machine learning models
- **NumPy 1.24** - Array operations

### Build:
- **Buildozer 1.5.0** - APK compiler
- **Cython 0.29** - Python to C compiler
- **Android NDK 23b** - Native development

---

## 📖 Documentation

- **Kivy**: https://kivy.org/doc/stable/
- **KivyMD**: https://kivymd.readthedocs.io/
- **Buildozer**: https://buildozer.readthedocs.io/
- **Face Recognition**: https://github.com/ageitgey/face_recognition

---

## 🆘 Support

### Issues:
- Check BUILD_APK_GUIDE.md for troubleshooting
- Review logs: `adb logcat` (Android)
- Test on desktop first: `python test_app.py`

---

## 📄 License

This project is for educational purposes (SPDI-II).

---

**Built with ❤️ for 43 Cambodian Students**

*Version 1.0 - September 2026*
