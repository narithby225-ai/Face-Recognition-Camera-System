"""
Register People from Dataset Folder
ចុះឈ្មោះមនុស្សពី Dataset Folder

This script automatically registers people from images in the dataset folder.
Format: [ID]_[Name].jpg (e.g., 001_Narith.jpg, 002_Dara.jpg)
"""

import os
import cv2
import json
import sys
from pathlib import Path

from src.face_encoder import FaceEncoder
from src.database_manager import DatabaseManager


def load_config(config_path: str = "config/config.json") -> dict:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config


def parse_filename(filename: str):
    """
    Parse filename to extract ID and name.
    Format: [ID]_[Name].jpg
    Example: 001_Narith.jpg -> (1, "Narith")
    """
    # Remove extension
    name_part = filename.rsplit('.', 1)[0]
    
    # Split by first underscore
    parts = name_part.split('_', 1)
    
    if len(parts) != 2:
        return None, None
    
    try:
        person_id = int(parts[0])
        person_name = parts[1].replace('_', ' ')
        return person_id, person_name
    except ValueError:
        return None, None


def register_from_dataset(dataset_folder: str = "dataset", config: dict = None):
    """Register all people from dataset folder."""
    
    if not os.path.exists(dataset_folder):
        print(f"❌ Dataset folder not found: {dataset_folder}")
        print(f"   Please create folder and add images in format: 001_Name.jpg")
        return
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for file in os.listdir(dataset_folder):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    if not image_files:
        print(f"❌ No images found in {dataset_folder}/")
        print(f"   Add images in format: 001_Name.jpg, 002_Name.jpg")
        return
    
    print("\n" + "="*70)
    print("📂 REGISTER FROM DATASET")
    print("="*70)
    print(f"Dataset folder: {dataset_folder}")
    print(f"Found {len(image_files)} image(s)")
    print("="*70 + "\n")
    
    # Initialize components
    encoder = FaceEncoder(
        model=config['recognition']['model'],
        num_jitters=config['registration'].get('num_jitters', 1)
    )
    
    db_manager = DatabaseManager(config['database']['path'])
    
    # Process each image
    registered_count = 0
    skipped_count = 0
    error_count = 0
    
    for filename in sorted(image_files):
        # Parse filename
        person_id, person_name = parse_filename(filename)
        
        if person_id is None or person_name is None:
            print(f"⚠️  Skipped: {filename} (invalid format)")
            print(f"   Expected format: 001_Name.jpg")
            skipped_count += 1
            continue
        
        # Check if already registered
        if db_manager.person_exists(person_name):
            print(f"⚠️  Skipped: {filename} (already registered)")
            skipped_count += 1
            continue
        
        # Load image (handle Khmer/Unicode filenames)
        image_path = os.path.join(dataset_folder, filename)
        try:
            # Use numpy to handle Unicode filenames
            import numpy as np
            with open(image_path, 'rb') as f:
                file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Failed to decode image")
        except Exception as e:
            print(f"❌ Error: Could not load {filename} - {str(e)}")
            error_count += 1
            continue
        
        print(f"📷 Processing: {filename} -> {person_name}...")
        
        # Detect faces
        face_locations = encoder.detect_faces(image)
        
        if len(face_locations) == 0:
            print(f"   ❌ No face detected in {filename}")
            error_count += 1
            continue
        
        if len(face_locations) > 1:
            print(f"   ⚠️  Multiple faces detected, using first one")
        
        # Encode face
        encoding = encoder.encode_face(image, face_locations[0])
        
        if encoding is None:
            print(f"   ❌ Failed to encode face in {filename}")
            error_count += 1
            continue
        
        # Register in database
        try:
            registered_id = db_manager.register_person(
                person_name, 
                [encoding], 
                [image_path],
                notes=f"Registered from dataset: {filename}"
            )
            print(f"   ✓ Registered: {person_name} (ID: {registered_id})")
            registered_count += 1
        except Exception as e:
            print(f"   ❌ Error registering {person_name}: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 REGISTRATION SUMMARY")
    print("="*70)
    print(f"✓ Successfully registered: {registered_count}")
    print(f"⚠️  Skipped: {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📁 Total images processed: {len(image_files)}")
    print("="*70 + "\n")
    
    if registered_count > 0:
        print("✅ You can now run face recognition:")
        print(f"   .\\venv\\Scripts\\python.exe main.py")
        print("\nTo view registered persons:")
        print(f"   .\\venv\\Scripts\\python.exe main.py --show-database")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Register people from dataset folder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ឧទាហរណ៍ (Examples):
  python register_from_dataset.py
  python register_from_dataset.py --dataset my_dataset
  
ទម្រង់ឈ្មោះឯកសារ (Filename Format):
  001_Narith.jpg
  002_Dara.jpg
  003_Sokha.jpg
  
រចនាសម្ព័ន្ធថត (Folder Structure):
  dataset/
  ├── 001_Narith.jpg
  ├── 002_Dara.jpg
  └── 003_Sokha.jpg
        """
    )
    
    parser.add_argument(
        '--dataset',
        type=str,
        default='dataset',
        help='Path to dataset folder (default: dataset)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.json',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Register from dataset
    register_from_dataset(args.dataset, config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
