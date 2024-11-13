from flask import Flask, jsonify
import time
import sqlite3
from sqlitin import get_db_connection
app = Flask(__name__)


class Employee:
    def __init__(self,id,name,specialization,primary_team_id,role=None):
        self.name=name
        self.id=id
        if role is None:
            self.role='Employee'
        else:
            self.role=role
        self.specialization=specialization
        self.primary_team_id=primary_team_id



start_time = None

@app.route('/checkin', methods=['POST'])
def checkin():
    global start_time
    start_time = time.time()
    return jsonify({"message": "Timer started"}), 200

@app.route('/checkout', methods=['POST'])
def checkout():
    global start_time
    if start_time is None:
        return jsonify({"message": "Timer not started"}), 400
    elapsed_time = time.time() - start_time
    start_time = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time}), 200

@app.route('/elapsed', methods=['GET'])
def elapsed():
    if start_time is None:
        return jsonify({"elapsed_time": "00:00:00"}), 200
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return jsonify({"elapsed_time": f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"}), 200



if __name__ == '__main__':
    app.run()
