# How to Install Python on Windows

## Method 1: From Python.org (Recommended)

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11 or 3.12 (latest stable version)
   - Choose "Windows installer (64-bit)"

2. **Install Python**
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check ✅ "Add Python to PATH" at the bottom!
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**
   - Open a NEW PowerShell window
   - Run: `python --version`
   - Should show: Python 3.11.x or 3.12.x

4. **Verify pip**
   - Run: `pip --version`
   - Should show pip version

## Method 2: From Microsoft Store (Easier but sometimes limited)

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Get" or "Install"
4. Wait for installation
5. Open NEW PowerShell and test: `python --version`

## After Installing Python

Once Python is installed, come back and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install packages
pip install opencv-python face-recognition numpy Pillow
```

## Troubleshooting

### "python: command not found" after installation
- Close ALL PowerShell windows
- Open a NEW PowerShell window
- Try again

### "Activate.ps1 cannot be loaded" error
Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Still not working?
1. Restart your computer
2. Open NEW PowerShell
3. Try: `py --version` (alternative command)
4. If that works, use `py` instead of `python` everywhere

## Quick Test After Installation

```powershell
python --version
pip --version
```

Both should work without errors!
