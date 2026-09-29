"""
Student Schemas
Pydantic models for student API validation
"""

from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    """Base student schema"""
    student_id: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    gender: Optional[str] = Field(None, pattern="^(male|female|other|ប|ស)$")
    date_of_birth: Optional[date] = None
    notes: Optional[str] = None


class StudentCreate(StudentBase):
    """Schema for creating a student"""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    student_id: Optional[str] = Field(None, min_length=1, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[str] = Field(None, pattern="^(male|female|other|ប|ស)$")
    date_of_birth: Optional[date] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class StudentInDB(StudentBase):
    """Schema for student in database"""
    id: int
    photo_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Student(StudentInDB):
    """Schema for student response"""
    full_name: str
    encoding_count: int = 0


class StudentWithEncodings(Student):
    """Student with face encoding information"""
    has_encodings: bool
    encoding_count: int


class StudentList(BaseModel):
    """Paginated student list response"""
    total: int
    page: int
    page_size: int
    students: List[Student]
