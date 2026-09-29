"""
Camera Test Script
Tests different camera backends and indices
"""

import cv2

print("="*60)
print("🎥 CAMERA DIAGNOSTIC TEST")
print("="*60)
print()

# Test different backends
backends = [
    ('Default', cv2.CAP_ANY),
    ('DirectShow (Windows)', cv2.CAP_DSHOW),
    ('Media Foundation', cv2.CAP_MSMF),
]

working_cameras = []

print("Testing camera backends and indices...\n")

for backend_name, backend_flag in backends:
    print(f"Testing {backend_name}:")
    for i in range(3):
        try:
            cap = cv2.VideoCapture(i, backend_flag)
            is_open = cap.isOpened()
            
            if is_open:
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"  ✓ Camera {i}: Working! (Frame: {frame.shape})")
                    working_cameras.append((i, backend_flag, backend_name))
                else:
                    print(f"  ⚠ Camera {i}: Opens but can't read frame")
            else:
                print(f"  ✗ Camera {i}: Not accessible")
            
            cap.release()
        except Exception as e:
            print(f"  ✗ Camera {i}: Error - {e}")
    print()

# Summary
print("="*60)
if working_cameras:
    print("✅ WORKING CAMERAS FOUND:")
    print("="*60)
    for idx, backend, name in working_cameras:
        print(f"  Camera {idx} with {name}")
    print()
    print("Recommended configuration:")
    best = working_cameras[0]
    print(f"  Index: {best[0]}")
    print(f"  Backend: {best[2]}")
else:
    print("❌ NO WORKING CAMERAS FOUND")
    print("="*60)
    print("\nTroubleshooting:")
    print("1. Check if camera is plugged in")
    print("2. Close other apps using camera (Zoom, Teams, etc.)")
    print("3. Check Windows Settings > Privacy > Camera")
    print("4. Try a different camera or USB port")

print("="*60)
