# Face Recognition System - Commands Cheatsheet

Quick reference for all available commands and keyboard shortcuts.

## 🚀 Installation

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Main Application Commands

### Start Face Recognition
```powershell
python main.py
```

### Test Camera
```powershell
python main.py --test-camera
```

### Show Registered Database
```powershell
python main.py --show-database
```

### Show System Statistics
```powershell
python main.py --stats
```

### Use Custom Config File
```powershell
python main.py --config path/to/config.json
```

## 👤 Registration Commands

### Interactive Registration
```powershell
python register_face.py
```

### Register with Name
```powershell
python register_face.py --name "John Doe"
```

### Register from Image File
```powershell
python register_face.py --name "Jane Smith" --image photo.jpg
```

### Use Custom Config
```powershell
python register_face.py --name "Bob" --config custom_config.json
```

## 🗄️ Database Management Commands

### Interactive Menu
```powershell
python manage_database.py
```

### List All Persons
```powershell
python manage_database.py --list
```

### View Person Details
```powershell
python manage_database.py --view 1  # View person with ID 1
```

### Search by Name
```powershell
python manage_database.py --search "John"
```

### Delete Person
```powershell
python manage_database.py --delete 1  # Delete person with ID 1
```

### Delete Person (Skip Confirmation)
```powershell
python manage_database.py --delete 1 --force
```

### Export Database to JSON
```powershell
python manage_database.py --export persons.json
```

### Show Database Statistics
```powershell
python manage_database.py --stats
```

### Create Database Backup
```powershell
python manage_database.py --backup

# Or specify backup file
python manage_database.py --backup backup.db
```

## 🧪 Demo Commands

### Run All Demos
```powershell
python demo.py
```

### Run Specific Demo
```powershell
python demo.py --demo 1  # Face detection demo
python demo.py --demo 2  # Database operations demo
python demo.py --demo 3  # Face comparison demo
python demo.py --demo 4  # Configuration demo
python demo.py --demo 5  # System information demo
```

## ⌨️ Keyboard Controls (During Recognition)

| Key | Action |
|-----|--------|
| `Q` | Quit application |
| `R` | Reload database from disk |
| `S` | Save screenshot of current frame |
| `D` | Toggle debug mode (show additional info) |

## ⌨️ Keyboard Controls (During Registration)

| Key | Action |
|-----|--------|
| `SPACE` | Capture face sample |
| `Q` | Quit/cancel registration |

## 📁 Directory Structure Quick Reference

```
data/
├── database/          # SQLite database files (*.db)
├── encodings/         # Cached face encodings (*.pkl)
├── registered_faces/  # Images of registered persons
├── logs/             # System logs
├── screenshots/      # Screenshots from main app (S key)
└── snapshots/        # Camera snapshots
```

## 🔧 Configuration File Locations

```
config/config.json     # Main configuration file
```

### Key Configuration Settings

```json
{
  "camera": {
    "source": 0,        // Change camera: 0, 1, 2, etc.
    "width": 640,       // Reduce for better performance
    "height": 480
  },
  "recognition": {
    "tolerance": 0.6,   // Lower = stricter (0.4-0.7)
    "model": "hog",     // "hog" (fast) or "cnn" (accurate)
    "frame_skip": 2     // Higher = better performance
  }
}
```

## 🐍 Python Package Installation

### Individual Packages
```powershell
pip install opencv-python
pip install face-recognition
pip install numpy
pip install Pillow
```

### From Requirements File
```powershell
pip install -r requirements.txt
```

### Check Installed Packages
```powershell
pip list
pip show opencv-python
pip show face-recognition
```

## 🔍 Troubleshooting Commands

### Check Python Version
```powershell
python --version  # Should be 3.8+
```

### Check Camera Availability
```powershell
python main.py --test-camera
```

### Verify Installation
```powershell
python demo.py --demo 5  # System information
```

### List Available Cameras
```python
# In Python console
from src.camera_handler import CameraHandler
print(CameraHandler.list_available_cameras())
```

