from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from backend.services import employee_service
from datetime import datetime

bp = APIBlueprint('employee', __name__, url_prefix='/employee')


@bp.get('/basic')
@jwt_required()
def employee_basic():
    current_user_id = int(get_jwt_identity())
    data = employee_service.get_employee_basic(current_user_id)
    if not data:
        return {"error": "Employee not found"}, 404
    return data


@bp.get('/team')
@jwt_required()
def employee_team():
    current_user_id = int(get_jwt_identity())
    return {
        "team_id": employee_service.get_team_id(current_user_id),
        "team_name": employee_service.get_team_name(current_user_id),
        "team_leader_id": employee_service.get_team_leader_id(current_user_id),
        "team_leader_name": employee_service.get_team_leader_name(current_user_id),
        "team_members": employee_service.get_team_members(current_user_id),
    }


@bp.get('/attendance/monthly')
@jwt_required()
def employee_monthly_attendance():
    current_user_id = int(get_jwt_identity())
    month = int(request.args.get('month', datetime.utcnow().month))
    year = request.args.get('year')
    year_int = int(year) if year else None
    return employee_service.get_monthly_attendance(current_user_id, month, year_int)


@bp.get('/attendance/day')
@jwt_required()
def employee_day_attendance():
    current_user_id = int(get_jwt_identity())
    date_str = request.args.get('date')
    if not date_str:
        return {"error": "date query param required (YYYY-MM-DD)"}, 400
    day = datetime.strptime(date_str, "%Y-%m-%d").date()
    return employee_service.get_working_time_by_day(current_user_id, day)

