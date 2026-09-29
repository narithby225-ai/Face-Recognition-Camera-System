"""
Simple Face Detection Demo
Uses only OpenCV (no face recognition yet)
This will detect faces and assign temporary IDs
"""

import cv2
import sys
import json
import os

def load_config():
    """Load configuration"""
    try:
        with open('config/config.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'camera': {'source': 0, 'width': 640, 'height': 480},
            'display': {'box_color': [0, 255, 0]}
        }

def main():
    print("\n" + "="*60)
    print("🎥 SIMPLE FACE DETECTION DEMO")
    print("="*60)
    print("This demo uses OpenCV for face detection")
    print("Press 'Q' to quit")
    print("="*60 + "\n")
    
    config = load_config()
    
    # Initialize camera with DirectShow backend (Windows)
    cap = cv2.VideoCapture(config['camera']['source'], cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        print("\nTroubleshooting:")
        print("1. Make sure no other application is using the camera")
        print("2. Try changing camera source in config/config.json (0, 1, or 2)")
        print("3. Check camera permissions in Windows Settings")
        return
    
    print("✓ Camera opened successfully!\n")
    
    # Load OpenCV's pre-trained face detector
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    
    if face_cascade.empty():
        print("❌ Error: Could not load face detector!")
        return
    
    print("✓ Face detector loaded!\n")
    print("Starting detection...\n")
    
    face_id_counter = 1
    tracked_faces = {}
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Failed to read frame")
            break
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw rectangles around faces
        for i, (x, y, w, h) in enumerate(faces):
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Add label
            label = f"Face #{i+1}"
            cv2.putText(frame, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Add info text
        info_text = f"Faces Detected: {len(faces)}"
        cv2.putText(frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.putText(frame, "Press 'Q' to quit", (10, frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display frame
        cv2.imshow('Simple Face Detection', frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nExiting...")
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("✓ Camera released")
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
