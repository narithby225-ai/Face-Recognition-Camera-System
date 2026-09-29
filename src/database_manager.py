"""
Database Manager for Face Recognition System
Handles all database operations including person registration and face encoding storage.
"""

import sqlite3
import json
import pickle
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict
import numpy as np


class DatabaseManager:
    """Manages SQLite database for storing person information and face encodings."""
    
    def __init__(self, db_path: str = "data/database/faces.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_directory_exists()
        self._initialize_database()
    
    def _ensure_directory_exists(self):
        """Create database directory if it doesn't exist."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create persons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                registration_date TEXT NOT NULL,
                last_seen TEXT,
                notes TEXT
            )
        ''')
        
        # Create face_encodings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_encodings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                encoding BLOB NOT NULL,
                image_path TEXT,
                created_date TEXT NOT NULL,
                FOREIGN KEY (person_id) REFERENCES persons (id)
            )
        ''')
        
        # Create recognition_logs table (optional tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recognition_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                confidence REAL,
                FOREIGN KEY (person_id) REFERENCES persons (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_person(self, name: str, encodings: List[np.ndarray], 
                       image_paths: Optional[List[str]] = None,
                       notes: str = "") -> int:
        """
        Register a new person with their face encodings.
        
        Args:
            name: Person's name
            encodings: List of face encodings (128-d vectors)
            image_paths: Optional paths to face images
            notes: Additional notes about the person
            
        Returns:
            person_id: Assigned unique ID for the person
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert person
        cursor.execute('''
            INSERT INTO persons (name, registration_date, notes)
            VALUES (?, ?, ?)
        ''', (name, datetime.now().isoformat(), notes))
        
        person_id = cursor.lastrowid
        
        # Insert face encodings
        if image_paths is None:
            image_paths = [None] * len(encodings)
        
        for encoding, image_path in zip(encodings, image_paths):
            encoding_blob = pickle.dumps(encoding)
            cursor.execute('''
                INSERT INTO face_encodings (person_id, encoding, image_path, created_date)
                VALUES (?, ?, ?, ?)
            ''', (person_id, encoding_blob, image_path, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Registered: {name} (ID: {person_id}) with {len(encodings)} face encoding(s)")
        return person_id
    
    def get_all_encodings(self) -> Tuple[List[np.ndarray], List[int], List[str]]:
        """
        Get all face encodings from database.
        
        Returns:
            Tuple of (encodings, person_ids, names)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT fe.encoding, fe.person_id, p.name
            FROM face_encodings fe
            JOIN persons p ON fe.person_id = p.id
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return [], [], []
        
        encodings = [pickle.loads(row[0]) for row in results]
        person_ids = [row[1] for row in results]
        names = [row[2] for row in results]
        
        return encodings, person_ids, names
    
    def get_person_by_id(self, person_id: int) -> Optional[Dict]:
        """
        Get person information by ID.
        
        Args:
            person_id: Person's unique ID
            
        Returns:
            Dictionary with person information or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, registration_date, last_seen, notes
            FROM persons
            WHERE id = ?
        ''', (person_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'registration_date': result[2],
                'last_seen': result[3],
                'notes': result[4]
            }
        return None
    
    def get_all_persons(self) -> List[Dict]:
        """
        Get all registered persons.
        
        Returns:
            List of dictionaries with person information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, registration_date, last_seen, notes
            FROM persons
            ORDER BY id
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        persons = []
        for row in results:
            persons.append({
                'id': row[0],
                'name': row[1],
                'registration_date': row[2],
                'last_seen': row[3],
                'notes': row[4]
            })
        
        return persons
    
    def update_last_seen(self, person_id: int):
        """
        Update the last seen timestamp for a person.
        
        Args:
            person_id: Person's unique ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE persons
            SET last_seen = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), person_id))
        
        conn.commit()
        conn.close()
    
    def log_recognition(self, person_id: int, confidence: float):
        """
        Log a recognition event.
        
        Args:
            person_id: Person's unique ID
            confidence: Recognition confidence score
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recognition_logs (person_id, timestamp, confidence)
            VALUES (?, ?, ?)
        ''', (person_id, datetime.now().isoformat(), confidence))
        
        conn.commit()
        conn.close()
    
    def delete_person(self, person_id: int) -> bool:
        """
        Delete a person and all associated encodings.
        
        Args:
            person_id: Person's unique ID
            
        Returns:
            True if deleted, False if person not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if person exists
        cursor.execute('SELECT id FROM persons WHERE id = ?', (person_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Delete encodings
        cursor.execute('DELETE FROM face_encodings WHERE person_id = ?', (person_id,))
        
        # Delete recognition logs
        cursor.execute('DELETE FROM recognition_logs WHERE person_id = ?', (person_id,))
        
        # Delete person
        cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Deleted person ID: {person_id}")
        return True
    
    def get_person_count(self) -> int:
        """
        Get total number of registered persons.
        
        Returns:
            Number of registered persons
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM persons')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def person_exists(self, name: str) -> bool:
        """
        Check if a person with given name exists.
        
        Args:
            name: Person's name
            
        Returns:
            True if person exists, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM persons WHERE name = ?', (name,))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None
