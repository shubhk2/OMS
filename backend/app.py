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
import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', 'super-secret')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

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
    cursor.execute("SELECT * FROM employee WHERE name = %s", (username,))
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

    access_token = create_access_token(identity=user.get('id'))
    return jsonify(access_token=access_token)

@app.route('/profile')
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
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

@app.route('/attendance/checkin', methods=['POST'])
@jwt_required()
def checkin():
    current_user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if there is already an open check-in (check_out_time is null)
        cursor.execute(
            "SELECT id FROM attendance WHERE employee_id = %s AND check_out_time IS NULL",
            (current_user_id,)
        )
        if cursor.fetchone():
            return jsonify({"error": "User already checked in"}), 409

        cursor.execute(
            "INSERT INTO attendance (employee_id, check_in_time) VALUES (%s, NOW())",
            (current_user_id,)
        )
        conn.commit()
        return jsonify({"message": "Checked in successfully"}), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/attendance/checkout', methods=['POST'])
@jwt_required()
def checkout():
    current_user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Find the open check-in record
        cursor.execute(
            "SELECT id FROM attendance WHERE employee_id = %s AND check_out_time IS NULL ORDER BY check_in_time DESC LIMIT 1",
            (current_user_id,)
        )
        attendance_record = cursor.fetchone()

        if not attendance_record:
            return jsonify({"error": "No active check-in found"}), 404

        attendance_id = attendance_record['id']
        cursor.execute(
            "UPDATE attendance SET check_out_time = NOW() WHERE id = %s",
            (attendance_id,)
        )
        conn.commit()
        return jsonify({"message": "Checked out successfully"}), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/attendance/elapsed', methods=['GET'])
@jwt_required()
def elapsed():
    current_user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT check_in_time FROM attendance WHERE employee_id = %s AND check_out_time IS NULL ORDER BY check_in_time DESC LIMIT 1",
            (current_user_id,)
        )
        record = cursor.fetchone()
        if record and record['check_in_time']:
            elapsed_time = datetime.datetime.now(datetime.timezone.utc) - record['check_in_time']
            hours, rem = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(rem, 60)
            return jsonify({"elapsed_time": f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"}), 200
        else:
            return jsonify({"elapsed_time": "00:00:00"}), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/attendance/status', methods=['GET'])
@jwt_required()
def attendance_status():
    current_user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT check_in_time FROM attendance WHERE employee_id = %s AND check_out_time IS NULL ORDER BY check_in_time DESC LIMIT 1",
            (current_user_id,)
        )
        record = cursor.fetchone()
        is_checked_in = record is not None
        return jsonify({"is_checked_in": is_checked_in}), 200
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
