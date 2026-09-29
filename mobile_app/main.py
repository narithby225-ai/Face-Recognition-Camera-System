"""
Face Recognition Mobile App
Built with Kivy + KivyMD for Android
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem

import cv2
import numpy as np
import face_recognition
import json
import os
from pathlib import Path
from datetime import datetime
import pickle


class FaceRecognitionEngine:
    """Core face recognition engine"""
    
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.known_ids = []
        self.tolerance = 0.6
        self.last_recognized = {}
        self.recognition_cooldown = 3.0
        
        # Load known faces
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from dataset"""
        dataset_path = Path("dataset")
        
        if not dataset_path.exists():
            print("Warning: No dataset folder found")
            return
        
        image_extensions = ['.jpg', '.jpeg', '.png']
        count = 0
        
        for img_file in dataset_path.glob("*"):
            if img_file.suffix.lower() in image_extensions:
                try:
                    # Parse filename: 001_DUC20240147_Name.jpg
                    filename = img_file.stem
                    parts = filename.split('_', 2)
                    
                    if len(parts) >= 3:
                        person_id = parts[1]
                        person_name = parts[2].replace('_', ' ')
                    else:
                        person_id = str(count)
                        person_name = filename
                    
                    # Load and encode face (handle Unicode paths)
                    with open(str(img_file), 'rb') as f:
                        file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    encodings = face_recognition.face_encodings(image_rgb)
                    
                    if encodings:
                        self.known_encodings.append(encodings[0])
                        self.known_names.append(person_name)
                        self.known_ids.append(person_id)
                        count += 1
                        print(f"Loaded: {person_name} ({person_id})")
                
                except Exception as e:
                    print(f"Failed to load {img_file.name}: {e}")
        
        print(f"Total loaded: {count} faces")
    
    def recognize_face(self, frame):
        """Recognize face in frame"""
        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        results = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Scale back coordinates
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
                        
                        results.append({
                            'name': name,
                            'id': person_id,
                            'confidence': confidence,
                            'location': (top, right, bottom, left),
                            'recognized': True
                        })
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


class WelcomeScreen(Screen):
    """Welcome/Home screen"""
    pass


class CameraScreen(Screen):
    """Camera screen with face recognition"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = FaceRecognitionEngine()
        self.recognition_active = False
        self.last_result = None
        
    def on_enter(self):
        """Called when entering screen"""
        self.start_recognition()
    
    def start_recognition(self):
        """Start face recognition"""
        self.recognition_active = True
        Clock.schedule_interval(self.update, 1.0 / 10.0)  # 10 FPS
    
    def stop_recognition(self):
        """Stop face recognition"""
        self.recognition_active = False
        Clock.unschedule(self.update)
    
    def update(self, dt):
        """Update face recognition"""
        if not self.recognition_active:
            return
        
        # Get camera widget
        camera = self.ids.camera
        
        # Capture frame
        texture = camera.texture
        if texture is None:
            return
        
        # Convert texture to numpy array
        frame = np.frombuffer(texture.pixels, dtype=np.uint8)
        frame = frame.reshape(texture.height, texture.width, 4)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        # Recognize faces
        results = self.engine.recognize_face(frame)
        
        if results:
            self.last_result = results[0]
            self.show_result(results[0])
        else:
            self.clear_result()
    
    def show_result(self, result):
        """Display recognition result"""
        if result['recognized']:
            self.ids.result_card.opacity = 1
            self.ids.welcome_label.text = "WELCOME!"
            self.ids.id_label.text = f"ID: {result['id']}"
            self.ids.name_label.text = result['name']
            self.ids.confidence_label.text = f"Confidence: {result['confidence']:.0%}"
            
            # Set green background
            self.ids.result_card.md_bg_color = (0, 0.7, 0, 0.9)
        else:
            self.ids.result_card.opacity = 1
            self.ids.welcome_label.text = "UNKNOWN"
            self.ids.id_label.text = "Not Recognized"
            self.ids.name_label.text = ""
            self.ids.confidence_label.text = ""
            
            # Set red background
            self.ids.result_card.md_bg_color = (0.8, 0, 0, 0.9)
    
    def clear_result(self):
        """Clear recognition result"""
        self.ids.result_card.opacity = 0
    
    def on_leave(self):
        """Called when leaving screen"""
        self.stop_recognition()


class SettingsScreen(Screen):
    """Settings screen"""
    pass


class FaceRecognitionApp(MDApp):
    """Main application"""
    
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        
        return None
    
    def show_info(self):
        """Show app info dialog"""
        dialog = MDDialog(
            title="Face Recognition System",
            text="Version 1.0\nDeveloped for Student Recognition\n\nPress camera button to start recognition.",
            size_hint=(0.8, None),
            height="200dp"
        )
        dialog.open()


if __name__ == '__main__':
    FaceRecognitionApp().run()
