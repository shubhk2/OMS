from sqlitin import get_db_connection
import time

class DailyAttendance:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.start_time = None
        self.break_start_time=None


    def check_in(self):
        self.start_time = time.time()
        conn=get_db_connection()
        conn.execute("Insert into Attendance (employee_id) values (?)", (self.employee_id,))
        conn.commit()
        conn.close()
        return {"message": "Check-in successful"}

    def check_out(self):
        if not self.start_time:
            return {"message": "Check-in was not recorded"}, 400
        elapsed_time = time.time() - self.start_time
        conn=get_db_connection()
        conn.execute("Update Attendance set check_out_time = CURRENT_TIME where employee_id = ? and Attendance.check_out_time is null", (self.employee_id,))
        self.start_time = None
        conn.commit()
        conn.close()
        return {"message": "Check-out successful", "elapsed_time": elapsed_time}

    def break_start(self):
        self.break_start_time = time.time()


        return {"message": "Break started"}

    def break_end(self):
        if not self.break_start_time:
            return {"message": "Break was not started"}, 400
        elapsed_time = time.time() - self.break_start_time
        hour=elapsed_time//3600
        minute=(elapsed_time%3600)//60
        second=(elapsed_time%3600)%60
        time_elapsed=str(hour)+":"+str(minute)+":"+str(second)[0:2]

        conn=get_db_connection()
        conn.execute("Update Attendance set break_time = ? where employee_id = ? and Attendance.check_out_time is null", (time_elapsed,self.employee_id))
        self.break_start_time = None
        conn.commit()
        conn.close()
        return {"message": "Break ended", "elapsed_time": elapsed_time}

class CumulativeAttendance:
    def __init__(self,employee_id):
        self.employee_id=employee_id

    def get_monthly_attendance(self,month):
        conn=get_db_connection()
        res=conn.execute("Select count(date) from Attendance where employee_id=? and strftime('%Y-%m', date) = ?",(self.employee_id,'2025-'+str(month))).fetchall()
        conn.close()
        return {'Monthly Attendance':res}

    def get_working_time_by_day(self,date):
        conn = get_db_connection()
        res=conn.execute('''SELECT check_in_time,check_out_time,
        printf('%02d:%02d:%02d',
        CAST((julianday(check_out_time) - julianday(check_in_time)) * 24 AS INTEGER),
        CAST(((julianday(check_out_time) - julianday(check_in_time)) * 24 * 60) % 60 AS INTEGER),
        CAST(((julianday(check_out_time) - julianday(check_in_time)) * 24 * 3600) % 60 AS INTEGER)
        ) AS time_diff
        FROM Attendance
        WHERE employee_id = ? AND date = ?;''',(self.employee_id,date)).fetchone()
        conn.close()
        return {"Work_time":res}




# d=DailyAttendance(3)
# print(d.check_in())
# time.sleep(5)
# print(d.break_start())
# time.sleep(5)
# print(d.break_end())
# print(d.check_out())
obj=CumulativeAttendance(2)
print(obj.get_monthly_attendance(11))
print(obj.get_working_time_by_day('2024-11-28'))

"when user presses break button he should #canceled enter time in minutes and then the break should start and end after that time but if the user returns before the time ends he should press the end break button ##  and the time should be recorded"
"break start is called when user selects a time and starts a break"
"if a user forgets to end break then what happens should be considered in future"#we can automatically end the break after the time they entered has elapsed
"if a user presses checkout by mistake than they can check in again with their time being cumulated"