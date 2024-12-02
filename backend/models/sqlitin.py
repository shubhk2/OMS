import sqlite3
conni = sqlite3.connect('../office.db')
conni.execute('PRAGMA foreign_keys = ON;')

# Create a cursor object to interact with the database
cursor = conni.cursor()
def get_db_connection():
    conn = sqlite3.connect('../office.db')
    conn.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key constraints
    conn.row_factory = sqlite3.Row  # Enables access to row values by column names
    return conn

# cursor.execute('''Create TABLE IF NOT EXISTS Role(id integer primary key ,name varchar(20),created_at DATETIME DEFAULT CURRENT_TIMESTAMP,updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
# cursor.execute('''Create trigger IF NOT EXISTS update_role_updated_at after update on Role for each row begin update Role set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''Insert into Role(name) VALUES ('Employee'),('Team Leader'),('Project Manager'),('HR Manager'),('Admin')''')
# cursor.execute('''Create TABLE IF NOT EXISTS Specialization(id integer primary key ,name varchar(20),created_at DATETIME DEFAULT CURRENT_TIMESTAMP,updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
# cursor.execute('''create trigger IF NOT EXISTS update_specialization_updated_at after update on Specialization for each row begin update Specialization set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''Insert into Specialization(name) VALUES ('Frontend Developer'),('Backend Developer'),('Full Stack Developer'),('UI/UX Designer'),('Data Analyst'),('Business Analyst'),('Game Developer'),('Mobile Developer'),('DevOps Engineer'),('Cloud Engineer'),('Quality Assurance Engineer')''')
# cursor.execute('DROP TABLE Employee;')
# #
# cursor.execute(''' create TABLE IF NOT EXISTS Employee (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(30),
#     username VARCHAR(30),
#     role Integer default 1,
#     specialization integer,
#     primary_team_id INTEGER default 1,
#     status INTEGER default 1,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (primary_team_id) REFERENCES Team(id),FOREIGN KEY (role) REFERENCES Role(id),FOREIGN KEY (specialization) REFERENCES Specialization(id)
# );''')
# cursor.execute('DROP TABLE IF EXISTS Team;')
# cursor.execute('''CREATE TABLE IF NOT EXISTS Team (id int Primary Key,
# name vachar(50),
# team_leader_id int,
# status int default 1,
# created_at datetime DEFAULT CURRENT_TIMESTAMP,
# updated_at datetime default CURRENT_TIMESTAMP,FOREIGN KEY (team_leader_id) REFERENCES Employee(id))''')
#
#
# #
# cursor.execute('''Drop trigger update_team_updated_at;''')
"update row after team table row is updated"
# cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_team_updated_at
# AFTER UPDATE ON Team
# FOR EACH ROW
# BEGIN
#     UPDATE Team SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
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
# cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_project_updated_at
# AFTER UPDATE ON Project
# FOR EACH ROW
# BEGIN
#     UPDATE Project SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
# END;''')
# cursor.execute('''drop trigger update_employee_updated_at;''')
# cursor.execute('''
# CREATE TRIGGER IF NOT EXISTS update_employee_updated_at
# AFTER UPDATE ON Employee
# FOR EACH ROW
# BEGIN
#     UPDATE Employee SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
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
# cursor.execute('''DROP TABLE IF EXISTS Overtime_Requests;''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS Overtime_Requests (
#     id INTEGER PRIMARY KEY,
#     employee_id INTEGER,
#     for_date DATE,
#     extra_task_description TEXT,
#     requested_hours INTEGER,
#     status INTEGER DEFAULT 0, -- 0: Pending, 1: Approved, 2: Rejected
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (employee_id) REFERENCES Employee(id)
# );''')
# #
# cursor.execute('''DROP TRIGGER IF EXISTS update_overtime_requests_updated_at;''')
# cursor.execute('''create TRIGGER IF NOT EXISTS update_overtime_request_updated_at
# AFTER UPDATE ON Overtime_Request
# FOR EACH ROW
# BEGIN
#     UPDATE Overtime_Request SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
# END;''')
# cursor.execute('''DROP TABLE IF EXISTS Attendance;''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (
#     employee_id INTEGER not null,
#     check_in_time DATETIME,
#     check_out_time DATETIME,
#     break_time DateTime default null,
#     total_hours_worked INTEGER,
#     overtime_hours INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (employee_id, check_in_time),
#     FOREIGN KEY (employee_id) REFERENCES Employee(id) on update cascade
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
# cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_task_updated_at
# AFTER UPDATE ON Task
# FOR EACH ROW
# BEGIN
#     UPDATE Task SET updated_at = CURRENT_TIMESTAMP WHERE task_id = OLD.task_id;
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
# cursor.execute(''' UPDATE Employee SET primary_team_id = 1 WHERE primary_team_id is null;''')
# END;''')
# cursor.execute('''Delete from Team ;''')
# cursor.execute('''Insert into Team(id,name,team_leader_id) VALUES (1,"Main",1);''')

