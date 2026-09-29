# 🎯 Face Recognition Camera System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10-green.svg)](https://opencv.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com/)
[![Kivy](https://img.shields.io/badge/Kivy-2.2-purple.svg)](https://kivy.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Android-lightgrey.svg)]()

A complete, production-ready face recognition system with **real-time ID and name display** for security, attendance, and reception applications. Built for **43 Cambodian students** with full **Khmer language support**.

---

## ✨ Features

### 🖥️ Desktop System
- 📷 **Live Camera Recognition** - Real-time face detection and identification
- 🎯 **ID Display** - Instant student/employee ID display (e.g., DUC20240147)
- 📝 **Name Display** - Full name with Khmer support (e.g., ឈឿត ណារិទ្ធ)
- 📊 **Confidence Score** - Recognition accuracy percentage
- ⚡ **Fast Processing** - ~0.3-0.5 seconds per face
- 🎨 **Professional UI** - Large welcome overlays with fade effects
- 🔄 **Auto Cooldown** - 3-second delay between recognitions
- 💾 **Offline Mode** - Works without internet

### 📱 Mobile App (Android)
- 📲 **Native Android App** - Built with Kivy/Python
- 🎯 **Same Features** - ID and Name display on mobile
- 💾 **Offline Mode** - Works without internet
- 🎨 **Material Design** - Modern, professional UI
- 📦 **Single APK** - Easy deployment (~150 MB)
- 🔒 **Camera Permissions** - Built-in permission handling

### 🔧 Backend API (FastAPI)
- 🚀 **28+ REST Endpoints** - Complete API for integration
- 🔐 **JWT Authentication** - Secure access control with bcrypt
- 👥 **Student Management** - Full CRUD operations
- 📊 **Attendance Tracking** - Mark, report, and analyze attendance
- 🎯 **Recognition API** - Detect, identify, and verify faces
- 🌐 **WebSocket Support** - Real-time event streaming
- 🐳 **Docker Ready** - Complete docker-compose setup
- 📝 **Auto Documentation** - Swagger/OpenAPI UI

---

## 🚀 Quick Start

### 1. Desktop Live Recognition (Easiest)

```powershell
# Install dependencies
pip install -r requirements.txt

# Run live recognition
python live_recognition_system.py
```

**What you'll see:**
- Live camera feed
- Green boxes around recognized faces
- Large "WELCOME!" overlay with ID and Name
- Confidence percentage

### 2. Test Mobile App on Desktop

```powershell
cd mobile_app
pip install kivy kivymd
python test_app.py
```

### 3. Build Android APK

See [`mobile_app/BUILD_APK_GUIDE.md`](mobile_app/BUILD_APK_GUIDE.md) for complete instructions.

**Quick version:**
```bash
# In WSL2 or Linux
cd mobile_app
pip3 install buildozer
buildozer android debug
```

---

## 📂 Project Structure

```
Face-Recognition-Camera-System/
├── 🖥️ Desktop System
│   ├── live_recognition_system.py      # Main live recognition app
│   ├── register_from_dataset.py        # Bulk face registration
│   ├── prepare_dataset.py              # Dataset preparation tool
│   ├── test_camera.py                  # Camera diagnostic
│   └── run_*.bat                       # Quick launchers
│
├── 📱 Mobile App
│   ├── main.py                         # Mobile app main logic
│   ├── facerecognition.kv              # UI layout (Kivy)
│   ├── buildozer.spec                  # APK build config
│   ├── test_app.py                     # Desktop testing
│   ├── BUILD_APK_GUIDE.md              # Build instructions
│   └── dataset/                        # Student photos
│
├── 🔧 Backend API
│   └── backend/
│       ├── app/
│       │   ├── api/
│       │   │   ├── auth.py             # Authentication endpoints
│       │   │   ├── students.py         # Student CRUD
│       │   │   ├── recognition.py      # Face recognition API
│       │   │   ├── attendance.py       # Attendance tracking
│       │   │   └── camera.py           # Camera management
│       │   ├── models/                 # SQLAlchemy models
│       │   ├── schemas/                # Pydantic schemas
│       │   └── main.py                 # FastAPI app
│       ├── Dockerfile
│       └── docker-compose.yml
│
├── 📊 Data & Config
│   ├── dataset/                        # Student photos
│   │   └── 008_DUC20240147_Name.jpg   # Format: ID_Code_Name.jpg
│   ├── students_list.csv               # 43 students data
│   ├── config/
│   │   └── config.json                 # System configuration
│   └── data/
│       ├── database/                   # SQLite storage
│       ├── encodings/                  # Face encodings cache
│       └── registered_faces/           # Registered face images
│
└── 📖 Documentation
    ├── README.md                       # This file
    ├── MOBILE_APP_QUICKSTART.md        # Mobile quick start
    ├── ARCHITECTURE.md                 # System architecture
    ├── INSTALLATION.md                 # Setup guide
    ├── PROJECT_OVERVIEW.md             # Feature overview
    └── KHMER_GUIDE.md                  # Khmer language support
```

---

## 🎓 For 43 Students

This system is pre-configured for **43 Cambodian students** with:
- ✅ Full student database (`students_list.csv`)
- ✅ Khmer name support (Unicode)
- ✅ ID format: DUC20240002, DUC20240003, etc.
- ✅ Photo naming: `001_DUC20240002_កាំង_ប៊ុនឆៃ.jpg`

**Students included:**
- DUC20240002 - កាំង ប៊ុនឆៃ
- DUC20240003 - ខុន វុទ្ធី
- DUC20240147 - ឈឿត ណារិទ្ធ
- ... (all 43 students)

---

## 📋 Prerequisites

### Desktop System:
- **Python**: 3.8 - 3.11 (3.14.3 tested)
- **OS**: Windows 10/11, Linux, macOS
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: Any USB/built-in webcam

### Mobile App:
- **Android**: 5.0+ (API 21+)
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 200MB for app
- **Camera**: Front or back camera

### Backend API:
- **Python**: 3.8+
- **PostgreSQL**: 12+ (or SQLite for dev)
- **Redis**: 6+ (optional)
- **Docker**: 20+ (optional)

---

## 📦 Installation

### Method 1: Quick Install (Recommended)

```powershell
# Clone repository
git clone https://github.com/narithby225-ai/Face-Recognition-Camera-System.git
cd Face-Recognition-Camera-System

# Install Python dependencies
pip install -r requirements.txt

# Run live recognition
python live_recognition_system.py
```

### Method 2: Virtual Environment (Best Practice)

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 3: Docker (Backend Only)

```bash
cd backend
docker-compose up -d
```

**Backend runs at:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

---

## 🎯 Usage

### Desktop Live Recognition

```powershell
# Simple: Just double-click
run_live_recognition.bat

# Or run manually
python live_recognition_system.py
```

**Controls:**
- **Q** - Quit
- **S** - Save screenshot
- **D** - Toggle debug mode
- **R** - Reload known faces

### Register New Faces

**From photos:**
```powershell
# Prepare dataset photos
python prepare_dataset.py

# Register all faces from dataset/
python register_from_dataset.py
```

**From camera:**
```powershell
python register_face.py
```

### Backend API

```powershell
cd backend
uvicorn app.main:socket_app --reload
```

**Try the API:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Example endpoints:**
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/students/` - List students
- `POST /api/v1/recognition/identify` - Identify face
- `POST /api/v1/attendance/mark` - Mark attendance

### Mobile App

See [`MOBILE_APP_QUICKSTART.md`](MOBILE_APP_QUICKSTART.md)

---

## ⚙️ Configuration

### Recognition Settings

Edit `config/config.json`:

```json
{
  "recognition": {
    "tolerance": 0.6,        // 0.4-0.7 (lower = stricter)
    "model": "hog",           // "hog" or "cnn"
    "num_jitters": 1,         // More = better accuracy, slower
    "frame_skip": 2           // Process every Nth frame
  },
  "camera": {
    "source": 0,              // Camera index
    "width": 640,
    "height": 480,
    "fps": 30
  }
}
```

### Database

**Development (SQLite):**
```python
DATABASE_URL = "sqlite:///./data/database/faces.db"
```

**Production (PostgreSQL):**
```python
DATABASE_URL = "postgresql://user:pass@localhost:5432/facerecog"
```

---

## 📊 Technical Stack

### Core Technologies:
- **Face Recognition**: face_recognition + dlib
- **Computer Vision**: OpenCV 4.10
- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Database**: PostgreSQL / SQLite
- **Mobile**: Kivy + KivyMD
- **Authentication**: JWT + bcrypt
- **Deployment**: Docker + docker-compose

### Key Libraries:
- `face_recognition` - Face detection and recognition
- `dlib` - Machine learning models
- `opencv-python` - Camera and image processing
- `numpy` - Array operations
- `fastapi` - REST API framework
- `sqlalchemy` - Database ORM
- `kivy` - Mobile UI framework

---

## 📱 Mobile App Screenshots

### Welcome Screen
```
┌─────────────────────────┐
│  Face Recognition Sys.  │
├─────────────────────────┤
│                         │
│    Welcome to           │
│  Face Recognition       │
│       System            │
│         🎯              │
│                         │
│  [START CAMERA]         │
│  [SETTINGS]             │
│                         │
│  43 Students Registered │
└─────────────────────────┘
```

### Camera Screen (Recognition Active)
```
┌─────────────────────────┐
│ ← Live Recognition   🔄 │
├─────────────────────────┤
│                         │
│  [Live Camera View]     │
│                         │
│  ┌─────────────────┐    │
│  │   WELCOME!      │    │
│  │ ID: DUC2024...  │    │
│  │ ឈឿត ណារិទ្ធ     │    │
│  │ Confidence: 95% │    │
│  └─────────────────┘    │
│                         │
│ 👤 Known Faces: 43      │
└─────────────────────────┘
```

---

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - Logout

### Students
- `GET /api/v1/students/` - List all students
- `POST /api/v1/students/` - Create student
- `GET /api/v1/students/{id}` - Get student
- `PUT /api/v1/students/{id}` - Update student
- `DELETE /api/v1/students/{id}` - Delete student

### Recognition
- `POST /api/v1/recognition/detect` - Detect faces
- `POST /api/v1/recognition/identify` - Identify person
- `POST /api/v1/recognition/verify` - Verify identity
- `GET /api/v1/recognition/encodings/{student_id}` - Get encodings

### Attendance
- `POST /api/v1/attendance/mark` - Mark attendance
- `GET /api/v1/attendance/today` - Today's attendance
- `GET /api/v1/attendance/stats` - Statistics
- `GET /api/v1/attendance/report` - Generate report

---

## 🐛 Troubleshooting

### Camera Issues

**"Camera not found"**
```powershell
# Test camera
python test_camera.py
```

**"Black screen"**
- Use DirectShow backend: `cv2.VideoCapture(0, cv2.CAP_DSHOW)`
- Close other apps using camera
- Restart computer

### Recognition Issues

**"No face detected"**
- Ensure good lighting
- Face directly towards camera
- Distance: 0.5-2 meters

**"Wrong person identified"**
- Lower tolerance: `"tolerance": 0.5`
- Use CNN model: `"model": "cnn"`
- Add more photos of the person

### Build Issues

**"Buildozer not found"**
```bash
pip3 install --upgrade buildozer
```

**"Android SDK not found"**
- First build downloads SDK automatically
- Takes 20-30 minutes
- Requires 5GB free space

---

## 📖 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Complete installation guide
- **[MOBILE_APP_QUICKSTART.md](MOBILE_APP_QUICKSTART.md)** - Mobile app guide
- **[mobile_app/BUILD_APK_GUIDE.md](mobile_app/BUILD_APK_GUIDE.md)** - APK build instructions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Feature overview
- **[KHMER_GUIDE.md](KHMER_GUIDE.md)** - Khmer language support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Face Recognition Library** by Adam Geitgey
- **dlib** by Davis King
- **OpenCV** team
- **FastAPI** by Sebastián Ramírez
- **Kivy** team

---

## 📞 Contact

**Project by:** narithby225-ai  
**GitHub:** https://github.com/narithby225-ai/Face-Recognition-Camera-System  
**Built for:** SPDI-II - 43 Cambodian Students

---

## 🎉 Success Stories

This system is ready for:
- ✅ **School Attendance** - Automatic student check-in
- ✅ **Security Checkpoints** - Access control
- ✅ **Reception Desks** - Visitor identification
- ✅ **Event Registration** - Quick attendee verification
- ✅ **Office Access** - Employee recognition

---

**Built with ❤️ for SPDI-II Students**

*Version 1.0 - September 2026*
