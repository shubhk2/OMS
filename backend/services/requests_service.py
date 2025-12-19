# python
from sqlalchemy import extract
from backend.models import db
from backend.models.leave_request import LeaveRequest
from backend.models.overtime_request import OvertimeRequest
from backend.models.wfh_request import WFHRequest

def create_leave_request(data: dict, user_id: int):
    req = LeaveRequest(employee_id=user_id, **data)
    db.session.add(req)
    db.session.commit()
    return req

def list_leave_requests(month: int, year: int, user_id: int):
    rows = LeaveRequest.query.filter(
        LeaveRequest.employee_id == user_id,
        extract('month', LeaveRequest.from_date) == month,
        extract('year', LeaveRequest.from_date) == year,
    ).all()
    return rows

def create_ot_request(data: dict, user_id: int):
    req = OvertimeRequest(employee_id=user_id, **data)
    db.session.add(req)
    db.session.commit()
    return req

def list_ot_requests(month: int, year: int, user_id: int):
    rows = OvertimeRequest.query.filter(
        OvertimeRequest.employee_id == user_id,
        extract('month', OvertimeRequest.for_date) == month,
        extract('year', OvertimeRequest.for_date) == year,
    ).all()
    return rows

def create_wfh_request(data: dict, user_id: int):
    req = WFHRequest(employee_id=user_id, **data)
    db.session.add(req)
    db.session.commit()
    return req

def list_wfh_requests(month: int, year: int, user_id: int):
    rows = WFHRequest.query.filter(
        WFHRequest.employee_id == user_id,
        extract('month', WFHRequest.from_date) == month,
        extract('year', WFHRequest.from_date) == year,
    ).all()
    return rows
