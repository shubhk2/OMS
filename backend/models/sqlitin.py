import sqlite3
# conni = sqlite3.connect('../office.db')
# conni.execute('PRAGMA foreign_keys = ON;')

# Create a cursor object to interact with the database
# cursor = conni.cursor()
def get_db_connection():
    conn = sqlite3.connect('../office.db')
    conn.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key constraints
    conn.row_factory = sqlite3.Row  # Enables access to row values by column names
    return conn

# conni.commit()
'''to get time difference between to times: SELECT
    printf('%02d:%02d:%02d',
        CAST((julianday(check_out_time) - julianday(check_in_time)) * 24 AS INTEGER),
        CAST(((julianday(check_out_time) - julianday(check_in_time)) * 24 * 60) % 60 AS INTEGER),
        CAST(((julianday(check_out_time) - julianday(check_in_time)) * 24 * 3600) % 60 AS INTEGER)
    ) AS time_diff
FROM Attendance
WHERE employee_id = 2 AND date = '2024-11-28';'''


# print(cursor.fetchall())
# cursor.execute('PRAGMA table_info("Attendance");')
# print(cursor.fetchall())
# cursor.execute('PRAGMA table_info("Project_Team");')
# print(cursor.fetchall())
# cursor.execute("PRAGMA table_info('Projects');")
# print(cursor.fetchall())
# cursor.execute("PRAGMA table_info('Employee_Team');")
# print(cursor.fetchall())
# cursor.execute("PRAGMA table_info('Team_Project');")
# print(cursor.fetchall())
# cursor.execute("PRAGMA table_info('Employee_Project_Team');")
# print(cursor.fetchall(),'\n')
# cursor.execute("PRAGMA table_info('Overtime_Requests');")
# print(cursor.fetchall())
# cursor.execute("PRAGMA table_info('WFH_hr_approval');")

