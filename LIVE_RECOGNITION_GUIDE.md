# 👋 Live Face Recognition with Welcome Greeting

## Overview

Real-time security/greeting system that:
- Detects faces instantly from camera
- Recognizes people and displays **"Welcome [Your Name]"**
- Shows confidence scores
- Tracks when people were last seen
- Optional attendance marking via API

---

## Features

### 🎯 **Instant Recognition**
- Real-time face detection
- Immediate greeting display
- 3-second cooldown between recognitions
- Welcome message shown for 5 seconds

### 🎨 **Visual Display**
- **Green box** around known people
- **Red box** around unknown people
- Large "Welcome [Name]!" overlay
- Confidence percentage shown
- FPS counter
- Active greetings counter

### ⚡ **Performance**
- DirectShow backend (Windows optimized)
- Frame skipping for smooth performance
- 15-30 FPS on most computers
- Low CPU usage

### 🔐 **Security Features**
- Unknown person detection
- Recognition confidence scores
- Activity logging to console
- Optional API integration for attendance

---

## Quick Start

### Step 1: Ensure Faces Are Registered

You need faces in the database first. Choose one method:

#### **Method A: Use existing dataset folder**
Your photos should already be in `dataset/` folder with format:
```
001_DUC20240002_កាំង_ប៊ុនឆៃ.jpg
002_DUC20240025_ក្វាវ_មេសា.jpg
...
```

#### **Method B: Register via camera**
```bash
.\venv\Scripts\python.exe register_face.py
```

#### **Method C: Use current database**
If you already have faces in `data/database/faces.db`, they'll load automatically.

### Step 2: Run the System

**Option 1: Double-click batch file**
```
run_live_recognition.bat
```

**Option 2: Command line**
```bash
.\venv\Scripts\python.exe live_recognition_system.py
```

### Step 3: Watch the Magic!

When someone appears:
1. **Face detected** → Green/red box appears
2. **Person recognized** → Large "Welcome [Name]!" displays
3. **Console shows** → "👋 Welcome [Name]! (Confidence: 95%)"
4. **Message fades** → After 5 seconds

---

## Controls

| Key | Action |
|-----|--------|
| **Q** | Quit application |
| **S** | Save screenshot |
| **D** | Toggle debug mode |
| **R** | Reload known faces |

---

## How It Works

### Recognition Process

```
1. Camera captures frame
   ↓
2. Detect faces (every 2nd frame for speed)
   ↓
3. Generate 128-D face encoding
   ↓
4. Compare with known faces
   ↓
5. Find best match (if distance < tolerance)
   ↓
6. Display "Welcome [Name]!" for 5 seconds
   ↓
7. Log to console
   ↓
8. Optional: Mark attendance via API
```

### Smart Features

**Cooldown System**
- Same person won't trigger welcome again for 3 seconds
- Prevents spam when person stays in frame

**Fade Effect**
- Welcome message fades out smoothly
- Multiple people can have greetings simultaneously

**Performance Optimization**
- Processes every 2nd frame (configurable)
- Smaller frame for face detection (4x smaller)
- Full resolution for display

---

## Configuration

Edit `config/config.json`:

### Recognition Accuracy
```json
{
  "recognition": {
    "tolerance": 0.6,     // Lower = stricter (0.4-0.7)
    "model": "hog",       // hog (fast) or cnn (accurate)
    "frame_skip": 2       // Process every Nth frame
  }
}
```

**Tolerance Guide:**
- `0.4-0.5` = Very strict (few false positives)
- `0.6` = Balanced (recommended)
- `0.7+` = Lenient (more false positives)

### Camera Settings
```json
{
  "camera": {
    "source": 0,          // Camera index (0, 1, 2...)
    "width": 640,
    "height": 480
  }
}
```

### In Code Settings

Edit `live_recognition_system.py`:

```python
# Line 26: Cooldown between recognitions
self.recognition_cooldown = 3.0  # seconds

# Line 29: Welcome message duration
self.welcome_duration = 5.0      # seconds

# Line 18: Frame skip for performance
self.frame_skip = 2              # process every 2nd frame
```

---

## Use Cases

### 🏠 **Home Security**
- Know who enters your property
- Alert on unknown faces
- Log entry times

### 🏢 **Office Reception**
- Greet employees automatically
- Track office hours
- Visitor identification

### 🏫 **School Attendance**
- Automatic attendance marking
- Welcome students by name
- Track late arrivals

### 🏪 **Retail Store**
- Recognize VIP customers
- Personalized greetings
- Customer traffic analysis

---

## Integration with Backend API

### Enable API Integration

In `live_recognition_system.py`, set:

```python
# Line 44-45
self.api_url = "http://localhost:8000"
self.api_enabled = True  # Change to True
```

### What It Does

When enabled, system will:
1. Detect and recognize face
2. Display welcome message
3. **Automatically call API** to mark attendance
4. Store in database

### API Call

```python
POST http://localhost:8000/api/v1/attendance/mark
{
    "student_id": 1,
    "date": "2024-09-27",
    "status": "present",
    "confidence": 0.95
}
```