# cursor.execute('''create table leave_types(id integer primary key not null,name text,created_at datetime default current_timestamp,updated_at datetime default current_timestamp)''')
# cursor.execute('''create table leave_requests(id integer primary key,employee_id integer,leave_type_id integer,from_date date,to_date date,reason text,status integer default 0,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,FOREIGN KEY (employee_id) REFERENCES Employee(id),FOREIGN KEY (leave_type_id) REFERENCES leave_types(id))''')
# cursor.execute('''create trigger update_wfh_type_updated_at after update on WFH_type for each row begin update WFH_type set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_leave_type_updated_at after update on Leave_type for each row begin update Leave_type set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_leave_request_updated_at after update on Leave_request for each row begin update Leave_request set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_wfh_request_updated_at after update on WFH_request for each row begin update WFH_request set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create table WFH_requests(id integer primary key,employee_id integer,wfh_type_id integer,from_date date,to_date date,reason text,status integer default 0,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,FOREIGN KEY (employee_id) REFERENCES Employee(id),foreign key (wfh_type_id) references WFH_types(id))''')
# cursor.execute(''' create table Ot_hr_approval(id integer primary key,employee_id integer,ot_request_id integer,hr_id integer,approved_hours integer,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,foreign key (employee_id) references Employee(id),foreign key (ot_request_id) references Overtime_Requests(id),foreign key (hr_id) references Employee(id))''')
# cursor.execute(''' create table Leave_hr_approval(id integer primary key,employee_id integer,leave_request_id integer,hr_id integer,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,foreign key (employee_id) references Employee(id),foreign key (leave_request_id) references leave_requests(id),foreign key (hr_id) references Employee(id))''')
# cursor.execute(''' create table Wfh_hr_approval(id integer primary key,wfh_request_id integer,hr_id integer,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,foreign key (wfh_request_id) references WFH_requests(id),foreign key (hr_id) references Employee(id))''')
# cursor.execute('''create table Ot_tl_approval(id integer primary key,employee_id integer,ot_request_id integer,tl_id integer,approved_hours integer,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,foreign key (employee_id) references Employee(id),foreign key (ot_request_id) references Overtime_Requests(id),foreign key (tl_id) references Employee(id))''')
# cursor.execute('''create table Leave_tl_approval(id integer primary key,employee_id integer,leave_request_id integer,tl_id integer,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,foreign key (employee_id) references Employee(id),foreign key (leave_request_id) references leave_requests(id),foreign key (tl_id) references Employee(id))''')
# cursor.execute('''create table Wfh_tl_approval(id integer primary key,wfh_request_id integer,tl_id integer,created_at datetime default current_timestamp,updated_at datetime default current_timestamp,foreign key (wfh_request_id) references WFH_requests(id),foreign key (tl_id) references Employee(id))''')
# cursor.execute('''create trigger update_Ot_hr_approval_updated_at after update on Ot_hr_approval for each row begin update Ot_hr_approval set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_Leave_hr_approval_updated_at after update on Leave_hr_approval for each row begin update Leave_hr_approval set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_Wfh_hr_approval_updated_at after update on Wfh_hr_approval for each row begin update Wfh_hr_approval set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_Ot_tl_approval_updated_at after update on Ot_tl_approval for each row begin update Ot_tl_approval set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_Leave_tl_approval_updated_at after update on Leave_tl_approval for each row begin update Leave_tl_approval set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# cursor.execute('''create trigger update_Wfh_tl_approval_updated_at after update on Wfh_tl_approval for each row begin update Wfh_tl_approval set updated_at=CURRENT_TIMESTAMP where id=old.id; end;''')
# print(cursor.fetchall())

cursor.execute('''INSERT INTO Role (id, name) VALUES 
(7, 'Team Manager'),
(8, 'Project Manager'),
(9, 'Product Manager'),
(10, 'Scrum Master'),
(11, 'HR Manager (HRM)'),
(12, 'HR Director (HRD)'),
(13, 'Chief Technology Officer (CTO)')''')

conni.commit()

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
cursor.execute("PRAGMA table_info('WFH_hr_approval');")
print(cursor.fetchall())
