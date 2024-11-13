from sqlitin import get_db_connection
import time

class Attendance:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.start_time = None

    def check_in(self):
        self.start_time = time.time()
        return {"message": "Check-in successful"}

    def check_out(self):
        if not self.start_time:
            return {"message": "Check-in was not recorded"}, 400
        elapsed_time = time.time() - self.start_time
        self.start_time = None
        return {"message": "Check-out successful", "elapsed_time": elapsed_time}
