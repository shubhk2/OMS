# python
# File: `backend/app.py`
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from werkzeug.security import check_password_hash
from datetime import timedelta
from flask_cors import CORS
from backend.db import get_db_connection
import time
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
# Configure CORS to explicitly allow Authorization header to avoid preflight issues
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"], expose_headers=["Authorization"])

# Setup the Flask-JWT-Extended extension
# Read secret from either JWT_SECRET_KEY (preferred) or JWT_SECRET for backwards compatibility
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', os.environ.get('JWT_SECRET', 'super-secret'))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

# JWT error handlers for better logging and clearer responses
@jwt.unauthorized_loader
def custom_unauthorized_response(err_str):
    logger.warning(f"JWT unauthorized: {err_str}")
    return jsonify({"msg": "Missing or malformed Authorization header"}), 401

@jwt.invalid_token_loader
def custom_invalid_token_response(err_str):
    logger.warning(f"JWT invalid token: {err_str}")
    return jsonify({"msg": "Invalid token"}), 422

@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    logger.warning("JWT expired token")
    return jsonify({"msg": "Token has expired"}), 401

def row_to_dict(row, cursor):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    # If cursor has description, map column names to row tuple
    if hasattr(cursor, 'description') and cursor.description:
        cols = [desc[0] for desc in cursor.description]
        return dict(zip(cols, row))
    return row

@app.route('/login', methods=['POST'])
def login():
    # Accept JSON or form data
    data = request.get_json(silent=True) or request.form
    username = None
    if hasattr(data, 'get'):
        username = data.get('username') or data.get('email') or data.get('user')
        password = data.get('password')
    else:
        username = None
        password = None

    if not password:
        return jsonify({"error": "Missing password field in request"}), 400
    logger.info(f"username: {username}, password provided: {'yes' if password else 'no'}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM   employee WHERE name = %s", (username,))
    raw = cursor.fetchone()
    user = row_to_dict(raw, cursor)
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    stored_password = user.get('password') if isinstance(user, dict) else None

    if stored_password is None:
        return jsonify({"error": "Account stored password missing — contact administrator"}), 500

    if not check_password_hash(stored_password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create access token with string identity to satisfy PyJWT "Subject must be a string" requirement
    access_token = create_access_token(identity=str(user.get('id')))
    return jsonify(access_token=access_token)

@app.route('/profile')
@jwt_required()
def profile():
    # JWT identity is stored as a string; convert to int for DB use
    current_user_identity = get_jwt_identity()
    try:
        current_user_id = int(current_user_identity)
    except (TypeError, ValueError):
        logger.warning(f"Invalid JWT identity type: {current_user_identity}")
        return jsonify({"msg": "Invalid token identity"}), 422
    logger.info(f"/profile accessed by user id: {current_user_id}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role, specialization FROM employee WHERE id = %s", (current_user_id,))
    raw = cursor.fetchone()
    user = row_to_dict(raw, cursor)
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({"msg": "User not found"}), 404

start_time = None

@app.route('/checkin', methods=['POST'])
@jwt_required()
def checkin():
    global start_time
    start_time = time.time()
    return jsonify({"message": "Timer started"}), 200

@app.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    global start_time
    if start_time is None:
        return jsonify({"message": "Timer not started"}), 400
    elapsed_time = time.time() - start_time
    start_time = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time}), 200

@app.route('/elapsed', methods=['GET'])
@jwt_required()
def elapsed():
    if start_time is None:
        return jsonify({"elapsed_time": "00:00:00"}), 200
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return jsonify({"elapsed_time": f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"}), 200

@app.route('/api/latest-checkins', methods=['GET'])
@jwt_required()
def latest_checkins():
    """Get latest checked-in employees for admin dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get the 5 most recent check-ins for today
        cursor.execute("""
            SELECT e.id, e.name, a.check_in_time, a.date
            FROM attendance a
            JOIN employee e ON a.employee_id = e.id
            WHERE a.date = CURRENT_DATE
            ORDER BY a.check_in_time DESC
            LIMIT 5
        """)
        rows = cursor.fetchall()
        checkins = []
        for row in rows:
            checkin = row_to_dict(row, cursor)
            checkins.append(checkin)
        cursor.close()
        conn.close()
        return jsonify(checkins), 200
    except Exception as e:
        logger.error(f"Error fetching latest check-ins: {e}")
        return jsonify({"error": "Failed to fetch check-ins"}), 500

@app.route('/api/ongoing-projects', methods=['GET'])
@jwt_required()
def ongoing_projects():
    """Get ongoing projects for admin dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get 4 ongoing projects (status = 1 means ongoing)
        cursor.execute("""
            SELECT id, name, status, deadline
            FROM project
            WHERE status = 1
            ORDER BY deadline ASC
            LIMIT 4
        """)
        rows = cursor.fetchall()
        projects = []
        for row in rows:
            project = row_to_dict(row, cursor)
            projects.append(project)
        cursor.close()
        conn.close()
        return jsonify(projects), 200
    except Exception as e:
        logger.error(f"Error fetching ongoing projects: {e}")
        return jsonify({"error": "Failed to fetch projects"}), 500

if __name__ == '__main__':
    app.run(debug=True)
