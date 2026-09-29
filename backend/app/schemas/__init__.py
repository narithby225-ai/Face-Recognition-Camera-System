"""Pydantic schemas for API validation"""

from app.schemas.user import User, UserCreate, UserUpdate, UserInDB
from app.schemas.token import Token, TokenData, TokenRefresh
from app.schemas.student import (
    Student, StudentCreate, StudentUpdate, StudentInDB, 
    StudentList, StudentWithEncodings
)
from app.schemas.attendance import (
    Attendance, AttendanceCreate, AttendanceUpdate, AttendanceInDB,
    AttendanceList, AttendanceStats, AttendanceReport
)

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserInDB",
    "Token", "TokenData", "TokenRefresh",
    "Student", "StudentCreate", "StudentUpdate", "StudentInDB", 
    "StudentList", "StudentWithEncodings",
    "Attendance", "AttendanceCreate", "AttendanceUpdate", "AttendanceInDB",
    "AttendanceList", "AttendanceStats", "AttendanceReport"
]
