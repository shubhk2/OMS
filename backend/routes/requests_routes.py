# python
from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.schemas import (
    LeaveRequestIn, LeaveRequestOut,
    OTRequestIn, OTRequestOut,
    WFHRequestIn, WFHRequestOut,
    MonthlyStatusQuery
)
from backend.services import requests_service as rs

requests_bp = APIBlueprint('requests', __name__, url_prefix='/requests')

# Leave create
@requests_bp.post('/leave')
@requests_bp.input(LeaveRequestIn, arg_name='data')
@requests_bp.output(LeaveRequestOut, status_code=201)
@jwt_required()
def create_leave_request(data):
    user_id = int(get_jwt_identity())
    new_req = rs.create_leave_request(data, user_id)
    return new_req

# Leave list (validated small JSON body)
@requests_bp.post('/leave/list')
@requests_bp.input(MonthlyStatusQuery, location='json', arg_name='payload')
@requests_bp.output(LeaveRequestOut(many=True))
@jwt_required()
def list_leave_requests(payload):
    user_id = int(get_jwt_identity())
    month = payload['month']
    year = payload['year']
    return rs.list_leave_requests(month, year, user_id)

# OT create
@requests_bp.post('/ot')
@requests_bp.input(OTRequestIn, arg_name='data')
@requests_bp.output(OTRequestOut, status_code=201)
@jwt_required()
def create_ot_request(data):
    user_id = int(get_jwt_identity())
    new_req = rs.create_ot_request(data, user_id)
    return new_req

# OT list
@requests_bp.post('/ot/list')
@requests_bp.input(MonthlyStatusQuery, location='json', arg_name='payload')
@requests_bp.output(OTRequestOut(many=True))
@jwt_required()
def list_ot_requests(payload):
    user_id = int(get_jwt_identity())
    month = payload['month']
    year = payload['year']
    return rs.list_ot_requests(month, year, user_id)

# WFH create
@requests_bp.post('/wfh')
@requests_bp.input(WFHRequestIn, arg_name='data')
@requests_bp.output(WFHRequestOut, status_code=201)
@jwt_required()
def create_wfh_request(data):
    user_id = int(get_jwt_identity())
    new_req = rs.create_wfh_request(data, user_id)
    return new_req

# WFH list
@requests_bp.post('/wfh/list')
@requests_bp.input(MonthlyStatusQuery, location='json', arg_name='payload')
@requests_bp.output(WFHRequestOut(many=True))
@jwt_required()
def list_wfh_requests(payload):
    user_id = int(get_jwt_identity())
    month = payload['month']
    year = payload['year']
    return rs.list_wfh_requests(month, year, user_id)
