"""
Face Recognition Camera System
A comprehensive system for face detection, recognition, and ID assignment.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .face_recognition_system import FaceRecognitionSystem
from .database_manager import DatabaseManager
from .face_encoder import FaceEncoder
from .camera_handler import CameraHandler

__all__ = [
    'FaceRecognitionSystem',
    'DatabaseManager',
    'FaceEncoder',
    'CameraHandler'
]
