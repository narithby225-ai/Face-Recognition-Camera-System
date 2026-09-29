"""
Student Model
Stores student information
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Student(Base):
    """Student model"""
    
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    photo_url = Column(String(500))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    face_encodings = relationship("FaceEncoding", back_populates="student", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        """Get student's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<Student {self.student_id}: {self.full_name}>"
