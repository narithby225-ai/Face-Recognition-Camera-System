"""
Test Installation Script
Verifies all components are working
"""

import sys

print("="*60)
print("🔍 TESTING INSTALLATION")
print("="*60)
print()

# Test 1: OpenCV
print("1. Testing OpenCV...")
try:
    import cv2
    print(f"   ✓ OpenCV version: {cv2.__version__}")
    print(f"   ✓ CascadeClassifier available: {hasattr(cv2, 'CascadeClassifier')}")
except Exception as e:
    print(f"   ✗ OpenCV Error: {e}")
    sys.exit(1)

# Test 2: NumPy
print("\n2. Testing NumPy...")
try:
    import numpy as np
    print(f"   ✓ NumPy version: {np.__version__}")
except Exception as e:
    print(f"   ✗ NumPy Error: {e}")
    sys.exit(1)

# Test 3: Pillow
print("\n3. Testing Pillow...")
try:
    import PIL
    print(f"   ✓ Pillow version: {PIL.__version__}")
except Exception as e:
    print(f"   ✗ Pillow Error: {e}")
    sys.exit(1)

# Test 4: Face Recognition (optional)
print("\n4. Testing face_recognition...")
try:
    import face_recognition
    print(f"   ✓ face_recognition installed")
except Exception as e:
    print(f"   ⚠ face_recognition Warning: {e}")
    print("   Note: Simple detection will still work!")

# Test 5: Camera
print("\n5. Testing Camera...")
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("   ✓ Camera is accessible (index 0)")
        ret, frame = cap.read()
        if ret:
            print(f"   ✓ Frame captured: {frame.shape}")
        cap.release()
    else:
        print("   ⚠ Camera not accessible at index 0")
        print("   Try changing camera source in config/config.json")
except Exception as e:
    print(f"   ✗ Camera Error: {e}")

# Test 6: Haar Cascade
print("\n6. Testing Face Detector...")
try:
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if not face_cascade.empty():
        print("   ✓ Face detector loaded successfully")
    else:
        print("   ✗ Face detector failed to load")
except Exception as e:
    print(f"   ✗ Face Detector Error: {e}")

# Test 7: Database
print("\n7. Testing Database...")
try:
    import sqlite3
    import os
    os.makedirs("data/database", exist_ok=True)
    test_db = "data/database/test.db"
    conn = sqlite3.connect(test_db)
    conn.close()
    if os.path.exists(test_db):
        os.remove(test_db)
    print("   ✓ SQLite database working")
except Exception as e:
    print(f"   ✗ Database Error: {e}")

# Summary
print("\n" + "="*60)
print("✅ INSTALLATION TEST COMPLETE!")
print("="*60)
print("\nYou can now run:")
print("  .\venv\Scripts\python.exe simple_face_detection.py")
print("\nOr double-click:")
print("  run_simple_detection.bat")
print("\n" + "="*60)
