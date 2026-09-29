"""
Students API Endpoints
CRUD operations for student management
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.face_encoding import FaceEncoding
from app.schemas.student import (
    Student as StudentSchema,
    StudentCreate,
    StudentUpdate,
    StudentList,
    StudentWithEncodings
)


router = APIRouter()


@router.get("/", response_model=StudentList)
async def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Any:
    """
    Get list of students with pagination and search
    """
    query = db.query(Student)
    
    # Filter by active status
    if is_active is not None:
        query = query.filter(Student.is_active == is_active)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                Student.student_id.ilike(f"%{search}%"),
                Student.first_name.ilike(f"%{search}%"),
                Student.last_name.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Pagination
    students = query.offset(skip).limit(limit).all()
    
    # Add encoding count and full name
    students_data = []
    for student in students:
        student_dict = {
            **student.__dict__,
            "full_name": student.full_name,
            "encoding_count": len(student.face_encodings)
        }
        students_data.append(student_dict)
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "students": students_data
    }


@router.post("/", response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new student
    """
    # Check if student_id already exists
    existing = db.query(Student).filter(Student.student_id == student_in.student_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already exists"
        )
    
    # Create student
    student = Student(**student_in.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return {
        **student.__dict__,
        "full_name": student.full_name,
        "encoding_count": 0
    }


@router.get("/{student_id}", response_model=StudentWithEncodings)
async def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get student by ID with face encoding info
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    encoding_count = len(student.face_encodings)
    
    return {
        **student.__dict__,
        "full_name": student.full_name,
        "encoding_count": encoding_count,
        "has_encodings": encoding_count > 0
    }


@router.put("/{student_id}", response_model=StudentSchema)
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update student information
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if new student_id conflicts
    if student_in.student_id and student_in.student_id != student.student_id:
        existing = db.query(Student).filter(
            Student.student_id == student_in.student_id,
            Student.id != student_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student ID already exists"
            )
    
    # Update fields
    update_data = student_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    return {
        **student.__dict__,
        "full_name": student.full_name,
        "encoding_count": len(student.face_encodings)
    }


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete student (cascade deletes face encodings and attendance)
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()


@router.get("/search/", response_model=List[StudentSchema])
async def search_students(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=100)
) -> Any:
    """
    Search students by student_id, first_name, or last_name
    """
    students = db.query(Student).filter(
        or_(
            Student.student_id.ilike(f"%{query}%"),
            Student.first_name.ilike(f"%{query}%"),
            Student.last_name.ilike(f"%{query}%")
        )
    ).limit(limit).all()
    
    return [
        {
            **student.__dict__,
            "full_name": student.full_name,
            "encoding_count": len(student.face_encodings)
        }
        for student in students
    ]
