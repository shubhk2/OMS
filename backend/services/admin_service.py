from __future__ import annotations

from datetime import date

from sqlalchemy import func

from backend.models import db
from backend.models.employee import Employee
from backend.models.team import Team
from backend.models.attendance import Attendance
from backend.models.leave_request import LeaveRequest
from backend.models.overtime_request import OvertimeRequest
from backend.models.wfh_request import WFHRequest


ADMIN_ROLE_ID = 14
HR_ROLE_IDS = {11, 12}
TL_ROLE_ID = 8


def _require_admin(current_user: Employee | None):
    if not current_user or current_user.role != ADMIN_ROLE_ID:
        return {"error": "Forbidden (admin only)"}, 403
    return None


def get_admin_home_snapshot(admin_id: int):
    """Admin dashboard data for the Home page.

    Returns:
      - last_checked_in: last 4 check-ins today (with status: checked-in / break)
      - indicators: checked_in_count, total_employees, on_leave_today, on_wfh_today
      - quick_stats: total_employees, active_teams, team_leaders, hr_members
      - alerts: pending OT/leaves, missed checkouts, teams without leader
    """

    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    today = date.today()

    total_employees = db.session.query(func.count(Employee.id)).scalar() or 0

    active_teams = db.session.query(func.count(Team.id)).filter(Team.status == 1).scalar() or 0
    team_leaders = db.session.query(func.count(Employee.id)).filter(Employee.role == TL_ROLE_ID).scalar() or 0
    hr_members = db.session.query(func.count(Employee.id)).filter(Employee.role.in_(HR_ROLE_IDS)).scalar() or 0

    checked_in_count = (
        Attendance.query.filter(Attendance.date == today, Attendance.check_out_time.is_(None)).count()
    )

    # Determine leave/wfh today: any request overlapping today with approved status (=1)
    on_leave_today = (
        LeaveRequest.query.filter(
            LeaveRequest.status == 1,
            LeaveRequest.from_date <= today,
            LeaveRequest.to_date >= today,
        ).count()
    )

    on_wfh_today = (
        WFHRequest.query.filter(
            WFHRequest.status == 1,
            WFHRequest.from_date <= today,
            WFHRequest.to_date >= today,
        ).count()
    )

    # Last 4 active check-ins today
    active_today = (
        Attendance.query.filter(Attendance.date == today, Attendance.check_out_time.is_(None))
        .order_by(Attendance.check_in_time.desc())
        .limit(4)
        .all()
    )

    # Enrich with employee + team names
    employee_ids = [a.employee_id for a in active_today]
    employees = Employee.query.filter(Employee.id.in_(employee_ids)).all() if employee_ids else []
    emp_by_id = {e.id: e for e in employees}

    # Teams lookup
    team_ids = list({e.primary_team_id for e in employees if e.primary_team_id is not None})
    teams = Team.query.filter(Team.id.in_(team_ids)).all() if team_ids else []
    team_by_id = {t.id: t for t in teams}

    def is_on_break(att: Attendance) -> bool:
        # unpaired start exists
        return bool(att.break_start_times) and (
            not att.break_end_times or len(att.break_start_times) > len(att.break_end_times)
        )

    last_checked_in = []
    for att in active_today:
        emp = emp_by_id.get(att.employee_id)
        team = team_by_id.get(emp.primary_team_id) if emp else None
        last_checked_in.append(
            {
                "employee": emp.name if emp else f"#{att.employee_id}",
                "team": team.name if team else "-",
                "check_in_time": att.check_in_time.strftime("%H:%M"),
                "status": "Break" if is_on_break(att) else "Checked in",
            }
        )

    pending_ot_approvals = OvertimeRequest.query.filter(OvertimeRequest.status == 0).count()
    pending_leave_requests = LeaveRequest.query.filter(LeaveRequest.status == 0).count()

    # simple heuristic: yesterday attendance rows with missing checkout
    missed_checkout = (
        Attendance.query.filter(
            Attendance.date < today,
            Attendance.check_out_time.is_(None),
        ).count()
    )

    teams_without_leader = Team.query.filter(Team.team_leader_id.is_(None)).count()

    return {
        "last_checked_in": last_checked_in,
        "indicators": {
            "checked_in": checked_in_count,
            "total": total_employees,
            "on_leave_today": on_leave_today,
            "on_wfh_today": on_wfh_today,
        },
        "quick_stats": {
            "total_employees": total_employees,
            "active_teams": active_teams,
            "team_leaders": team_leaders,
            "hr_members": hr_members,
        },
        "alerts": {
            "pending_ot_approvals": pending_ot_approvals,
            "pending_leave_requests": pending_leave_requests,
            "missed_check_out": missed_checkout,
            "teams_without_leader": teams_without_leader,
        },
    }, 200


