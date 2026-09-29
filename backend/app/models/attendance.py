"""
Attendance Model
Tracks student attendance records
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Attendance(Base):
    """Attendance model for tracking student attendance"""
    
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time_in = Column(DateTime(timezone=True))
    time_out = Column(DateTime(timezone=True))
    status = Column(String(20), default="present")  # present, absent, late, excused
    confidence = Column(Float)  # Face recognition confidence
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    student = relationship("Student", back_populates="attendance_records")
    
    # Unique constraint: one attendance record per student per day
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='unique_student_date'),
    )
    
    def __repr__(self):
        return f"<Attendance student_id={self.student_id} date={self.date} status={self.status}>"
