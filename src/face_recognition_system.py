"""
Face Recognition System
Main system integrating camera, face detection, recognition, and database.
"""

import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
import time
import os

from .camera_handler import CameraHandler
from .face_encoder import FaceEncoder
from .database_manager import DatabaseManager


class FaceRecognitionSystem:
    """Main face recognition system."""
    
    def __init__(self, config: Dict):
        """
        Initialize face recognition system.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize components
        self.camera = CameraHandler(
            source=config['camera']['source'],
            width=config['camera']['width'],
            height=config['camera']['height'],
            fps=config['camera']['fps']
        )
        
        self.encoder = FaceEncoder(
            model=config['recognition']['model'],
            num_jitters=config['recognition']['num_jitters']
        )
        
        self.database = DatabaseManager(
            db_path=config['database']['path']
        )
        
        # Recognition settings
        self.tolerance = config['recognition']['tolerance']
        self.frame_skip = config['recognition']['frame_skip']
        
        # Display settings
        self.show_confidence = config['display']['show_confidence']
        self.show_id = config['display']['show_id']
        self.box_color = tuple(config['display']['box_color'])
        self.text_color = tuple(config['display']['text_color'])
        self.unknown_color = tuple(config['display']['unknown_color'])
        
        # Load known faces from database
        self.known_encodings = []
        self.known_person_ids = []
        self.known_names = []
        self.load_known_faces()
        
        # Frame processing
        self.frame_counter = 0
        self.process_this_frame = True
        
        # Recognition cache (to avoid flickering)
        self.last_recognition = {}
        self.recognition_cache_time = 0.5  # seconds
        
        # FPS tracking
        self.fps = 0.0
        self.fps_update_time = time.time()
        self.fps_frame_count = 0
    
    def load_known_faces(self):
        """Load known face encodings from database."""
        print("Loading known faces from database...")
        
        encodings, person_ids, names = self.database.get_all_encodings()
        
        self.known_encodings = encodings
        self.known_person_ids = person_ids
        self.known_names = names
        
        unique_persons = len(set(person_ids))
        print(f"✓ Loaded {len(encodings)} encodings for {unique_persons} person(s)")
    
    def reload_database(self):
        """Reload face encodings from database."""
        self.load_known_faces()
    
    def start_camera(self) -> bool:
        """
        Start camera capture.
        
        Returns:
            True if successful, False otherwise
        """
        return self.camera.start()
    
    def stop_camera(self):
        """Stop camera capture."""
        self.camera.release()
    
    def recognize_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        Recognize faces in frame.
        
        Args:
            frame: Input frame
            
        Returns:
            List of recognition results with person info and locations
        """
        # Detect and encode faces
        face_encodings, face_locations = self.encoder.encode_faces(frame)
        
        results = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            if self.known_encodings:
                best_match_idx, distance = self.encoder.find_best_match(
                    self.known_encodings,
                    face_encoding,
                    self.tolerance
                )
                
                if best_match_idx is not None:
                    person_id = self.known_person_ids[best_match_idx]
                    name = self.known_names[best_match_idx]
                    confidence = 1.0 - distance
                    
                    # Update last seen
                    self.database.update_last_seen(person_id)
                    
                    results.append({
                        'person_id': person_id,
                        'name': name,
                        'confidence': confidence,
                        'distance': distance,
                        'location': face_location,
                        'known': True
                    })
                else:
                    # Unknown face
                    results.append({
                        'person_id': None,
                        'name': 'Unknown',
                        'confidence': 0.0,
                        'distance': None,
                        'location': face_location,
                        'known': False
                    })
            else:
                # No known faces in database
                results.append({
                    'person_id': None,
                    'name': 'Unknown',
                    'confidence': 0.0,
                    'distance': None,
                    'location': face_location,
                    'known': False
                })
        
        return results
    
    def draw_results(self, frame: np.ndarray, results: List[Dict]) -> np.ndarray:
        """
        Draw recognition results on frame.
        
        Args:
            frame: Input frame
            results: Recognition results
            
        Returns:
            Frame with drawn results
        """
        for result in results:
            location = result['location']
            name = result['name']
            person_id = result['person_id']
            confidence = result['confidence']
            known = result['known']
            
            # Choose color
            color = self.box_color if known else self.unknown_color
            
            # Build label
            if known and self.show_id:
                label = f"ID:{person_id} {name}"
            else:
                label = name
            
            if self.show_confidence and known:
                label += f" ({confidence:.2f})"
            
            # Draw face box with label
            frame = self.encoder.draw_face_box(
                frame,
                location,
                label,
                color
            )
        
        return frame
    
    def update_fps(self):
        """Update FPS calculation."""
        self.fps_frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.fps_update_time
        
        if elapsed >= 1.0:
            self.fps = self.fps_frame_count / elapsed
            self.fps_frame_count = 0
            self.fps_update_time = current_time
    
    def process_frame(self, frame: np.ndarray, skip_recognition: bool = False) -> Tuple[np.ndarray, List[Dict]]:
        """
        Process a single frame.
        
        Args:
            frame: Input frame
            skip_recognition: If True, only draw cached results
            
        Returns:
            Tuple of (processed_frame, recognition_results)
        """
        results = []
        
        # Frame skipping for performance
        if not skip_recognition:
            self.frame_counter += 1
            self.process_this_frame = (self.frame_counter % self.frame_skip == 0)
        
        # Recognize faces
        if self.process_this_frame and not skip_recognition:
            results = self.recognize_faces(frame)
            self.last_recognition = {
                'results': results,
                'time': time.time()
            }
        else:
            # Use cached results if recent
            if self.last_recognition and \
               (time.time() - self.last_recognition['time']) < self.recognition_cache_time:
                results = self.last_recognition['results']
        
        # Draw results
        if results:
            frame = self.draw_results(frame, results)
        
        # Update and draw FPS
        self.update_fps()
        frame = self.camera.draw_fps(frame, self.fps)
        
        # Draw person count
        person_count = len([r for r in results if r['known']])
        unknown_count = len([r for r in results if not r['known']])
        count_text = f"Recognized: {person_count} | Unknown: {unknown_count}"
        frame = self.camera.draw_info(
            frame, 
            count_text, 
            position=(10, frame.shape[0] - 20),
            color=(255, 255, 255)
        )
        
        return frame, results
    
    def run(self):
        """Run the face recognition system in real-time."""
        if not self.start_camera():
            print("Failed to start camera!")
            return
        
        print("\n" + "="*50)
        print("Face Recognition System Running")
        print("="*50)
        print("Controls:")
        print("  [Q] - Quit")
        print("  [R] - Reload database")
        print("  [S] - Save screenshot")
        print("  [D] - Toggle debug mode")
        print("="*50 + "\n")
        
        debug_mode = False
        
        try:
            while True:
                # Read frame
                ret, frame = self.camera.read_frame()
                
                if not ret or frame is None:
                    print("Failed to read frame")
                    break
                
                # Process frame
                processed_frame, results = self.process_frame(frame)
                
                # Debug mode - show additional info
                if debug_mode:
                    info_y = 60
                    cv2.putText(processed_frame, f"Known faces: {len(set(self.known_person_ids))}", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    info_y += 25
                    cv2.putText(processed_frame, f"Encodings: {len(self.known_encodings)}", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    info_y += 25
                    cv2.putText(processed_frame, f"Tolerance: {self.tolerance}", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                
                # Display frame
                cv2.imshow('Face Recognition System', processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\nExiting...")
                    break
                elif key == ord('r') or key == ord('R'):
                    print("\nReloading database...")
                    self.reload_database()
                elif key == ord('s') or key == ord('S'):
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"data/screenshots/screenshot_{timestamp}.jpg"
                    os.makedirs("data/screenshots", exist_ok=True)
                    self.camera.save_frame(processed_frame, filename)
                elif key == ord('d') or key == ord('D'):
                    debug_mode = not debug_mode
                    print(f"\nDebug mode: {'ON' if debug_mode else 'OFF'}")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        finally:
            self.stop_camera()
            cv2.destroyAllWindows()
            print("✓ System stopped")
    
    def get_statistics(self) -> Dict:
        """
        Get system statistics.
        
        Returns:
            Dictionary with system statistics
        """
        person_count = self.database.get_person_count()
        
        return {
            'total_persons': person_count,
            'total_encodings': len(self.known_encodings),
            'current_fps': self.fps,
            'tolerance': self.tolerance,
            'detection_model': self.encoder.model
        }