def create_employee(admin_id: int, payload: dict):
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    username = (payload.get("username") or email or name).strip()
    role = int(payload.get("role") or 1)
    specialization = payload.get("specialization")
    primary_team_id = payload.get("primary_team_id")
    password="shubh123"
    if not name or not username:
        return {"error": "name and username are required"}, 400

    # unique username check (index exists; but we still validate)
    if Employee.query.filter(Employee.username == username).first():
        return {"error": "username already exists"}, 409

    emp = Employee(
        name=name,
        username=username,
        email=email or None,
        role=role,
        specialization=int(specialization) if specialization is not None else None,
        primary_team_id=int(primary_team_id) if primary_team_id is not None else None,
        status=1,
        password=password,
    )
    db.session.add(emp)
    db.session.commit()
    return {"employee": emp.to_dict()}, 201


def create_team(admin_id: int, payload: dict):
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    name = (payload.get("name") or "").strip()
    team_leader_id = payload.get("team_leader_id")

    if not name or not team_leader_id:
        return {"error": "name and team_leader_id are required"}, 400

    leader = Employee.query.get(int(team_leader_id))
    if not leader:
        return {"error": "team leader not found"}, 404

    team = Team(name=name, team_leader_id=leader.id, status=1)
    db.session.add(team)
    db.session.flush()

    # ensure leader is TL role and assign primary team
    leader.role = TL_ROLE_ID
    leader.primary_team_id = team.id

    db.session.commit()

    return {"team": team.to_dict()}, 201


def assign_role_and_team(admin_id: int, payload: dict):
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    employee_id = payload.get("employee_id")
    role = payload.get("role")
    primary_team_id = payload.get("primary_team_id")

    if employee_id is None:
        return {"error": "employee_id is required"}, 400

    emp = Employee.query.get(int(employee_id))
    if not emp:
        return {"error": "employee not found"}, 404

    if role is not None:
        emp.role = int(role)

    if primary_team_id is not None:
        team = Team.query.get(int(primary_team_id))
        if not team:
            return {"error": "team not found"}, 404
        emp.primary_team_id = team.id

    db.session.commit()
    return {"employee": emp.to_dict()}, 200


def list_employees_basic(admin_id: int):
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    emps = Employee.query.order_by(Employee.id.asc()).all()
    return {
        "employees": [
            {
                "id": e.id,
                "name": e.name,
                "username": e.username,
                "role": e.role,
                "primary_team_id": e.primary_team_id,
            }
            for e in emps
        ]
    }, 200


def list_teams_basic(admin_id: int):
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    teams = Team.query.order_by(Team.id.asc()).all()
    return {"teams": [t.to_dict() for t in teams]}, 200


