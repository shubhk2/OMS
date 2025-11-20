from backend.models.employee import Employee
from backend.models.attendance import Attendance
from backend.models.overtime_request import OvertimeRequest
from backend.models import db
from datetime import date


def get_employee_basic(e_id: int):
    emp = Employee.query.get(e_id)
    if not emp:
        return None
    return {
        "id": emp.id,
        "name": emp.name,
        "email": emp.email,
    }


def get_team_id(e_id: int):
    emp = Employee.query.get(e_id)
    return emp.primary_team_id if emp else None


def get_team_name(e_id: int):
    from sqlalchemy import text
    team_id = get_team_id(e_id)
    if team_id is None:
        return None
    # We don't have a Team model yet; use lightweight SQL for now
    row = db.session.execute(text("SELECT name FROM team WHERE id = :tid"), {"tid": team_id}).fetchone()
    return row[0] if row else None


def get_team_leader_id(e_id: int):
    from sqlalchemy import text
    team_id = get_team_id(e_id)
    if team_id is None:
        return None
    row = db.session.execute(text("SELECT team_leader_id FROM team WHERE id = :tid"), {"tid": team_id}).fetchone()
    return row[0] if row else None


def get_team_leader_name(e_id: int):
    leader_id = get_team_leader_id(e_id)
    if leader_id is None:
        return None
    leader = Employee.query.get(leader_id)
    return leader.name if leader else None


def get_team_members(e_id: int):
    team_id = get_team_id(e_id)
    if team_id is None:
        return []
    members = Employee.query.filter_by(primary_team_id=team_id).all()
    return [m.name for m in members]


def get_monthly_attendance(employee_id: int, month: int, year: int | None = None):
    if year is None:
        year = date.today().year
    count = (
        db.session.query(Attendance)
        .filter(
            Attendance.employee_id == employee_id,
            db.extract('year', Attendance.date) == year,
            db.extract('month', Attendance.date) == month,
        )
        .count()
    )
    return {"monthly_attendance": count}


def get_working_time_by_day(employee_id: int, day: date):
    rec = (
        db.session.query(Attendance)
        .filter_by(employee_id=employee_id, date=day)
        .order_by(Attendance.check_in_time.asc())
        .first()
    )
    if not rec or not rec.check_in_time or not rec.check_out_time:
        return {"work_time": "00:00:00"}
    from datetime import datetime as dt
    start = dt.combine(rec.date, rec.check_in_time)
    end = dt.combine(rec.date, rec.check_out_time)
    delta = end - start
    total_seconds = int(delta.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return {"work_time": f"{hours:02}:{minutes:02}:{seconds:02}"}