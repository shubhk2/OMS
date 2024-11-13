from sqlitin import get_db_connection

class Employee:
    def __init__(self, id, name, specialization, primary_team_id, role='Employee'):
        self.id = id
        self.name = name
        self.role = role
        self.specialization = specialization
        self.primary_team_id = primary_team_id

    @staticmethod
    def get_employee_by_id(employee_id):
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM Employee WHERE id = ?', (employee_id,)).fetchone()
        conn.close()
        return employee

    # Add more methods for Employee operations
