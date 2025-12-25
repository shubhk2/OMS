# python
# File: `backend/app.py`
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from flask_cors import CORS
from apiflask import APIFlask
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = APIFlask(__name__, title="My API", version="1.0")
app.security_schemes = {
    'BearerAuth': {
        'type': 'http',
        'scheme': 'bearer',
        'bearerFormat': 'JWT',
    }
}
app.config['SECURITY'] = [{'BearerAuth': []}]
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', 'super-secret')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

# Setup SQLAlchemy
postgres_url = os.environ.get('POSTGRES_URL')
# if postgres_url and not postgres_url.startswith('postgresql://'):
#     # Handle postgres:// -> postgresql:// for SQLAlchemy
#     postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
if postgres_url and 'sslmode=' not in postgres_url:
    postgres_url += '&sslmode=require' if '?' in postgres_url else '?sslmode=require'

app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from backend.models import db
db.init_app(app)


# def row_to_dict(row, cursor=None):
#     # Kept for any legacy use; not used in new services.
#     if row is None:
#         return None
#     if isinstance(row, dict):
#         return row
#     if cursor is not None and hasattr(cursor, 'description') and cursor.description:
#         cols = [desc[0] for desc in cursor.description]
#         return dict(zip(cols, row))
#     return row


# Register blueprints
from backend.routes.auth_routes import bp as auth_bp
from backend.routes.employee_routes import bp as employee_bp
from backend.routes.attendance_routes import bp as attendance_bp
from backend.routes.ot_routes import bp as ot_bp
from backend.routes.requests_routes import requests_bp
from backend.routes.admin_routes import bp as admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(ot_bp)
app.register_blueprint(requests_bp)
app.register_blueprint(admin_bp)


@app.route('/profile')
@jwt_required()
def profile():
    """
    Get current user profile
      200:
        description: User profile
      404:
        description: User not found
    """
    from backend.models.employee import Employee

    current_user_id = int(get_jwt_identity())
    user = Employee.query.filter_by(id=current_user_id).first()

    if user:
        return {
            'id': user.id,
            'name': user.name,
            'role': user.role,
            'specialization': user.specialization,
            'email': user.email,
            'username': user.username,
            'primary_team_id': user.primary_team_id,
            'status': user.status
        }
    return {"msg": "User not found"}, 404


if __name__ == '__main__':
    app.run(debug=True)
