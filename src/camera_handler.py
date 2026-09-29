"""
Camera Handler Module
Manages camera/video capture and frame processing.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import time


class CameraHandler:
    """Handles camera capture and frame management."""
    
    def __init__(self, source: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        """
        Initialize camera handler.
        
        Args:
            source: Camera index (0 for default webcam) or video file path
            width: Frame width
            height: Frame height
            fps: Target frames per second
        """
        self.source = source
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.is_opened = False
        self.frame_count = 0
        self.last_frame_time = 0
    
    def start(self) -> bool:
        """
        Start camera capture.
        
        Returns:
            True if successful, False otherwise
        """
        # Use DirectShow backend on Windows for better compatibility
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera source: {self.source}")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        self.is_opened = True
        self.frame_count = 0
        self.last_frame_time = time.time()
        
        print(f"✓ Camera started: {self.width}x{self.height} @ {self.fps}fps")
        return True
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from camera.
        
        Returns:
            Tuple of (success, frame)
        """
        if not self.is_opened or self.cap is None:
            return False, None
        
        ret, frame = self.cap.read()
        
        if ret:
            self.frame_count += 1
        
        return ret, frame
    
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False
            print("✓ Camera released")
    
    def get_fps(self) -> float:
        """
        Calculate actual FPS.
        
        Returns:
            Current FPS
        """
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        
        if elapsed > 0:
            fps = 1.0 / elapsed
            self.last_frame_time = current_time
            return fps
        
        return 0.0
    
    def resize_frame(self, frame: np.ndarray, scale: float = 0.5) -> np.ndarray:
        """
        Resize frame for faster processing.
        
        Args:
            frame: Input frame
            scale: Scale factor (0.5 = half size)
            
        Returns:
            Resized frame
        """
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        return cv2.resize(frame, (width, height))
    
    def save_frame(self, frame: np.ndarray, filepath: str) -> bool:
        """
        Save frame to file.
        
        Args:
            frame: Frame to save
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cv2.imwrite(filepath, frame)
            print(f"✓ Frame saved: {filepath}")
            return True
        except Exception as e:
            print(f"Error saving frame: {e}")
            return False
    
    def draw_info(self, frame: np.ndarray, text: str, 
                  position: Tuple[int, int] = (10, 30),
                  font_scale: float = 0.7,
                  color: Tuple[int, int, int] = (0, 255, 0),
                  thickness: int = 2) -> np.ndarray:
        """
        Draw information text on frame.
        
        Args:
            frame: Input frame
            text: Text to display
            position: Text position (x, y)
            font_scale: Font size scale
            color: Text color (B, G, R)
            thickness: Text thickness
            
        Returns:
            Frame with text
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, position, font, font_scale, color, thickness)
        return frame
    
    def draw_fps(self, frame: np.ndarray, fps: float) -> np.ndarray:
        """
        Draw FPS counter on frame.
        
        Args:
            frame: Input frame
            fps: FPS value
            
        Returns:
            Frame with FPS counter
        """
        text = f"FPS: {fps:.1f}"
        return self.draw_info(frame, text, position=(10, 30), color=(0, 255, 255))
    
    def capture_snapshot(self, output_dir: str = "data/snapshots") -> Optional[str]:
        """
        Capture and save current frame.
        
        Args:
            output_dir: Directory to save snapshot
            
        Returns:
            Path to saved snapshot or None
        """
        import os
        from datetime import datetime
        
        ret, frame = self.read_frame()
        
        if not ret or frame is None:
            return None
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{timestamp}.jpg"
        filepath = os.path.join(output_dir, filename)
        
        if self.save_frame(frame, filepath):
            return filepath
        
        return None
    
    def apply_mirror(self, frame: np.ndarray) -> np.ndarray:
        """
        Mirror (flip) frame horizontally.
        
        Args:
            frame: Input frame
            
        Returns:
            Mirrored frame
        """
        return cv2.flip(frame, 1)
    
    def get_frame_dimensions(self) -> Tuple[int, int]:
        """
        Get current frame dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        if self.cap is not None and self.is_opened:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return width, height
        return self.width, self.height
    
    def is_camera_open(self) -> bool:
        """
        Check if camera is open.
        
        Returns:
            True if camera is open, False otherwise
        """
        return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    @staticmethod
    def list_available_cameras(max_test: int = 5) -> list:
        """
        List available camera indices.
        
        Args:
            max_test: Maximum number of indices to test
            
        Returns:
            List of available camera indices
        """
        available = []
        for i in range(max_test):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(i)
                cap.release()
        
        return available
