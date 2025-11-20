from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services import attendance_service
from apiflask import APIBlueprint
bp = APIBlueprint('attendance', __name__, url_prefix='/attendance')



@bp.route('/checkin', methods=['POST'])
@jwt_required()
@bp.doc(security='BearerAuth')
def checkin():
    current_user_id = int(get_jwt_identity())
    body, status = attendance_service.check_in(current_user_id)
    return body, status


@bp.route('/checkout', methods=['POST'])
@jwt_required()
@bp.doc(security='BearerAuth')
def checkout():
    current_user_id = int(get_jwt_identity())
    body, status = attendance_service.check_out(current_user_id)
    return body, status


@bp.route('/elapsed', methods=['GET'])
@jwt_required()
@bp.doc(security='BearerAuth')
def elapsed():
    current_user_id = int(get_jwt_identity())
    body, status = attendance_service.elapsed_time(current_user_id)
    return body, status


@bp.route('/status', methods=['GET'])
@jwt_required()
@bp.doc(security='BearerAuth')
def attendance_status():
    current_user_id = int(get_jwt_identity())
    body, status = attendance_service.is_checked_in(current_user_id)
    return body, status
# Routes package

