"""
Face Encoding Model
Stores 128-dimensional face encodings
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class FaceEncoding(Base):
    """Face encoding model for face recognition"""
    
    __tablename__ = "face_encodings"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    encoding = Column(LargeBinary, nullable=False)  # 128-D numpy array stored as bytes
    image_url = Column(String(500))
    quality_score = Column(Float)  # Face quality/confidence score
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    student = relationship("Student", back_populates="face_encodings")
    
    def __repr__(self):
        return f"<FaceEncoding student_id={self.student_id}>"
