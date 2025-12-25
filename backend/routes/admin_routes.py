from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from backend.services import admin_service
import logging
logger = logging.getLogger(__name__)


bp = APIBlueprint('admin', __name__, url_prefix='/admin')


@bp.get('/home')
@jwt_required()
@bp.doc(security='BearerAuth', summary='Admin home snapshot', description='Returns dashboard snapshot data for admin home page.')
def admin_home():
    admin_id = int(get_jwt_identity())
    body, status = admin_service.get_admin_home_snapshot(admin_id)
    return body, status


@bp.get('/employees')
@jwt_required()
@bp.doc(security='BearerAuth', summary='List employees (basic)', description='Admin-only employee list used for dropdowns.')
def employees_basic():
    admin_id = int(get_jwt_identity())
    body, status = admin_service.list_employees_basic(admin_id)
    return body, status


@bp.get('/teams')
@jwt_required()
@bp.doc(security='BearerAuth', summary='List teams (basic)', description='Admin-only team list used for dropdowns.')
def teams_basic():
    admin_id = int(get_jwt_identity())
    body, status = admin_service.list_teams_basic(admin_id)
    return body, status


@bp.post('/employees')
@jwt_required()
@bp.doc(security='BearerAuth', summary='Create employee', description='Admin-only: create a new employee (login enabled after admin adds them).')
def create_employee():
    admin_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    body, status = admin_service.create_employee(admin_id, payload)
    return body, status


@bp.post('/teams')
@jwt_required()
@bp.doc(security='BearerAuth', summary='Create team', description='Admin-only: create a new team with a mandatory team leader.')
def create_team():
    admin_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    body, status = admin_service.create_team(admin_id, payload)
    return body, status


@bp.post('/assign')
@jwt_required()
@bp.doc(security='BearerAuth', summary='Assign role/team', description='Admin-only: assign/change role and/or primary team for an employee.')
def assign_role_team():
    admin_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    body, status = admin_service.assign_role_and_team(admin_id, payload)
    return body, status


# New: admin attendance list & summary endpoints
@bp.get('/attendance/list')
@jwt_required()
@bp.doc(security='BearerAuth', summary='Filtered attendance list', description='Returns attendance rows filtered by date/month/year/team/employee')
def admin_attendance_list():
    admin_id = int(get_jwt_identity())
    # Query params: date (YYYY-MM-DD), month (1-12), year (YYYY), team_id, employee_id
    q = request.args
    params = {
        'date': q.get('date'),
        'month': q.get('month'),
        'year': q.get('year'),
        'team_id': q.get('team_id'),
        'employee_id': q.get('employee_id'),
        'employee_name': q.get('employee_name')
    }
    body, status = admin_service.get_attendance_list(admin_id, params)
    logger.info(body)
    return body, status


@bp.get('/attendance/summary')
@jwt_required()
@bp.doc(security='BearerAuth', summary='Attendance summary', description='Returns monthly/yearly attendance summaries')
def admin_attendance_summary():
    admin_id = int(get_jwt_identity())
    q = request.args
    params = {'month': q.get('month'), 'year': q.get('year')}
    body, status = admin_service.get_attendance_summary(admin_id, params)
    return body, status


# Routes package
