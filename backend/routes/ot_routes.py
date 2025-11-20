from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from datetime import datetime
from backend.services import ot_service

bp = APIBlueprint('ot', __name__, url_prefix='/ot')


@bp.post('/request')
@jwt_required()
def ot_request():
    current_user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    for_date_str = data.get('for_date')  # expected YYYY-MM-DD
    requested_minutes = data.get('requested_minutes')
    description = data.get('description')

    if not for_date_str or requested_minutes is None:
        return {"error": "for_date and requested_minutes are required"}, 400

    for_date = datetime.strptime(for_date_str, "%Y-%m-%d").date()
    return ot_service.create_ot_request(current_user_id, for_date, int(requested_minutes), description)


@bp.get('/tl/pending')
@jwt_required()
def ot_pending_tl():
    current_user_id = int(get_jwt_identity())
    return ot_service.list_ot_to_be_approved_tl(current_user_id)


@bp.get('/hr/pending')
@jwt_required()
def ot_pending_hr():
    current_user_id = int(get_jwt_identity())
    return ot_service.list_ot_to_be_approved_hr(current_user_id)


@bp.post('/tl/approve/<int:ot_id>')
@jwt_required()
def ot_approve_tl(ot_id: int):
    current_user_id = int(get_jwt_identity())
    body, status = ot_service.approve_ot_tl(current_user_id, ot_id)
    return body, status


@bp.post('/hr/approve/<int:ot_id>')
@jwt_required()
def ot_approve_hr(ot_id: int):
    current_user_id = int(get_jwt_identity())
    body, status = ot_service.approve_ot_hr(current_user_id, ot_id)
    return body, status


