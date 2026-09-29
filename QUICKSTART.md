# Quick Start Guide

Get your Face Recognition Camera System running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install packages
pip install opencv-python face-recognition numpy Pillow
```

**Note**: If `face-recognition` fails, you may need to install CMake and Visual Studio Build Tools first. See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

## Step 2: Test Your Camera (30 seconds)

```powershell
python main.py --test-camera
```

Press 'Q' to close the test window when you see your camera feed.

## Step 3: Register Your First Person (1 minute)

```powershell
python register_face.py
```

1. Enter the person's name when prompted
2. Position your face in the camera view
3. Press **SPACE** to capture (5 samples needed)
4. Press **Q** when done

## Step 4: Start Face Recognition (30 seconds)

```powershell
python main.py
```

Your face should now be recognized with your name and ID displayed!

## Controls While Running

| Key | Action |
|-----|--------|
| `Q` | Quit the application |
| `R` | Reload database (after registering new people) |
| `S` | Save screenshot |
| `D` | Toggle debug mode |

## Common First-Time Issues

### "No module named cv2"
```powershell
pip install opencv-python
```

### "No module named face_recognition"
```powershell
pip install face-recognition
```
If this fails, see [INSTALLATION.md](INSTALLATION.md) for platform-specific instructions.

### "Failed to open camera"
- Check that no other application is using the camera
- Try changing camera source in `config/config.json`:
  ```json
  "source": 1  // Try 0, 1, or 2
  ```

### "No face detected"
- Ensure good lighting
- Face the camera directly
- Move closer to the camera
- Remove glasses or masks if possible

## What's Next?

### Register More People
```powershell
python register_face.py --name "Another Person"
```

### View Registered People
```powershell
python main.py --show-database
```

### Check System Stats
```powershell
python main.py --stats
```

### Adjust Recognition Settings

Edit `config/config.json`:

```json
{
  "recognition": {
    "tolerance": 0.5,  // Lower = stricter (0.4-0.6 recommended)
    "model": "hog"     // "hog" (fast) or "cnn" (accurate)
  }
}
```

## Tips for Best Results

1. **Lighting**: Use good, even lighting
2. **Positioning**: Face camera directly, fill 30-50% of frame
3. **Samples**: Register 5-10 different angles/expressions
4. **Background**: Use plain backgrounds when registering
5. **Distance**: Stand 2-4 feet from camera

## Performance Optimization

If the system is slow:

1. **Reduce resolution** in `config/config.json`:
   ```json
   "camera": {
     "width": 320,
     "height": 240
   }
   ```

2. **Increase frame skip**:
   ```json
   "recognition": {
     "frame_skip": 3  // Process every 3rd frame
   }
   ```

3. **Use HOG model** (faster):
   ```json
   "recognition": {
     "model": "hog"
   }
   ```

## Architecture Overview

```
Face Recognition System
├── Camera Handler    → Captures video frames
├── Face Encoder      → Detects and encodes faces
├── Database Manager  → Stores person data & face encodings
└── Recognition System → Matches faces and displays results
```

## Example Workflow

```
1. Camera captures frame
2. System detects faces in frame
3. Generates 128-D encoding for each face
4. Compares with database encodings
5. Finds best match (if any)
6. Displays name + ID on recognized faces
7. Marks unknown faces for registration
```

## Need More Help?

- **Full documentation**: See [README.md](README.md)
- **Installation issues**: See [INSTALLATION.md](INSTALLATION.md)
- **Configuration**: Check `config/config.json`
- **Database management**: Use `manage_database.py`

## Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Camera working (tested with --test-camera)
- [ ] At least one person registered
- [ ] Face recognition running
- [ ] Recognition working correctly

Congratulations! Your Face Recognition Camera System is now operational! 🎉
