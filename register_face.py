"""
Face Registration Script
Register new individuals into the face recognition system.
"""

import argparse
import json
import os
import sys
import cv2
import time
from typing import List

from src.face_encoder import FaceEncoder
from src.database_manager import DatabaseManager
from src.camera_handler import CameraHandler


def load_config(config_path: str = "config/config.json") -> dict:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def register_from_camera(name: str, config: dict) -> bool:
    """
    Register person by capturing face from camera.
    
    Args:
        name: Person's name
        config: Configuration dictionary
        
    Returns:
        True if successful, False otherwise
    """
    encoder = FaceEncoder(
        model=config['recognition']['model'],
        num_jitters=config['registration'].get('num_jitters', 1)
    )
    
    camera = CameraHandler(
        source=config['camera']['source'],
        width=config['camera']['width'],
        height=config['camera']['height']
    )
    
    if not camera.start():
        print("❌ Failed to start camera!")
        return False
    
    print("\n" + "="*60)
    print("📸 FACE CAPTURE MODE")
    print("="*60)
    print("Position your face in the center of the frame")
    print(f"We'll capture {config['registration']['num_samples']} samples")
    print("Press SPACE to capture, Q to quit")
    print("="*60 + "\n")
    
    captured_encodings = []
    captured_images = []
    sample_count = 0
    target_samples = config['registration']['num_samples']
    
    # Create output directory for registered faces
    output_dir = os.path.join(config['paths']['registered_faces'], name.replace(' ', '_'))
    os.makedirs(output_dir, exist_ok=True)
    
    # Also create dataset directory for organized storage
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)
    
    try:
        while sample_count < target_samples:
            ret, frame = camera.read_frame()
            
            if not ret or frame is None:
                print("Failed to read frame")
                break
            
            # Detect faces
            face_locations = encoder.detect_faces(frame)
            
            # Draw faces
            display_frame = frame.copy()
            for location in face_locations:
                top, right, bottom, left = location
                cv2.rectangle(display_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw status
            status_text = f"Captured: {sample_count}/{target_samples}"
            cv2.putText(display_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if len(face_locations) == 0:
                cv2.putText(display_frame, "No face detected!", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            elif len(face_locations) > 1:
                cv2.putText(display_frame, "Multiple faces! Show only one.", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            else:
                cv2.putText(display_frame, "Press SPACE to capture", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow('Face Registration', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == ord('Q'):
                print("\n❌ Registration cancelled by user")
                camera.release()
                cv2.destroyAllWindows()
                return False
            
            elif key == ord(' '):  # Spacebar
                if len(face_locations) == 1:
                    # Validate face quality
                    if encoder.validate_face_quality(frame, config['registration']['min_face_size']):
                        # Encode face
                        encoding = encoder.encode_face(frame, face_locations[0])
                        
                        if encoding is not None:
                            captured_encodings.append(encoding)
                            captured_images.append(frame.copy())
                            sample_count += 1
                            
                            print(f"✓ Sample {sample_count}/{target_samples} captured")
                            
                            # Save image
                            image_path = os.path.join(output_dir, f"sample_{sample_count}.jpg")
                            cv2.imwrite(image_path, frame)
                            
                            # Brief pause
                            time.sleep(0.3)
                        else:
                            print("❌ Failed to encode face, try again")
                    else:
                        print("❌ Face quality too low, move closer or improve lighting")
                elif len(face_locations) == 0:
                    print("❌ No face detected!")
                else:
                    print("❌ Multiple faces detected! Only one person at a time.")
    
    except KeyboardInterrupt:
        print("\n❌ Registration interrupted")
        camera.release()
        cv2.destroyAllWindows()
        return False
    
    camera.release()
    cv2.destroyAllWindows()
    
    if len(captured_encodings) < target_samples:
        print(f"\n❌ Not enough samples captured ({len(captured_encodings)}/{target_samples})")
        return False
    
    # Save to database
    print("\n💾 Saving to database...")
    db_manager = DatabaseManager(config['database']['path'])
    
    # Check if person already exists
    if db_manager.person_exists(name):
        response = input(f"⚠️  Person '{name}' already exists. Add more samples? (y/n): ")
        if response.lower() != 'y':
            print("Registration cancelled")
            return False
    
    image_paths = [os.path.join(output_dir, f"sample_{i+1}.jpg") 
                   for i in range(len(captured_encodings))]
    
    person_id = db_manager.register_person(name, captured_encodings, image_paths)
    
    # Save best face image to dataset folder with format: [ID]_[Name].jpg
    if captured_images:
        # Format ID with leading zeros (e.g., 001, 002, 003)
        formatted_id = f"{person_id:03d}"
        # Clean name (replace spaces with underscores)
        clean_name = name.replace(' ', '_')
        # Create filename: 001_Narith.jpg
        dataset_filename = f"{formatted_id}_{clean_name}.jpg"
        dataset_path = os.path.join("dataset", dataset_filename)
        
        # Save the first captured image to dataset
        cv2.imwrite(dataset_path, captured_images[0])
        print(f"✓ Saved to dataset: {dataset_filename}")
    
    print("\n" + "="*60)
    print("✅ REGISTRATION SUCCESSFUL!")
    print("="*60)
    print(f"Name: {name}")
    print(f"ID: {person_id}")
    print(f"Samples: {len(captured_encodings)}")
    print(f"Images saved to: {output_dir}")
    print("="*60 + "\n")
    
    return True


def register_from_image(name: str, image_path: str, config: dict) -> bool:
    """
    Register person from image file.
    
    Args:
        name: Person's name
        image_path: Path to image file
        config: Configuration dictionary
        
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    encoder = FaceEncoder(
        model=config['recognition']['model'],
        num_jitters=config['registration'].get('num_jitters', 1)
    )
    
    print(f"\n📷 Processing image: {image_path}")
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Failed to load image")
        return False
    
    # Detect faces
    face_locations = encoder.detect_faces(image)
    
    if len(face_locations) == 0:
        print("❌ No face detected in image!")
        return False
    
    if len(face_locations) > 1:
        print(f"⚠️  Multiple faces detected ({len(face_locations)}), using the first one")
    
    # Encode face
    encoding = encoder.encode_face(image, face_locations[0])
    
    if encoding is None:
        print("❌ Failed to encode face")
        return False
    
    # Save to database
    db_manager = DatabaseManager(config['database']['path'])
    
    if db_manager.person_exists(name):
        response = input(f"⚠️  Person '{name}' already exists. Add this image? (y/n): ")
        if response.lower() != 'y':
            print("Registration cancelled")
            return False
    
    person_id = db_manager.register_person(name, [encoding], [image_path])
    
    print("\n" + "="*60)
    print("✅ REGISTRATION SUCCESSFUL!")
    print("="*60)
    print(f"Name: {name}")
    print(f"ID: {person_id}")
    print(f"Image: {image_path}")
    print("="*60 + "\n")
    
    return True


def main():
    """Main registration entry point."""
    parser = argparse.ArgumentParser(
        description='Register new person into Face Recognition System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python register_face.py                           # Interactive camera registration
  python register_face.py --name "John Doe"         # Register with camera
  python register_face.py --name "Jane" --image photo.jpg  # Register from image
        """
    )
    
    parser.add_argument(
        '--name',
        type=str,
        help='Person name to register'
    )
    
    parser.add_argument(
        '--image',
        type=str,
        help='Path to image file (optional, uses camera if not provided)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.json',
        help='Path to configuration file (default: config/config.json)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Get name if not provided
    name = args.name
    if not name:
        print("\n" + "="*60)
        print("👤 FACE REGISTRATION SYSTEM")
        print("="*60)
        name = input("Enter person's name: ").strip()
        
        if not name:
            print("❌ Name cannot be empty!")
            sys.exit(1)
    
    # Register from image or camera
    if args.image:
        success = register_from_image(name, args.image, config)
    else:
        success = register_from_camera(name, config)
    
    if success:
        print("You can now run 'python main.py' to start recognition!")
    else:
        print("Registration failed. Please try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
