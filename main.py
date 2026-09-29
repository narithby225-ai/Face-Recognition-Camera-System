"""
Main Application Entry Point
Face Recognition Camera System
"""

import argparse
import json
import os
import sys

from src.face_recognition_system import FaceRecognitionSystem
from src.database_manager import DatabaseManager


def load_config(config_path: str = "config/config.json") -> dict:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def show_database(config: dict):
    """Display all registered persons in database."""
    db_manager = DatabaseManager(config['database']['path'])
    persons = db_manager.get_all_persons()
    
    if not persons:
        print("\n📋 Database is empty. No persons registered yet.")
        print("   Use 'python register_face.py' to register someone.\n")
        return
    
    print("\n" + "="*80)
    print("📋 REGISTERED PERSONS DATABASE")
    print("="*80)
    print(f"{'ID':<6} {'Name':<25} {'Registered':<20} {'Last Seen':<20}")
    print("-"*80)
    
    for person in persons:
        person_id = person['id']
        name = person['name']
        reg_date = person['registration_date'][:19] if person['registration_date'] else 'N/A'
        last_seen = person['last_seen'][:19] if person['last_seen'] else 'Never'
        
        print(f"{person_id:<6} {name:<25} {reg_date:<20} {last_seen:<20}")
    
    print("-"*80)
    print(f"Total: {len(persons)} person(s) registered")
    print("="*80 + "\n")


def show_statistics(config: dict):
    """Display system statistics."""
    db_manager = DatabaseManager(config['database']['path'])
    person_count = db_manager.get_person_count()
    encodings, _, _ = db_manager.get_all_encodings()
    
    print("\n" + "="*80)
    print("📊 SYSTEM STATISTICS")
    print("="*80)
    print(f"Registered Persons:      {person_count}")
    print(f"Total Face Encodings:    {len(encodings)}")
    print(f"Average Encodings/Person: {len(encodings)/person_count if person_count > 0 else 0:.1f}")
    print(f"Detection Model:         {config['recognition']['model'].upper()}")
    print(f"Recognition Tolerance:   {config['recognition']['tolerance']}")
    print(f"Camera Resolution:       {config['camera']['width']}x{config['camera']['height']}")
    print("="*80 + "\n")


def test_camera(config: dict):
    """Test camera functionality."""
    from src.camera_handler import CameraHandler
    
    print("\n🎥 Testing camera...\n")
    
    # List available cameras
    available = CameraHandler.list_available_cameras()
    print(f"Available cameras: {available}")
    
    if not available:
        print("❌ No cameras found!")
        return
    
    # Test camera
    camera = CameraHandler(
        source=config['camera']['source'],
        width=config['camera']['width'],
        height=config['camera']['height']
    )
    
    if camera.start():
        print("✓ Camera started successfully")
        print("  Press 'Q' to close test window")
        
        import cv2
        while True:
            ret, frame = camera.read_frame()
            if ret and frame is not None:
                cv2.imshow('Camera Test', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        camera.release()
        cv2.destroyAllWindows()
    else:
        print("❌ Failed to start camera")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Face Recognition Camera System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start face recognition
  python main.py --show-database    # View registered persons
  python main.py --stats            # Show system statistics
  python main.py --test-camera      # Test camera functionality
  python main.py --config custom.json  # Use custom config file
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.json',
        help='Path to configuration file (default: config/config.json)'
    )
    
    parser.add_argument(
        '--show-database',
        action='store_true',
        help='Display all registered persons'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show system statistics'
    )
    
    parser.add_argument(
        '--test-camera',
        action='store_true',
        help='Test camera functionality'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Handle different modes
    if args.show_database:
        show_database(config)
        return
    
    if args.stats:
        show_statistics(config)
        return
    
    if args.test_camera:
        test_camera(config)
        return
    
    # Run face recognition system
    print("\n" + "="*80)
    print("🎯 FACE RECOGNITION CAMERA SYSTEM")
    print("="*80)
    print("Initializing system...\n")
    
    try:
        system = FaceRecognitionSystem(config)
        system.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
