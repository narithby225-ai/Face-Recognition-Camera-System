# Installation Guide

## Prerequisites

Before installing the Face Recognition Camera System, ensure you have:

1. **Python 3.8 or higher** installed
2. **A working webcam** (or video file for testing)
3. **Administrative/sudo privileges** (for installing system dependencies)

## Platform-Specific Installation

### Windows

#### 1. Install Python
Download and install Python from [python.org](https://www.python.org/downloads/)

#### 2. Install CMake and Visual Studio Build Tools
The `dlib` library requires compilation tools:

- Download and install **CMake**: https://cmake.org/download/
- Install **Visual Studio Build Tools**: https://visualstudio.microsoft.com/downloads/
  - Select "Desktop development with C++" workload

#### 3. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### 4. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If `dlib` installation fails, try installing pre-built wheels:
```powershell
pip install dlib-19.24.2-cp310-cp310-win_amd64.whl
```
Download wheels from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x

### Linux (Ubuntu/Debian)

#### 1. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev
sudo apt-get install -y cmake build-essential
sudo apt-get install -y libopencv-dev python3-opencv
sudo apt-get install -y libboost-all-dev
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS

#### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Dependencies
```bash
brew install cmake
brew install boost
```

#### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Verification

After installation, verify everything works:

### 1. Test Camera
```bash
python main.py --test-camera
```

### 2. Check Database
```bash
python main.py --show-database
```

### 3. View Statistics
```bash
python main.py --stats
```

## Troubleshooting

### Issue: dlib won't install

**Windows:**
- Ensure CMake is in PATH
- Install Visual Studio Build Tools with C++ support
- Try pre-built wheels from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x

**Linux:**
```bash
sudo apt-get install -y libboost-python-dev
```

**macOS:**
```bash
brew install boost-python3
```

### Issue: OpenCV camera access denied

**Windows:**
- Check Settings > Privacy > Camera
- Allow desktop apps to access camera

**Linux:**
- Add user to video group:
  ```bash
  sudo usermod -a -G video $USER
  ```
- Log out and log back in

**macOS:**
- Grant Terminal camera access in System Preferences > Security & Privacy

### Issue: face_recognition not detecting faces

1. Ensure good lighting
2. Face the camera directly
3. Move closer to camera
4. Try different detection model in `config/config.json`:
   ```json
   "model": "cnn"  // More accurate but slower
   ```

### Issue: Low FPS / Slow performance

1. Reduce camera resolution in `config/config.json`
2. Increase frame skip:
   ```json
   "frame_skip": 3
   ```
3. Use HOG model instead of CNN:
   ```json
   "model": "hog"
   ```

## Alternative: Docker Installation

If you prefer Docker, use our Docker setup:

```bash
docker build -t face-recognition-system .
docker run -it --device=/dev/video0 face-recognition-system
```

## GPU Acceleration (Optional)

For faster CNN detection, install CUDA-enabled dlib:

1. Install NVIDIA CUDA Toolkit
2. Compile dlib with CUDA support:
   ```bash
   pip install dlib --no-cache-dir --force-reinstall --install-option="--yes" --install-option="USE_AVX_INSTRUCTIONS" --install-option="--yes" --install-option="DLIB_USE_CUDA"
   ```

## Next Steps

After successful installation:

1. **Register your first person:**
   ```bash
   python register_face.py
   ```

2. **Start the face recognition system:**
   ```bash
   python main.py
   ```

3. **Read the README.md for usage instructions**

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages carefully
3. Ensure all prerequisites are met
4. Check that camera is working outside this application

## System Requirements

**Minimum:**
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Camera: 720p webcam
- Storage: 500 MB free space

**Recommended:**
- CPU: Quad-core 2.5 GHz or better
- RAM: 8 GB
- Camera: 1080p webcam
- Storage: 2 GB free space
- GPU: NVIDIA GPU with CUDA support (for CNN model)
