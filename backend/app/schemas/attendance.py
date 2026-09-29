"""
Attendance Schemas
Pydantic models for attendance API validation
"""

from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field


class AttendanceBase(BaseModel):
    """Base attendance schema"""
    student_id: int
    date: date
    status: str = Field(default="present", pattern="^(present|absent|late|excused)$")


class AttendanceCreate(AttendanceBase):
    """Schema for creating attendance record"""
    time_in: Optional[datetime] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)
    notes: Optional[str] = Field(None, max_length=500)


class AttendanceUpdate(BaseModel):
    """Schema for updating attendance"""
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(present|absent|late|excused)$")
    notes: Optional[str] = Field(None, max_length=500)


class AttendanceInDB(AttendanceBase):
    """Schema for attendance in database"""
    id: int
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    confidence: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class Attendance(AttendanceInDB):
    """Schema for attendance response"""
    student_name: Optional[str] = None


class AttendanceList(BaseModel):
    """Paginated attendance list response"""
    total: int
    page: int
    page_size: int
    records: List[Attendance]


class AttendanceStats(BaseModel):
    """Attendance statistics"""
    total_students: int
    present_count: int
    absent_count: int
    late_count: int
    excused_count: int
    attendance_rate: float
    date: date


class AttendanceReport(BaseModel):
    """Attendance report for date range"""
    start_date: date
    end_date: date
    total_days: int
    stats: List[AttendanceStats]
    student_summaries: List[dict]
