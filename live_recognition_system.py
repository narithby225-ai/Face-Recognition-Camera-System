"""
Live Face Recognition System with Welcome Greeting
Detects faces in real-time and displays "Welcome [Name]"
"""

import cv2
import numpy as np
import face_recognition
import pickle
import time
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Optional, Tuple
import requests


class LiveRecognitionSystem:
    """Real-time face recognition with instant greeting display"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the system"""
        self.config = self.load_config(config_path)
        
        # Camera settings
        self.camera_id = self.config['camera']['source']
        self.camera = None
        
        # Recognition settings
        self.tolerance = self.config['recognition']['tolerance']
        self.model = self.config['recognition']['model']
        self.frame_skip = self.config['recognition']['frame_skip']
        
        # Known faces storage
        self.known_encodings = []
        self.known_names = []
        self.known_ids = []
        
        # Tracking
        self.last_recognized = {}
        self.recognition_cooldown = 3.0  # seconds between same person recognition
        
        # Display settings
        self.welcome_duration = 5.0  # Show welcome message for 5 seconds
        self.active_greetings = {}  # {person_name: end_time}
        
        # Frame processing
        self.frame_counter = 0
        self.fps = 0
        self.fps_start_time = time.time()
        
        # Load known faces
        self.load_known_faces()
        
        # API settings (optional)
        self.api_url = "http://localhost:8000"
        self.api_enabled = False
        
    def load_config(self, config_path: str) -> dict:
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {
                'camera': {'source': 0},
                'recognition': {
                    'tolerance': 0.6,
                    'model': 'hog',
                    'frame_skip': 2
                }
            }
    
    def load_known_faces(self):
        """Load known faces from database or pickle file"""
        print("Loading known faces...")
        
        # Try loading from pickle file first
        encodings_file = Path("data/encodings/face_encodings.pkl")
        
        if encodings_file.exists():
            try:
                with open(encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_encodings = data['encodings']
                    self.known_names = data['names']
                    self.known_ids = data.get('ids', list(range(len(data['names']))))
                
                print(f"✓ Loaded {len(self.known_names)} known face(s)")
                return
            except Exception as e:
                print(f"Error loading pickle file: {e}")
        
        # Try loading from dataset folder
        dataset_path = Path("dataset")
        if dataset_path.exists():
            self.load_from_dataset(dataset_path)
        else:
            print("⚠ No known faces found. Register faces first!")
    
    def load_from_dataset(self, dataset_path: Path):
        """Load faces from dataset folder"""
        print("Loading from dataset folder...")
        
        image_extensions = ['.jpg', '.jpeg', '.png']
        count = 0
        
        for img_file in dataset_path.glob("*"):
            if img_file.suffix.lower() in image_extensions:
                try:
                    # Parse filename: 001_ID_Name.jpg
                    filename = img_file.stem
                    parts = filename.split('_', 2)
                    
                    if len(parts) >= 2:
                        person_id = parts[0]
                        person_name = parts[-1].replace('_', ' ')
                    else:
                        person_id = str(count)
                        person_name = filename
                    
                    # Load and encode face
                    image = face_recognition.load_image_file(str(img_file))
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        self.known_encodings.append(encodings[0])
                        self.known_names.append(person_name)
                        self.known_ids.append(person_id)
                        count += 1
                        print(f"  ✓ Loaded: {person_name}")
                
                except Exception as e:
                    print(f"  ✗ Failed to load {img_file.name}: {e}")
        
        print(f"✓ Loaded {count} face(s) from dataset")
    
    def start_camera(self) -> bool:
        """Start camera with DirectShow backend"""
        print("Starting camera...")
        
        # Try DirectShow backend (Windows)
        self.camera = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        
        if not self.camera.isOpened():
            # Fallback to default
            self.camera = cv2.VideoCapture(self.camera_id)
        
        if not self.camera.isOpened():
            print("✗ Failed to open camera!")
            return False
        
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        
        # Give camera time to warm up and stabilize
        print("⏳ Warming up camera...")
        time.sleep(2)
        
        # Read and discard first few frames (they might be black)
        for i in range(5):
            ret, frame = self.camera.read()
            if ret and frame is not None and frame.any():
                break
            time.sleep(0.1)
        
        # Verify camera is working
        ret, test_frame = self.camera.read()
        if not ret or test_frame is None:
            print("✗ Camera opened but can't read frames!")
            return False
        
        print("✓ Camera started successfully")
        return True
    
    def recognize_faces(self, frame: np.ndarray) -> List[Dict]:
        """Recognize faces in frame"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame, model=self.model)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        results = []
        current_time = time.time()
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Scale back face location
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Compare with known faces
            if self.known_encodings:
                matches = face_recognition.compare_faces(
                    self.known_encodings, 
                    face_encoding, 
                    tolerance=self.tolerance
                )
                face_distances = face_recognition.face_distance(
                    self.known_encodings, 
                    face_encoding
                )
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]
                        person_id = self.known_ids[best_match_index]
                        confidence = 1.0 - face_distances[best_match_index]
                        
                        # Check cooldown
                        if name in self.last_recognized:
                            if current_time - self.last_recognized[name] < self.recognition_cooldown:
                                continue
                        
                        # Update tracking
                        self.last_recognized[name] = current_time
                        
                        # Add to active greetings
                        self.active_greetings[name] = current_time + self.welcome_duration
                        
                        results.append({
                            'name': name,
                            'id': person_id,
                            'confidence': confidence,
                            'location': (top, right, bottom, left),
                            'recognized': True
                        })
                        
                        # Print to console
                        print(f"👋 Welcome {name}! (Confidence: {confidence:.2f})")
                        
                        # Optional: Send to API
                        if self.api_enabled:
                            self.mark_attendance_api(person_id, name, confidence)
                        
                        continue
            
            # Unknown face
            results.append({
                'name': 'Unknown',
                'id': None,
                'confidence': 0.0,
                'location': (top, right, bottom, left),
                'recognized': False
            })
        
        return results
    
    def draw_results(self, frame: np.ndarray, results: List[Dict]) -> np.ndarray:
        """Draw face boxes and welcome messages with ID and Name"""
        current_time = time.time()
        
        # Draw face detections
        for result in results:
            top, right, bottom, left = result['location']
            name = result['name']
            person_id = result['id']
            confidence = result['confidence']
            recognized = result['recognized']
            
            # Choose color
            if recognized:
                color = (0, 255, 0)  # Green for known
                
                # Create ID and Name labels
                id_label = f"ID: {person_id}"
                name_label = f"Name: {name}"
                confidence_label = f"Confidence: {confidence:.0%}"
                
                # Draw rectangle around face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
                
                # Calculate label dimensions
                font = cv2.FONT_HERSHEY_DUPLEX
                font_scale = 0.7
                thickness = 2
                
                id_size = cv2.getTextSize(id_label, font, font_scale, thickness)[0]
                name_size = cv2.getTextSize(name_label, font, font_scale, thickness)[0]
                conf_size = cv2.getTextSize(confidence_label, font, 0.5, 1)[0]
                
                # Calculate total height needed
                label_height = id_size[1] + name_size[1] + conf_size[1] + 30
                max_width = max(id_size[0], name_size[0], conf_size[0]) + 20
                
                # Draw background for labels (above the face)
                cv2.rectangle(
                    frame, 
                    (left, top - label_height - 10), 
                    (left + max_width, top), 
                    color, 
                    cv2.FILLED
                )
                
                # Draw ID
                cv2.putText(
                    frame, id_label, 
                    (left + 10, top - label_height + 20),
                    font, font_scale, (255, 255, 255), thickness
                )
                
                # Draw Name
                cv2.putText(
                    frame, name_label, 
                    (left + 10, top - label_height + 50),
                    font, font_scale, (255, 255, 255), thickness
                )
                
                # Draw Confidence
                cv2.putText(
                    frame, confidence_label, 
                    (left + 10, top - label_height + 70),
                    font, 0.5, (255, 255, 255), 1
                )
                
            else:
                color = (0, 0, 255)  # Red for unknown
                label = "Unknown Person"
                
                # Draw rectangle
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw label background
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                
                # Draw label text
                cv2.putText(
                    frame, label, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1
                )
        
        # Draw welcome messages (large overlay with ID and Name)
        y_offset = 80
        for name, end_time in list(self.active_greetings.items()):
            if current_time < end_time:
                # Calculate fade effect
                remaining = end_time - current_time
                alpha = min(remaining / self.welcome_duration, 1.0)
                
                # Find the person's ID from known_names
                person_id = "N/A"
                try:
                    idx = self.known_names.index(name)
                    person_id = self.known_ids[idx]
                except:
                    pass
                
                # Create welcome message with ID and Name
                welcome_text = f"WELCOME!"
                id_text = f"ID: {person_id}"
                name_text = f"{name}"
                
                # Measure text sizes
                font = cv2.FONT_HERSHEY_DUPLEX
                welcome_font_scale = 2.0
                info_font_scale = 1.2
                thickness = 4
                info_thickness = 3
                
                welcome_size = cv2.getTextSize(welcome_text, font, welcome_font_scale, thickness)[0]
                id_size = cv2.getTextSize(id_text, font, info_font_scale, info_thickness)[0]
                name_size = cv2.getTextSize(name_text, font, info_font_scale, info_thickness)[0]
                
                # Calculate total dimensions
                max_width = max(welcome_size[0], id_size[0], name_size[0]) + 60
                total_height = welcome_size[1] + id_size[1] + name_size[1] + 60
                
                # Center position
                box_x = (frame.shape[1] - max_width) // 2
                box_y = y_offset
                
                # Draw background rectangle with alpha
                overlay = frame.copy()
                cv2.rectangle(
                    overlay,
                    (box_x, box_y),
                    (box_x + max_width, box_y + total_height),
                    (0, 120, 0),
                    -1
                )
                cv2.addWeighted(overlay, alpha * 0.8, frame, 1 - alpha * 0.8, 0, frame)
                
                # Draw border
                cv2.rectangle(
                    frame,
                    (box_x, box_y),
                    (box_x + max_width, box_y + total_height),
                    (0, 255, 0),
                    3
                )
                
                # Calculate centered text positions
                welcome_x = box_x + (max_width - welcome_size[0]) // 2
                id_x = box_x + (max_width - id_size[0]) // 2
                name_x = box_x + (max_width - name_size[0]) // 2
                
                # Draw "WELCOME!" text
                cv2.putText(
                    frame, welcome_text, 
                    (welcome_x, box_y + welcome_size[1] + 15),
                    font, welcome_font_scale, (255, 255, 255), thickness
                )
                
                # Draw ID text
                cv2.putText(
                    frame, id_text, 
                    (id_x, box_y + welcome_size[1] + id_size[1] + 30),
                    font, info_font_scale, (255, 255, 100), info_thickness
                )
                
                # Draw Name text
                cv2.putText(
                    frame, name_text, 
                    (name_x, box_y + welcome_size[1] + id_size[1] + name_size[1] + 45),
                    font, info_font_scale, (255, 255, 255), info_thickness
                )
                
                y_offset += total_height + 20
            else:
                # Remove expired greeting
                del self.active_greetings[name]
        
        return frame
    
    def draw_info(self, frame: np.ndarray) -> np.ndarray:
        """Draw FPS and system info"""
        # Calculate FPS
        self.frame_counter += 1
        elapsed = time.time() - self.fps_start_time
        if elapsed > 1.0:
            self.fps = self.frame_counter / elapsed
            self.frame_counter = 0
            self.fps_start_time = time.time()
        
        # Draw FPS
        cv2.putText(
            frame, f"FPS: {self.fps:.1f}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
        )
        
        # Draw known faces count
        cv2.putText(
            frame, f"Known: {len(self.known_names)}", (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1
        )
        
        # Draw active greetings count
        active_count = len(self.active_greetings)
        if active_count > 0:
            cv2.putText(
                frame, f"Active Greetings: {active_count}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1
            )
        
        return frame
    
    def mark_attendance_api(self, person_id: str, name: str, confidence: float):
        """Mark attendance via API"""
        try:
            # This would call your backend API
            # Placeholder for now
            pass
        except Exception as e:
            print(f"API error: {e}")
    
    def run(self):
        """Main loop"""
        if not self.start_camera():
            return
        
        print("\n" + "="*60)
        print("🎥 LIVE FACE RECOGNITION SYSTEM")
        print("="*60)
        print("Controls:")
        print("  Q - Quit")
        print("  S - Save screenshot")
        print("  D - Toggle debug mode")
        print("  R - Reload known faces")
        print("="*60 + "\n")
        
        debug_mode = False
        
        try:
            while True:
                ret, frame = self.camera.read()
                
                if not ret or frame is None:
                    print("✗ Failed to read frame")
                    break
                
                # Process frame (with skipping for performance)
                self.frame_counter += 1
                if self.frame_counter % self.frame_skip == 0:
                    results = self.recognize_faces(frame)
                    
                    # Draw results
                    frame = self.draw_results(frame, results)
                else:
                    # Still draw active greetings even when skipping detection
                    current_time = time.time()
                    y_offset = 100
                    for name, end_time in list(self.active_greetings.items()):
                        if current_time < end_time:
                            welcome_text = f"Welcome {name}!"
                            font = cv2.FONT_HERSHEY_DUPLEX
                            font_scale = 1.5
                            thickness = 3
                            text_size = cv2.getTextSize(welcome_text, font, font_scale, thickness)[0]
                            text_x = (frame.shape[1] - text_size[0]) // 2
                            text_y = y_offset
                            
                            cv2.rectangle(
                                frame,
                                (text_x - 20, text_y - text_size[1] - 20),
                                (text_x + text_size[0] + 20, text_y + 20),
                                (0, 100, 0),
                                -1
                            )
                            cv2.putText(
                                frame, welcome_text, (text_x, text_y),
                                font, font_scale, (255, 255, 255), thickness
                            )
                            y_offset += 100
                        else:
                            del self.active_greetings[name]
                
                # Draw info
                frame = self.draw_info(frame)
                
                # Show frame
                cv2.imshow('Live Face Recognition - Welcome System', frame)
                
                # Handle keyboard
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\nExiting...")
                    break
                elif key == ord('s') or key == ord('S'):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshots/welcome_{timestamp}.jpg"
                    Path("screenshots").mkdir(exist_ok=True)
                    cv2.imwrite(filename, frame)
                    print(f"✓ Saved: {filename}")
                elif key == ord('d') or key == ord('D'):
                    debug_mode = not debug_mode
                    print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                elif key == ord('r') or key == ord('R'):
                    print("Reloading known faces...")
                    self.load_known_faces()
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        finally:
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            print("✓ System stopped")


def main():
    """Entry point"""
    print("\n" + "="*60)
    print("🎯 Live Face Recognition with Welcome Greeting")
    print("="*60)
    print("\nInitializing system...")
    
    system = LiveRecognitionSystem()
    
    if len(system.known_names) == 0:
        print("\n⚠️  WARNING: No known faces loaded!")
        print("\nTo add known faces:")
        print("1. Run: python register_face.py")
        print("2. Or put photos in dataset/ folder")
        print("\nContinue anyway? (y/n): ", end='')
        
        response = input().strip().lower()
        if response != 'y':
            print("Exiting...")
            return
    
    system.run()


if __name__ == "__main__":
    main()
