"""
Face Encoder Module
Handles face detection and encoding generation using face_recognition library.
"""

import face_recognition
import cv2
import numpy as np
from typing import List, Tuple, Optional
import os


class FaceEncoder:
    """Handles face detection and encoding generation."""
    
    def __init__(self, model: str = "hog", num_jitters: int = 1):
        """
        Initialize Face Encoder.
        
        Args:
            model: Detection model - "hog" (faster, CPU) or "cnn" (accurate, GPU)
            num_jitters: Number of times to re-sample face for encoding (higher = more accurate but slower)
        """
        self.model = model
        self.num_jitters = num_jitters
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image.
        
        Args:
            image: Image as numpy array (BGR format from OpenCV)
            
        Returns:
            List of face locations as (top, right, bottom, left) tuples
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image, model=self.model)
        
        return face_locations
    
    def encode_face(self, image: np.ndarray, face_location: Optional[Tuple] = None) -> Optional[np.ndarray]:
        """
        Generate face encoding from image.
        
        Args:
            image: Image as numpy array (BGR format from OpenCV)
            face_location: Optional pre-detected face location
            
        Returns:
            128-dimensional face encoding or None if no face found
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Get face locations if not provided
        if face_location is None:
            face_locations = face_recognition.face_locations(rgb_image, model=self.model)
            if not face_locations:
                return None
            face_location = [face_locations[0]]
        else:
            face_location = [face_location]
        
        # Generate encoding
        encodings = face_recognition.face_encodings(
            rgb_image, 
            face_location, 
            num_jitters=self.num_jitters
        )
        
        if encodings:
            return encodings[0]
        return None
    
    def encode_faces(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[Tuple]]:
        """
        Generate encodings for all faces in image.
        
        Args:
            image: Image as numpy array (BGR format from OpenCV)
            
        Returns:
            Tuple of (encodings, face_locations)
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image, model=self.model)
        
        # Generate encodings
        encodings = face_recognition.face_encodings(
            rgb_image, 
            face_locations, 
            num_jitters=self.num_jitters
        )
        
        return encodings, face_locations
    
    def encode_from_file(self, image_path: str) -> Optional[np.ndarray]:
        """
        Generate face encoding from image file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            128-dimensional face encoding or None if no face found
        """
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return None
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image: {image_path}")
            return None
        
        return self.encode_face(image)
    
    def compare_faces(self, known_encodings: List[np.ndarray], 
                     face_encoding: np.ndarray, 
                     tolerance: float = 0.6) -> Tuple[List[bool], List[float]]:
        """
        Compare a face encoding against known encodings.
        
        Args:
            known_encodings: List of known face encodings
            face_encoding: Face encoding to compare
            tolerance: Matching threshold (lower = stricter)
            
        Returns:
            Tuple of (matches, distances) where matches is list of bools and distances is list of floats
        """
        if not known_encodings:
            return [], []
        
        # Calculate face distances
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        
        # Determine matches
        matches = list(distances <= tolerance)
        
        return matches, distances.tolist()
    
    def find_best_match(self, known_encodings: List[np.ndarray], 
                       face_encoding: np.ndarray,
                       tolerance: float = 0.6) -> Tuple[Optional[int], Optional[float]]:
        """
        Find the best matching face encoding.
        
        Args:
            known_encodings: List of known face encodings
            face_encoding: Face encoding to compare
            tolerance: Matching threshold
            
        Returns:
            Tuple of (best_match_index, distance) or (None, None) if no match
        """
        matches, distances = self.compare_faces(known_encodings, face_encoding, tolerance)
        
        if not matches or not any(matches):
            return None, None
        
        # Find best match (lowest distance)
        best_match_index = np.argmin(distances)
        
        if matches[best_match_index]:
            return best_match_index, distances[best_match_index]
        
        return None, None
    
    def validate_face_quality(self, image: np.ndarray, min_size: int = 20) -> bool:
        """
        Validate if face in image meets quality requirements.
        
        Args:
            image: Image as numpy array
            min_size: Minimum face size in pixels
            
        Returns:
            True if face quality is acceptable, False otherwise
        """
        face_locations = self.detect_faces(image)
        
        if not face_locations:
            return False
        
        # Check face size
        top, right, bottom, left = face_locations[0]
        width = right - left
        height = bottom - top
        
        if width < min_size or height < min_size:
            return False
        
        # Check if face is too close to edges (might be cropped)
        img_height, img_width = image.shape[:2]
        margin = 10
        
        if (top < margin or left < margin or 
            bottom > img_height - margin or right > img_width - margin):
            return False
        
        return True
    
    def draw_face_box(self, image: np.ndarray, face_location: Tuple, 
                     label: str = "", color: Tuple[int, int, int] = (0, 255, 0),
                     thickness: int = 2) -> np.ndarray:
        """
        Draw bounding box and label on face.
        
        Args:
            image: Image as numpy array
            face_location: Face location as (top, right, bottom, left)
            label: Text label to display
            color: Box color as (B, G, R)
            thickness: Line thickness
            
        Returns:
            Image with drawn box
        """
        top, right, bottom, left = face_location
        
        # Draw rectangle
        cv2.rectangle(image, (left, top), (right, bottom), color, thickness)
        
        # Draw label background
        if label:
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.6
            font_thickness = 1
            
            # Get text size
            (text_width, text_height), baseline = cv2.getTextSize(
                label, font, font_scale, font_thickness
            )
            
            # Draw background rectangle
            cv2.rectangle(
                image,
                (left, bottom - text_height - baseline - 10),
                (left + text_width + 10, bottom),
                color,
                cv2.FILLED
            )
            
            # Draw text
            cv2.putText(
                image,
                label,
                (left + 5, bottom - 5),
                font,
                font_scale,
                (255, 255, 255),
                font_thickness
            )
        
        return image
