import sqlite3
conni = sqlite3.connect('office.db')

# Create a cursor object to interact with the database
cursor = conni.cursor()
def get_db_connection():
    conn = sqlite3.connect('Student_db.db')
    conn.row_factory = sqlite3.Row  # Enables access to row values by column names
    return conn
# cursor.execute('DROP TABLE IF EXISTS Team;')
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Team (id int Primary Key,
# name vachar(50),
# leader_name varchar(50),
# status
# created_at datetime DEFAULT CURRENT_TIMESTAMP,
# updated_at datetime default CURRENT_TIMESTAMP)''')
#
#
# #
"update row after team table row is updated"
# cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_team_updated_at
# AFTER UPDATE ON Team
# FOR EACH ROW
# BEGIN
#     UPDATE Team SET updated_at = CURRENT_TIMESTAMP WHERE Team.id = OLD.Team.id;
# END;
# ''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS Projects (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(100),
#     status VARCHAR(50),
#     deadline DATE,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );''')
# cursor.execute('''drop trigger update_projects_updated_at;''')
# cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_projects_updated_at
# AFTER UPDATE ON Projects
# FOR EACH ROW
# BEGIN
#     UPDATE Projects SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
# END;''')
# cursor.execute('DROP TABLE Employee_dg_tmp;')
# #
# cursor.execute(''' create TABLE IF NOT EXISTS Employee (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(100),
#     role VARCHAR(50) default 'Employee',
#     specialization VARCHAR(100),
#     primary_team_id INTEGER default 1,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (primary_team_id) REFERENCES Team(id)
# );''')
# # cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_employee_updated_at
# AFTER UPDATE ON Employee
# FOR EACH ROW
# BEGIN
#     UPDATE Employee SET updated_at = CURRENT_TIMESTAMP WHERE Employee.id = OLD.Employee.id;
# END;''')
"Project team is for the team of a project(not the original team) while team_project is for the project of a team(original team)"
# cursor.execute(''' create TABLE IF NOT EXISTS Project_Team (
#     project_team_id INTEGER PRIMARY KEY,
#     project_id INTEGER,
#     team_leader_id INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (project_id) REFERENCES Projects(id)
# );''')

# cursor.execute(''' create TRIGGER IF NOT EXISTS update_project_team_updated_at
# AFTER UPDATE ON Project_Team
# FOR EACH ROW
# BEGIN
#     UPDATE Project_Team SET updated_at = CURRENT_TIMESTAMP WHERE project_team_id = OLD.project_team_id;
# END;''')

# cursor.execute(''' create TABLE IF NOT EXISTS Employee_Team (
#     employee_id INTEGER,
#     team_id INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (employee_id, team_id),
#     FOREIGN KEY (employee_id) REFERENCES Employee(id),
#     FOREIGN KEY (team_id) REFERENCES Team(id)
# );''')
# cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_employee_team_updated_at
# AFTER UPDATE ON Employee_Team
# FOR EACH ROW
# BEGIN
#     UPDATE Employee_Team SET updated_at = CURRENT_TIMESTAMP WHERE employee_id = OLD.employee_id AND team_id = OLD.team_id;
# END;''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS Team_Project (
#     team_id INTEGER,
#     project_id INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (team_id, project_id),
#     FOREIGN KEY (team_id) REFERENCES Team(id),
#     FOREIGN KEY (project_id) REFERENCES Projects(id)
# );''')
# cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_team_project_updated_at
# AFTER UPDATE ON Team_Project
# FOR EACH ROW
# BEGIN
#     UPDATE Team_Project SET updated_at = CURRENT_TIMESTAMP WHERE team_id = OLD.team_id AND project_id = OLD.project_id;
# END;''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS Employee_Project_Team (
#     employee_id INTEGER,
#     project_team_id INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (employee_id, project_team_id),
#     FOREIGN KEY (employee_id) REFERENCES Employee(id),
#     FOREIGN KEY (project_team_id) REFERENCES Project_Team(project_team_id)
# );''')
#
# cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_employee_project_team_updated_at
# AFTER UPDATE ON Employee_Project_Team
# FOR EACH ROW
# BEGIN
#     UPDATE Employee_Project_Team SET updated_at = CURRENT_TIMESTAMP WHERE employee_id = OLD.employee_id AND project_team_id = OLD.project_team_id;
# END;''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS Overtime_Requests (
#     id INTEGER PRIMARY KEY,
#     employee_id INTEGER,
#     for_date DATE,
#     extra_task_description TEXT,
#     requested_hours INTEGER,
#     status VARCHAR(50),
#     approved_hours INTEGER,
#     approved_by VARCHAR(100),
#     approval_date DATE,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (employee_id) REFERENCES Employee(id)
# );''')
#
# cursor.execute('''create TRIGGER IF NOT EXISTS update_overtime_requests_updated_at
# AFTER UPDATE ON Overtime_Requests
# FOR EACH ROW
# BEGIN
#     UPDATE Overtime_Requests SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
# END;''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (
#     employee_id INTEGER,
#     check_in_time DATETIME,
#     check_out_time DATETIME,
#     break_time INTEGER,
#     total_hours_worked INTEGER,
#     overtime_hours INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (employee_id, check_in_time),
#     FOREIGN KEY (employee_id) REFERENCES Employee(id)
# );''')
# cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_attendance_updated_at
# AFTER UPDATE ON Attendance
# FOR EACH ROW
# BEGIN
#     UPDATE Attendance SET updated_at = CURRENT_TIMESTAMP WHERE employee_id = OLD.employee_id AND check_in_time = OLD.check_in_time;
# END;''')
# cursor.execute('''Drop table Salary;''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
#     task_id INTEGER PRIMARY KEY NOT NULL,
#     task_name VARCHAR(100),
#     project_id INTEGER,
#     employee_id INTEGER,
#     status VARCHAR(50),
#     deadline DATEtime,
#     completion_date DATEtime,
#     score INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (project_id) REFERENCES Projects(id),
#     FOREIGN KEY (employee_id) REFERENCES Employee(id)
# );''')
#
# cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_tasks_updated_at
# AFTER UPDATE ON Tasks
# FOR EACH ROW
# BEGIN
#     UPDATE Tasks SET updated_at = CURRENT_TIMESTAMP WHERE task_id = OLD.task_id;
# END;''')

# cursor.execute('''Create TABLE IF NOT EXISTS Salary (
#     id INTEGER PRIMARY KEY NOT NULL,
#     employee_id INTEGER,
#     month DATE,
#     base_salary REAL,
#     overtime_bonus REAL default 0,
#     wfh_deduction REAL default 0,
#     leave_deduction REAL default 0,
#     total_salary REAL,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (employee_id) REFERENCES Employee(id)
# );''')
#
# cursor.execute('''drop trigger update_salary_updated_at;''')
# cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_salary_updated_at
# AFTER UPDATE ON Salary
# FOR EACH ROW
# BEGIN
#     UPDATE Salary SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
# END;''')

cursor.execute('''Insert into Employee(name,role,specialization) VALUES ("Shlok","Team Leader","Active");''')

# print(cursor.fetchall())
conn.commit()

# cursor.execute('PRAGMA table_info("Employee");')
# print(cursor.fetchall())
# cursor.execute('PRAGMA table_info("Team");')
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
# cursor.execute("PRAGMA table_info('Attendance');")
# print(cursor.fetchall())
# cursor.execute("PRAGMA table_info('Tasks');")
# print(cursor.fetchall())