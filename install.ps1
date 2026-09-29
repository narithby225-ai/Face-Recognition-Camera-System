# Installation Script for Face Recognition Camera System
# Run this with: .\install.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Face Recognition System - Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "1. Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = py --version 2>&1
    Write-Host "   ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python not found!" -ForegroundColor Red
    Write-Host "   Please install Python from: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "2. Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ✓ Virtual environment already exists" -ForegroundColor Green
} else {
    py -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment and install packages
Write-Host ""
Write-Host "3. Installing required packages..." -ForegroundColor Yellow
Write-Host "   This may take 3-5 minutes, please wait..." -ForegroundColor Cyan

& ".\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".\venv\Scripts\python.exe" -m pip install opencv-python face-recognition numpy Pillow --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "   ⚠ Some packages may have failed to install" -ForegroundColor Yellow
    Write-Host "   You may need to install CMake for face-recognition" -ForegroundColor Yellow
}

# Verify installation
Write-Host ""
Write-Host "4. Verifying installation..." -ForegroundColor Yellow

$modules = @("cv2", "face_recognition", "numpy", "PIL")
$allGood = $true

foreach ($module in $modules) {
    $result = & ".\venv\Scripts\python.exe" -c "import $module; print('OK')" 2>&1
    if ($result -like "*OK*") {
        Write-Host "   ✓ $module" -ForegroundColor Green
    } else {
        Write-Host "   ✗ $module" -ForegroundColor Red
        $allGood = $false
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✓ Installation Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Activate virtual environment:" -ForegroundColor White
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Register a person:" -ForegroundColor White
    Write-Host "   py register_face.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. Start face recognition:" -ForegroundColor White
    Write-Host "   py main.py" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "⚠ Installation completed with warnings" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Some packages failed to install." -ForegroundColor Yellow
    Write-Host "You may need to:" -ForegroundColor Yellow
    Write-Host "1. Install CMake: https://cmake.org/download/" -ForegroundColor White
    Write-Host "2. Install Visual Studio Build Tools" -ForegroundColor White
    Write-Host "3. Then run: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "4. And: pip install face-recognition" -ForegroundColor White
    Write-Host ""
}
