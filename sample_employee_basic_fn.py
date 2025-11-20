from sqlitin import get_db_connection

class Employee:
    def __init__(self, e_id):
        self.id=e_id

    def get_employee_by_id(self):
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM Employee WHERE id = ?', (self.id,)).fetchone()
        conn.close()
        return employee['name'], employee['email']

    def get_salary(self):
        conn = get_db_connection()
        salary = conn.execute('SELECT base_salary FROM Salary WHERE employee_id = ?', (self.id,)).fetchone()
        conn.close()
        salary=salary['base_salary']
        return salary

    def get_team_id(self):
        conn = get_db_connection()
        team_id = conn.execute(' select primary_team_id from Employee where id=?', (self.id,)).fetchone()
        conn.close()
        team_id=team_id['primary_team_id']
        return team_id

    def get_team_name(self):
        conn = get_db_connection()
        team_id=int(self.get_team_id())
        team_name = conn.execute('SELECT Team.name FROM Team WHERE Team.id =?', (team_id,)).fetchone()
        conn.close()
        team_name=team_name['name']
        return team_name

    def get_team_leader_id(self):
        conn = get_db_connection()
        t_id=int(self.get_team_id())
        team_lead = conn.execute('select team_leader_id from Team where id=?', (t_id,)).fetchone()
        conn.close()
        team_lead=team_lead['team_leader_id']
        return team_lead

    def get_team_leader_name(self):
        conn = get_db_connection()
        t_id=int(self.get_team_leader_id())
        team_lead_name = conn.execute('select name from Employee where id=?', (t_id,)).fetchone()
        conn.close()
        team_lead_name=team_lead_name['name']
        return team_lead_name

    def get_team_members(self):
        conn = get_db_connection()
        t_id=int(self.get_team_id())
        team_members = conn.execute('select name from Employee where primary_team_id=?', (t_id,)).fetchall()
        conn.close()
        team_members=[member['name'] for member in team_members]
        return team_members





e=Employee(2)
print(e.get_team_id(),e.get_team_name(),e.get_team_leader_name())
"js receives username and password from the user and sends it to the backend. The backend checks if the username and password are correct and sends a response back to the frontend. If the username and password are correct, the backend sends a response with a status code of 200. If the username and password are incorrect, the backend sends a response with a status code of 401. The frontend then will send the user to index.html if the user is found in database.make index.html dynamic."
