from apiflask import APIBlueprint
from flask_jwt_extended import create_access_token
from backend.services.auth_service import authenticate_user
from backend.schemas import LoginIn, LoginOut
from flask import jsonify
# Import the new models

bp = APIBlueprint('auth', __name__, url_prefix='/auth')

@bp.post('/login')
@bp.input(LoginIn) # Use the Pydantic model for input
def login(json_data):
    username = json_data.username
    password = json_data.password

    if not password:
        return {"error": "Missing password field in request"}, 400

    user = authenticate_user(username, password)
    if user is None:
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.get('id')))
    # return role id too (frontend uses it for routing)
    return jsonify(access_token=access_token, role=user.get('role'))
