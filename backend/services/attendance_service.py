import datetime
from backend.models import db
from backend.models.attendance import Attendance
from datetime import date


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

    # If user is on break, finalize break duration by pairing last start with now
    if attendance.break_start_times and (not attendance.break_end_times or len(attendance.break_start_times) > len(attendance.break_end_times)):
        # last start time
        last_start = attendance.break_start_times[-1]
        now_time = datetime.datetime.now().time()
        # append end time
        attendance.break_end_times = (attendance.break_end_times or []) + [now_time]
        # compute delta in seconds between last_start and now_time
        # last_start and now_time are time objects (no date). We'll compute using today date.
        start_dt = datetime.datetime.combine(datetime.date.today(), last_start)
        end_dt = datetime.datetime.combine(datetime.date.today(), now_time)
        if end_dt < start_dt:
            # if end passed midnight, add a day
            end_dt += datetime.timedelta(days=1)
        delta = end_dt - start_dt
        attendance.total_break_time = (attendance.total_break_time or 0) + int(delta.total_seconds())

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

        # Subtract total break seconds stored in total_break_time
        total_break = attendance.total_break_time or 0
        # If a break is ongoing (more starts than ends), add current break duration
        if attendance.break_start_times and (not attendance.break_end_times or len(attendance.break_start_times) > len(attendance.break_end_times)):
            last_start = attendance.break_start_times[-1]
            start_dt = datetime.datetime.combine(datetime.date.today(), last_start)
            now_dt = now
            if now_dt < start_dt:
                now_dt += datetime.timedelta(days=1)
            total_break += int((now_dt - start_dt).total_seconds())

        elapsed_seconds = int(elapsed.total_seconds()) - int(total_break)
        if elapsed_seconds < 0:
            elapsed_seconds = 0

        hours, rem = divmod(elapsed_seconds, 3600)
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


def is_on_break(employee_id: int):
    # Returns whether the current active attendance row is on break (unpaired start exists)
    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        check_out_time=None
    ).first()

    if not attendance:
        return {"on_break": False}, 200

    on_break = False
    if attendance.break_start_times and (not attendance.break_end_times or len(attendance.break_start_times) > len(attendance.break_end_times)):
        on_break = True
    return {"on_break": on_break}, 200


def break_toggle(employee_id: int):
    # Toggle break: start a break by appending start time, end by appending end time and adding to total
    attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        check_out_time=None
    ).order_by(Attendance.check_in_time.desc()).first()

    if not attendance:
        return {"error": "No active check-in found"}, 404

    now_time = datetime.datetime.now().time()

    # Determine if currently on break
    on_break = attendance.break_start_times and (not attendance.break_end_times or len(attendance.break_start_times) > len(attendance.break_end_times))

    if on_break:
        # End break: append end time and compute delta with last start
        attendance.break_end_times = (attendance.break_end_times or []) + [now_time]
        last_start = attendance.break_start_times[-1]
        start_dt = datetime.datetime.combine(datetime.date.today(), last_start)
        end_dt = datetime.datetime.combine(datetime.date.today(), now_time)
        if end_dt < start_dt:
            end_dt += datetime.timedelta(days=1)
        delta = end_dt - start_dt
        attendance.total_break_time = (attendance.total_break_time or 0) + int(delta.total_seconds())
        db.session.commit()
        return {"message": "Break ended"}, 200
    else:
        # Start break: append start time
        attendance.break_start_times = (attendance.break_start_times or []) + [now_time]
        db.session.commit()
        return {"message": "Break started"}, 200
