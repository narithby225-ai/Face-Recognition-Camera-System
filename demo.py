"""
Demo Script for Face Recognition System
Demonstrates system capabilities with sample data.
"""

import json
import os
import sys
import time
import cv2
import numpy as np

from src.face_encoder import FaceEncoder
from src.database_manager import DatabaseManager


def create_sample_face_image(name: str, output_path: str):
    """
    Create a sample face image with text overlay.
    This is for demo purposes only - real faces work much better!
    """
    # Create blank image
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw simple face
    center = (200, 200)
    
    # Face circle
    cv2.circle(img, center, 120, (200, 200, 200), -1)
    cv2.circle(img, center, 120, (100, 100, 100), 2)
    
    # Eyes
    cv2.circle(img, (160, 180), 15, (50, 50, 50), -1)
    cv2.circle(img, (240, 180), 15, (50, 50, 50), -1)
    
    # Smile
    cv2.ellipse(img, (200, 220), (50, 30), 0, 0, 180, (50, 50, 50), 2)
    
    # Add name
    cv2.putText(img, name, (120, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Save
    cv2.imwrite(output_path, img)
    return img


def demo_face_detection():
    """Demonstrate face detection capabilities."""
    print("\n" + "="*60)
    print("🔍 DEMO 1: FACE DETECTION")
    print("="*60)
    
    encoder = FaceEncoder(model="hog")
    
    # Create sample image
    sample_img = create_sample_face_image("Demo Face", "demo_sample.jpg")
    
    print("\nDetecting faces in sample image...")
    
    # Note: This simple demo image won't detect real faces
    # Real photos work much better!
    face_locations = encoder.detect_faces(sample_img)
    
    print(f"Number of faces detected: {len(face_locations)}")
    
    if face_locations:
        for i, location in enumerate(face_locations):
            top, right, bottom, left = location
            print(f"  Face {i+1}: top={top}, right={right}, bottom={bottom}, left={left}")
    else:
        print("  Note: Simple demo images don't have real facial features.")
        print("  Use actual photos for real face detection!")
    
    # Clean up
    if os.path.exists("demo_sample.jpg"):
        os.remove("demo_sample.jpg")


def demo_database_operations():
    """Demonstrate database operations."""
    print("\n" + "="*60)
    print("🗄️  DEMO 2: DATABASE OPERATIONS")
    print("="*60)
    
    # Use temporary test database
    test_db_path = "data/database/demo_test.db"
    
    # Remove if exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db_manager = DatabaseManager(test_db_path)
    
    print("\n1. Creating demo face encodings...")
    # Create dummy encodings (128-dimensional vectors)
    encoding1 = np.random.rand(128)
    encoding2 = np.random.rand(128)
    encoding3 = np.random.rand(128)
    
    print("\n2. Registering demo persons...")
    id1 = db_manager.register_person("Alice Demo", [encoding1, encoding2], notes="Demo person 1")
    id2 = db_manager.register_person("Bob Demo", [encoding3], notes="Demo person 2")
    
    print(f"\n3. Retrieving persons from database...")
    persons = db_manager.get_all_persons()
    print(f"   Total persons: {len(persons)}")
    
    for person in persons:
        print(f"   - ID: {person['id']}, Name: {person['name']}")
    
    print(f"\n4. Getting encodings...")
    encodings, person_ids, names = db_manager.get_all_encodings()
    print(f"   Total encodings: {len(encodings)}")
    print(f"   Encodings per person: {len(encodings) / len(persons):.1f}")
    
    print(f"\n5. Updating last seen for {persons[0]['name']}...")
    db_manager.update_last_seen(persons[0]['id'])
    updated_person = db_manager.get_person_by_id(persons[0]['id'])
    print(f"   Last seen: {updated_person['last_seen']}")
    
    print(f"\n6. Deleting demo person...")
    db_manager.delete_person(id1)
    remaining = db_manager.get_person_count()
    print(f"   Remaining persons: {remaining}")
    
    # Clean up
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    print("\n✓ Database demo complete!")


def demo_face_comparison():
    """Demonstrate face comparison and matching."""
    print("\n" + "="*60)
    print("🔍 DEMO 3: FACE COMPARISON")
    print("="*60)
    
    encoder = FaceEncoder()
    
    print("\n1. Creating test face encodings...")
    # Simulate face encodings
    face_a = np.random.rand(128)
    face_b = face_a + np.random.rand(128) * 0.1  # Similar to face_a
    face_c = np.random.rand(128)  # Different face
    
    known_encodings = [face_a]
    
    print("\n2. Comparing similar face...")
    matches, distances = encoder.compare_faces(known_encodings, face_b, tolerance=0.6)
    print(f"   Match: {matches[0]}, Distance: {distances[0]:.4f}")
    
    print("\n3. Comparing different face...")
    matches, distances = encoder.compare_faces(known_encodings, face_c, tolerance=0.6)
    print(f"   Match: {matches[0]}, Distance: {distances[0]:.4f}")
    
    print("\n4. Finding best match...")
    test_encodings = [face_a, face_b, face_c]
    best_idx, best_distance = encoder.find_best_match(test_encodings, face_a, tolerance=0.6)
    
    if best_idx is not None:
        print(f"   Best match index: {best_idx}, Distance: {best_distance:.4f}")
    else:
        print("   No match found")
    
    print("\n✓ Face comparison demo complete!")


def demo_configuration():
    """Demonstrate configuration loading and customization."""
    print("\n" + "="*60)
    print("⚙️  DEMO 4: CONFIGURATION")
    print("="*60)
    
    config_path = "config/config.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("\nCurrent Configuration:")
        print(f"  Camera Resolution: {config['camera']['width']}x{config['camera']['height']}")
        print(f"  Detection Model: {config['recognition']['model']}")
        print(f"  Recognition Tolerance: {config['recognition']['tolerance']}")
        print(f"  Frame Skip: {config['recognition']['frame_skip']}")
        print(f"  Show Confidence: {config['display']['show_confidence']}")
        print(f"  Show ID: {config['display']['show_id']}")
        
        print("\n💡 Tips for customization:")
        print("  - Lower tolerance (0.4-0.5) = stricter matching")
        print("  - Higher tolerance (0.6-0.7) = more lenient matching")
        print("  - HOG model = faster but less accurate")
        print("  - CNN model = slower but more accurate")
        print("  - Higher frame_skip = better performance")
    else:
        print("\n❌ Configuration file not found!")


def demo_system_info():
    """Display system information and requirements."""
    print("\n" + "="*60)
    print("ℹ️  DEMO 5: SYSTEM INFORMATION")
    print("="*60)
    
    print("\n📦 Checking installed packages...")
    
    packages = {
        'cv2': 'OpenCV',
        'face_recognition': 'Face Recognition',
        'numpy': 'NumPy',
        'PIL': 'Pillow'
    }
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name}: Installed")
        except ImportError:
            print(f"  ❌ {name}: Not installed")
    
    print("\n🎥 Checking camera availability...")
    from src.camera_handler import CameraHandler
    available_cameras = CameraHandler.list_available_cameras()
    
    if available_cameras:
        print(f"  ✓ Found {len(available_cameras)} camera(s): {available_cameras}")
    else:
        print("  ⚠️  No cameras detected")
    
    print("\n📂 Checking directory structure...")
    required_dirs = [
        'data/database',
        'data/encodings',
        'data/registered_faces',
        'data/logs',
        'config',
        'src'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ❌ {directory} (missing)")


def run_all_demos():
    """Run all demo functions."""
    print("\n" + "="*70)
    print(" "*15 + "🎯 FACE RECOGNITION SYSTEM DEMO")
    print("="*70)
    print("\nThis demo will showcase the system's capabilities")
    print("without requiring actual face images or camera access.\n")
    
    input("Press ENTER to start the demos...")
    
    try:
        demo_face_detection()
        time.sleep(1)
        
        demo_database_operations()
        time.sleep(1)
        
        demo_face_comparison()
        time.sleep(1)
        
        demo_configuration()
        time.sleep(1)
        
        demo_system_info()
        
        print("\n" + "="*70)
        print("✅ ALL DEMOS COMPLETED!")
        print("="*70)
        print("\n📚 Next Steps:")
        print("  1. Read QUICKSTART.md for setup instructions")
        print("  2. Run: python register_face.py")
        print("  3. Run: python main.py")
        print("  4. Enjoy your face recognition system!\n")
    
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main demo entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Face Recognition System Demo')
    parser.add_argument('--demo', type=int, choices=[1,2,3,4,5], 
                       help='Run specific demo (1-5)')
    
    args = parser.parse_args()
    
    if args.demo == 1:
        demo_face_detection()
    elif args.demo == 2:
        demo_database_operations()
    elif args.demo == 3:
        demo_face_comparison()
    elif args.demo == 4:
        demo_configuration()
    elif args.demo == 5:
        demo_system_info()
    else:
        run_all_demos()


if __name__ == "__main__":
    main()
