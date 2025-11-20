import datetime
from backend.models import db
from backend.models.attendance import Attendance
from datetime import date, time as dt_time


def check_in(employee_id: int):
    # Check if user already has an active check-in
    existing = Attendance.query.filter_by(
        employee_id=employee_id,
        check_out_time=None
    ).first()

    if existing:
        return {"error": "User already checked in"}, 409

    # Create new attendance record
    now = datetime.datetime.now()
    attendance = Attendance(
        employee_id=employee_id,
        check_in_time=now.time(),
        date=now.date()
    )
    db.session.add(attendance)
    db.session.commit()

    return {"message": "Checked in successfully"}, 200


def check_out(employee_id: int):
    # Find active check-in
    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        check_out_time=None
    ).order_by(Attendance.check_in_time.desc()).first()

    if not attendance:
        return {"error": "No active check-in found"}, 404

    # Update check-out time
    attendance.check_out_time = datetime.datetime.now().time()
    db.session.commit()

    return {"message": "Checked out successfully"}, 200


def elapsed_time(employee_id: int):
    # Find active check-in
    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        check_out_time=None
    ).order_by(Attendance.check_in_time.desc()).first()

    if attendance and attendance.check_in_time:
        # Combine date and time to create datetime for calculation
        check_in_datetime = datetime.datetime.combine(
            attendance.date or date.today(),
            attendance.check_in_time
        )
        now = datetime.datetime.now()
        elapsed = now - check_in_datetime

        hours, rem = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(rem, 60)
        return {"elapsed_time": f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"}, 200
    else:
        return {"elapsed_time": "00:00:00"}, 200


def is_checked_in(employee_id: int):
    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        check_out_time=None
    ).first()

    return {"is_checked_in": attendance is not None}, 200

