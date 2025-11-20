from backend.models.overtime_request import OvertimeRequest
from backend.models.employee import Employee
from backend.models import db
from datetime import date


def create_ot_request(employee_id: int, for_date: date, requested_min: int, description: str | None = None):
    req = OvertimeRequest(
        employee_id=employee_id,
        for_date=for_date,
        requested_minutes=requested_min,
        extra_task_description=description,
    )
    db.session.add(req)
    db.session.commit()
    return {"ot_request_entry": 200, "id": req.id}


def list_ot_to_be_approved_tl(tl_id: int):
    """Return OT requests for employees in the TL's team with status=0 (pending)."""
    # Get TL's team id
    tl = Employee.query.get(tl_id)
    if not tl:
        return {"tl_ot_list": []}
    team_id = tl.primary_team_id
    # Find employees in this team
    employees_in_team = Employee.query.with_entities(Employee.id).filter_by(primary_team_id=team_id).subquery()
    reqs = (
        OvertimeRequest.query
        .filter(OvertimeRequest.status == 0, OvertimeRequest.employee_id.in_(employees_in_team))
        .all()
    )
    return {"tl_ot_list": [r.to_dict() for r in reqs]}


def list_ot_to_be_approved_hr(hr_id: int):
    """Placeholder: currently returns all pending OT requests; can be refined later."""
    reqs = OvertimeRequest.query.filter_by(status=0).all()
    return {"hr_ot_list": [r.to_dict() for r in reqs]}


def approve_ot_tl(tl_id: int, ot_request_id: int):
    req = OvertimeRequest.query.get(ot_request_id)
    if not req:
        return {"error": "OT request not found"}, 404
    # For now, mark status=1 for TL approval
    req.status = 1
    db.session.commit()
    return {"message": "ot_approved_tl"}


def approve_ot_hr(hr_id: int, ot_request_id: int):
    req = OvertimeRequest.query.get(ot_request_id)
    if not req:
        return {"error": "OT request not found"}, 404
    # For now, mark status=2 for HR approval
    req.status = 2
    db.session.commit()
    return {"message": "ot_approved_hr"}