## 📊 Quick Status Checks

### How Many People Registered?
```powershell
python main.py --stats
# OR
python manage_database.py --stats
```

### Who's in the Database?
```powershell
python main.py --show-database
# OR
python manage_database.py --list
```

### Database File Location
```
data/database/faces.db
```

## 🧹 Maintenance Commands

### Create Database Backup
```powershell
python manage_database.py --backup
```

### Export All Data
```powershell
python manage_database.py --export all_persons.json
```

### Clean Cache (Manual)
```powershell
# Windows
Remove-Item data\encodings\*.pkl

# Linux/Mac
rm data/encodings/*.pkl
```

## 🎨 Customization Quick Tips

### Change Recognition Strictness
Edit `config/config.json`:
```json
"tolerance": 0.5  // Stricter
"tolerance": 0.7  // More lenient
```

### Improve Performance
Edit `config/config.json`:
```json
"camera": {"width": 320, "height": 240},
"recognition": {"frame_skip": 3, "model": "hog"}
```

### Improve Accuracy
Edit `config/config.json`:
```json
"recognition": {
  "model": "cnn",
  "num_jitters": 5,
  "tolerance": 0.5
}
```

## 📦 Package Management

### Update All Packages
```powershell
pip install --upgrade -r requirements.txt
```

### Freeze Current Versions
```powershell
pip freeze > requirements_frozen.txt
```

### Create Portable Environment
```powershell
pip install pipreqs
pipreqs . --force
```

## 🚀 Quick Workflows

### Complete First-Time Setup
```powershell
# 1. Create environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install packages
pip install -r requirements.txt

# 3. Test camera
python main.py --test-camera

# 4. Register yourself
python register_face.py

# 5. Start recognition
python main.py
```

### Daily Usage
```powershell
# Activate environment
.\venv\Scripts\activate

# Register new person
python register_face.py --name "New Person"

# Start recognition
python main.py

# Check who's registered
python manage_database.py --list
```

### Database Cleanup
```powershell
# Backup first
python manage_database.py --backup

# View all persons
python manage_database.py --list

# Delete specific person
python manage_database.py --delete 5

# Verify
python manage_database.py --list
```

## 💡 Pro Tips

### 1. Multiple Camera Testing
```powershell
# Try different camera indices
python main.py --test-camera
# Edit config.json "source": 0, 1, or 2
```

### 2. Batch Registration
```powershell
# Register multiple people from images
python register_face.py --name "Person1" --image img1.jpg
python register_face.py --name "Person2" --image img2.jpg
python register_face.py --name "Person3" --image img3.jpg
```

### 3. Performance Monitoring
```powershell
# Enable debug mode: Press 'D' during recognition
# Shows: FPS, registered faces count, tolerance value
```

### 4. Quick Database Reset
```powershell
# Backup current database
python manage_database.py --backup

# Delete database file
Remove-Item data\database\faces.db

# Start fresh - new database will be created automatically
python register_face.py
```

## 📖 Documentation Quick Links

- **Getting Started**: See `QUICKSTART.md`
- **Installation Help**: See `INSTALLATION.md`
- **Full Documentation**: See `README.md`
- **Project Overview**: See `PROJECT_OVERVIEW.md`
- **This Cheatsheet**: `COMMANDS_CHEATSHEET.md`

## 🆘 Emergency Commands

### System Not Working?
```powershell
# 1. Run diagnostics
python demo.py --demo 5

# 2. Test camera
python main.py --test-camera

# 3. Check database
python manage_database.py --stats

# 4. Reinstall packages
pip install --force-reinstall -r requirements.txt
```

### Database Corrupted?
```powershell
# Restore from backup
Copy-Item data\backups\faces_backup_*.db data\database\faces.db
```

### Camera Issues?
```powershell
# List cameras
python -c "from src.camera_handler import CameraHandler; print(CameraHandler.list_available_cameras())"

# Try different source in config.json
```

---

**Last Updated**: September 2026  
**Keep this file handy for quick reference!**
