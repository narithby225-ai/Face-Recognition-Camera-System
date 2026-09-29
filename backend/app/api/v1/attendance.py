"""
Attendance API Endpoints
Track and manage student attendance
"""

from typing import Any, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.attendance import Attendance
from app.schemas.attendance import (
    Attendance as AttendanceSchema,
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceList,
    AttendanceStats,
    AttendanceReport
)


router = APIRouter()


@router.get("/", response_model=AttendanceList)
async def get_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    student_id: Optional[int] = None,
    status: Optional[str] = None
) -> Any:
    """
    Get attendance records with filters
    """
    query = db.query(Attendance).join(Student)
    
    # Date range filter
    if date_from:
        query = query.filter(Attendance.date >= date_from)
    if date_to:
        query = query.filter(Attendance.date <= date_to)
    
    # Student filter
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    
    # Status filter
    if status:
        query = query.filter(Attendance.status == status)
    
    # Order by date descending
    query = query.order_by(Attendance.date.desc(), Attendance.time_in.desc())
    
    total = query.count()
    records = query.offset(skip).limit(limit).all()
    
    # Add student names
    records_data = []
    for record in records:
        records_data.append({
            **record.__dict__,
            "student_name": record.student.full_name
        })
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "records": records_data
    }


@router.post("/mark", response_model=AttendanceSchema, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    attendance_in: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Mark student attendance (usually called automatically by recognition system)
    """
    # Check if student exists
    student = db.query(Student).filter(Student.id == attendance_in.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if attendance already exists for this date
    existing = db.query(Attendance).filter(
        and_(
            Attendance.student_id == attendance_in.student_id,
            Attendance.date == attendance_in.date
        )
    ).first()
    
    if existing:
        # Update existing record
        if attendance_in.time_in:
            existing.time_in = attendance_in.time_in
        if attendance_in.confidence:
            existing.confidence = attendance_in.confidence
        if attendance_in.notes:
            existing.notes = attendance_in.notes
        existing.status = attendance_in.status
        
        db.commit()
        db.refresh(existing)
        return {**existing.__dict__, "student_name": student.full_name}
    
    # Create new attendance record
    attendance = Attendance(**attendance_in.dict())
    if not attendance.time_in:
        attendance.time_in = datetime.now()
    
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    return {**attendance.__dict__, "student_name": student.full_name}


@router.get("/stats", response_model=AttendanceStats)
async def get_attendance_stats(
    target_date: date = Query(default_factory=date.today),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get attendance statistics for a specific date
    """
    # Get total active students
    total_students = db.query(Student).filter(Student.is_active == True).count()
    
    # Get attendance counts by status
    stats = db.query(
        Attendance.status,
        func.count(Attendance.id)
    ).filter(
        Attendance.date == target_date
    ).group_by(Attendance.status).all()
    
    status_counts = {status: count for status, count in stats}
    
    present_count = status_counts.get("present", 0)
    absent_count = total_students - sum(status_counts.values())
    late_count = status_counts.get("late", 0)
    excused_count = status_counts.get("excused", 0)
    
    attendance_rate = (present_count / total_students * 100) if total_students > 0 else 0
    
    return {
        "total_students": total_students,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "excused_count": excused_count,
        "attendance_rate": round(attendance_rate, 2),
        "date": target_date
    }


@router.get("/report", response_model=AttendanceReport)
async def get_attendance_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate attendance report for date range
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be after start_date"
        )
    
    total_days = (end_date - start_date).days + 1
    
    # Get stats for each day
    daily_stats = []
    current_date = start_date
    
    while current_date <= end_date:
        stats = await get_attendance_stats(current_date, db, current_user)
        daily_stats.append(stats)
        current_date += timedelta(days=1)
    
    # Get student summaries
    students = db.query(Student).filter(Student.is_active == True).all()
    student_summaries = []
    
    for student in students:
        records = db.query(Attendance).filter(
            and_(
                Attendance.student_id == student.id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        ).all()
        
        present_days = sum(1 for r in records if r.status == "present")
        late_days = sum(1 for r in records if r.status == "late")
        excused_days = sum(1 for r in records if r.status == "excused")
        absent_days = total_days - len(records)
        
        student_summaries.append({
            "student_id": student.student_id,
            "student_name": student.full_name,
            "present_days": present_days,
            "late_days": late_days,
            "excused_days": excused_days,
            "absent_days": absent_days,
            "attendance_rate": round((present_days / total_days * 100) if total_days > 0 else 0, 2)
        })
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_days": total_days,
        "stats": daily_stats,
        "student_summaries": student_summaries
    }


@router.get("/student/{student_id}", response_model=list)
async def get_student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None
) -> Any:
    """
    Get attendance history for a specific student
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    query = db.query(Attendance).filter(Attendance.student_id == student_id)
    
    if date_from:
        query = query.filter(Attendance.date >= date_from)
    if date_to:
        query = query.filter(Attendance.date <= date_to)
    
    records = query.order_by(Attendance.date.desc()).all()
    
    return [
        {**record.__dict__, "student_name": student.full_name}
        for record in records
    ]
