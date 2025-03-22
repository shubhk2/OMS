from sqlitin import get_db_connection
from Employee import *
import time
class OT:
    def __init__(self,id):
        self.employee_id=id

    def ot_request(self,for_date,requested_min,description=None):#check if optional is set like this only
        conn=get_db_connection()
        if description:
            conn.execute('Insert into Overtime_Request (employee_id,for_date,extra_task_description,requested_minutes) values (?,?,?,?)',(self.employee_id,for_date,description,requested_min))
        else:
            conn.execute('Insert into Overtime_Request (employee_id,for_date,requested_minutes) values (?,?,?)',(self.employee_id,for_date,requested_min))

        conn.close()
        return {"ot_request_entry":200}

    def ot_to_be_approved_tl(self):
        """Enter id of tl in the class object"""
        e=Employee(self.employee_id)
        team=e.get_team_leader_id()
        conn=get_db_connection()
        res=conn.execute("Select employee_id,for_date,extra_task_description,requested_minutes from Overtime_Request  where status=0 and employee_id in (Select id from Employee where primary_team_id=?)",(team,))
        conn.close()
        return {"tl_ot_list":res}

    def ot_to_be_approved_hr(self):
        """Enter id of hr in the class object->get ot_rec to be approved"""
        e=Employee(self.employee_id)
        conn=get_db_connection()
        res=conn.execute("Select o.employee_id,for_date,extra_task_description,requested_minutes from Overtime_Request o join main.Ot_tl_approval Ota on o.id = Ota.ot_request_id ")

        conn.close()
        return {"hr_ot_list":res}

    def approve_ot_tl(self,ot_request_id):#ot request id from Overtime_Request.id
        conn=get_db_connection()
        conn.execute("Insert into Ot_tl_approval (ot_request_id,tl_id) values (?,?)",(ot_request_id,self.employee_id))
        conn.close()
        return {"message":"ot_approved"}

    def approve_ot_hr(self,ot_request_id):#ot request id from Overtime_Request.id
        conn=get_db_connection()
        conn.execute("Insert into Ot_hr_approval (ot_request_id,hr_id) values (?,?)",(ot_request_id,self.employee_id))
        conn.close()
        return {"message":"ot_approved"}