---

## Troubleshooting

### No Faces Detected

**Problem:** Camera opens but no boxes appear

**Solutions:**
1. Check lighting (need good light)
2. Face camera directly
3. Move closer (2-3 feet)
4. Try different `model`:
   ```json
   "model": "cnn"  // More accurate but slower
   ```

### Wrong Person Recognition

**Problem:** System confuses people

**Solutions:**
1. Lower tolerance:
   ```json
   "tolerance": 0.5  // Stricter matching
   ```
2. Register more photos per person
3. Use better quality photos
4. Ensure good lighting during registration

### Performance Issues

**Problem:** Laggy or low FPS

**Solutions:**
1. Increase frame skip:
   ```json
   "frame_skip": 3  // Process every 3rd frame
   ```
2. Use HOG model (faster):
   ```json
   "model": "hog"
   ```
3. Reduce camera resolution:
   ```json
   "width": 320,
   "height": 240
   ```

### Camera Won't Start

**Problem:** "Failed to open camera"

**Solutions:**
1. Close other apps using camera
2. Try different camera index:
   ```json
   "source": 1  // or 2, 3...
   ```
3. Check camera permissions (Windows Settings)
4. Run `python main.py --test-camera`

---

## Advanced Features

### Multiple Simultaneous Greetings

System can greet multiple people at once:
```
Welcome Alice!
Welcome Bob!
Welcome Charlie!
```

Each greeting:
- Shows for 5 seconds
- Has fade-out effect
- Positioned vertically

### Console Logging

Real-time activity log:
```
👋 Welcome កាំង ប៊ុនឆៃ! (Confidence: 0.97)
👋 Welcome ក្វាវ មេសា! (Confidence: 0.95)
👋 Welcome គង់ បារាំង! (Confidence: 0.93)
```

### Screenshot Capture

Press **S** to save:
- Filename: `screenshots/welcome_20240927_143052.jpg`
- Includes welcome messages
- Includes face boxes
- Full resolution

---

## Comparison with Other Modes

### Simple Detection (`simple_face_detection.py`)
- Just draws boxes
- No recognition
- No names
- Fast and simple

### Registration (`register_face.py`)
- Captures faces
- Adds to database
- One person at a time

### Main Recognition (`main.py`)
- Full system
- Database tracking
- Multiple features

### **Live Welcome (This System)** ⭐
- Real-time greeting
- Instant feedback
- Security focus
- User-friendly

---

## Performance Benchmarks

### Typical Performance

| Hardware | FPS | Recognition Speed |
|----------|-----|-------------------|
| Intel i5 + Webcam | 20-25 | <100ms |
| Intel i7 + Webcam | 25-30 | <50ms |
| Laptop with integrated | 15-20 | <150ms |

### With Settings

| Configuration | FPS | Accuracy |
|---------------|-----|----------|
| HOG + skip=2 | 25-30 | Good |
| HOG + skip=3 | 30-35 | Good |
| CNN + skip=2 | 10-15 | Excellent |
| CNN + skip=3 | 15-20 | Excellent |

---

## Tips for Best Results

### During Registration
1. ✅ Good, even lighting
2. ✅ Face camera directly
3. ✅ Neutral expression
4. ✅ Multiple angles (5+ photos)
5. ✅ Close to camera (fill frame)

### During Recognition
1. ✅ Same lighting conditions
2. ✅ Clean camera lens
3. ✅ Stable camera position
4. ✅ 2-4 feet from camera
5. ✅ Avoid backlighting

### System Setup
1. ✅ Mount camera at eye level
2. ✅ Point at entry/doorway
3. ✅ Ensure good lighting
4. ✅ Test with all users
5. ✅ Adjust tolerance as needed

---

## Next Steps

### Enhance the System

1. **Add Audio**
   ```python
   # Text-to-speech greeting
   import pyttsx3
   engine = pyttsx3.init()
   engine.say(f"Welcome {name}")
   engine.runAndWait()
   ```

2. **Add Notifications**
   - Email alerts for unknown faces
   - SMS notifications
   - Push notifications

3. **Add Logging**
   - Save all recognitions to file
   - Daily activity reports
   - Statistics dashboard

4. **Connect to Backend**
   - Full API integration
   - Web dashboard
   - Mobile app access

---

## Safety & Privacy

### Data Privacy
- Face encodings stored locally
- No cloud processing
- No data sent externally (unless API enabled)

### Security
- Unknown face alerts
- Activity logging
- Optional authentication

### Compliance
- Inform users about face recognition
- Get consent where required
- Follow local privacy laws

---

## Summary

**What You Have:**
✅ Real-time face recognition
✅ Instant welcome greetings
✅ Unknown person detection
✅ Performance optimized
✅ Easy to use
✅ Customizable

**Perfect For:**
- Home security
- Office reception
- Attendance systems
- Customer greeting
- Access control

---

**Enjoy your personalized welcome system!** 👋😊

For questions or issues, check:
- Console output for errors
- Camera permissions
- Face registration quality
- Configuration settings