def get_attendance_list(admin_id: int, params: dict):
    """Return attendance rows filtered by params for admin UI.
    Params keys: date (YYYY-MM-DD), month (1-12), year (YYYY), team_id, employee_id
    """
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    from sqlalchemy import extract

    q = Attendance.query

    # join with Employee to filter by team or get name
    q = q.join(Employee, Attendance.employee_id == Employee.id)

    if params.get('date'):
        try:
            d = date.fromisoformat(params['date'])
            q = q.filter(Attendance.date == d)
        except Exception:
            return {"error": "invalid date format"}, 400

    if params.get('month'):
        try:
            m = int(params['month'])
            q = q.filter(extract('month', Attendance.date) == m)
        except Exception:
            return {"error": "invalid month"}, 400

    if params.get('year'):
        try:
            y = int(params['year'])
            q = q.filter(extract('year', Attendance.date) == y)
        except Exception:
            return {"error": "invalid year"}, 400

    if params.get('team_id'):
        try:
            t = int(params['team_id'])
            q = q.filter(Employee.primary_team_id == t)
        except Exception:
            return {"error": "invalid team_id"}, 400

    # Support employee_name lookup (admin UI can pass name and we resolve it here)
    if params.get('employee_name') and not params.get('employee_id'):
        name_q = (params['employee_name'] or '').strip()
        if name_q:
            # try exact username first then case-insensitive name
            emp = Employee.query.filter(Employee.username == name_q).first()
            if not emp:
                emp = Employee.query.filter(func.lower(Employee.name) == name_q.lower()).first()
            if not emp:
                return {"error": "employee not found for given name"}, 404
            params['employee_id'] = emp.id

    if params.get('employee_id'):
        try:
            e = int(params['employee_id'])
            q = q.filter(Attendance.employee_id == e)
        except Exception:
            return {"error": "invalid employee_id"}, 400

    rows = q.order_by(Attendance.date.desc(), Attendance.check_in_time.desc()).limit(500).all()

    # Enrich rows
    employee_ids = [r.employee_id for r in rows]
    employees = Employee.query.filter(Employee.id.in_(employee_ids)).all() if employee_ids else []
    emp_by_id = {e.id: e for e in employees}

    def status_of(r: Attendance):
        if r.check_out_time is None:
            if r.break_start_times and (not r.break_end_times or len(r.break_start_times) > len(r.break_end_times)):
                return 'Break'
            return 'Checked in'
        return 'Checked out'

    out = []
    for r in rows:
        e = emp_by_id.get(r.employee_id)
        out.append({
            'employee_id': r.employee_id,
            'employee_name': e.name if e else f'#${r.employee_id}',
            'team_id': e.primary_team_id if e else None,
            'check_in_time': r.check_in_time.strftime('%H:%M:%S') if r.check_in_time else None,
            'check_out_time': r.check_out_time.strftime('%H:%M:%S') if r.check_out_time else None,
            'date': r.date.isoformat() if r.date else None,
            'status': status_of(r),
            'total_break_seconds': r.total_break_time or 0,
            'overtime_minutes': r.overtime_minutes or 0,
        })

    return {'attendance': out}, 200


def get_attendance_summary(admin_id: int, params: dict):
    """Return simple summary counts for a given month/year: total present days, avg check-in time, missed checkouts count."""
    admin = Employee.query.get(admin_id)
    deny = _require_admin(admin)
    if deny:
        return deny

    from sqlalchemy import extract, func

    q = Attendance.query

    if params.get('month'):
        try:
            m = int(params['month'])
            q = q.filter(extract('month', Attendance.date) == m)
        except Exception:
            return {"error": "invalid month"}, 400

    if params.get('year'):
        try:
            y = int(params['year'])
            q = q.filter(extract('year', Attendance.date) == y)
        except Exception:
            return {"error": "invalid year"}, 400

    total_records = q.count()
    checked_in_count = q.filter(Attendance.check_out_time.is_(None)).count()
    missed_checkout = q.filter(Attendance.date < date.today(), Attendance.check_out_time.is_(None)).count()

    # Average check-in time in seconds (approx)
    # For Postgres TIME column use date_part('epoch', check_in_time) to get seconds since midnight
    try:
        times = q.with_entities(func.avg(func.date_part('epoch', Attendance.check_in_time))).scalar()
    except Exception:
        # Fallback: None (some backends may not support date_part over TIME)
        times = None

    avg_checkin = None
    if times:
        try:
            total_seconds = int(times)
            h, rem = divmod(total_seconds, 3600)
            m, s = divmod(rem, 60)
            avg_checkin = f"{int(h):02}:{int(m):02}:{int(s):02}"
        except Exception:
            avg_checkin = None

    return {
        'total_records': total_records,
        'checked_in_now': checked_in_count,
        'missed_checkout': missed_checkout,
        'avg_checkin_time': avg_checkin,
    }, 200
