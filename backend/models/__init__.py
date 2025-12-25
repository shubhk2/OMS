from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from backend.models.role import Role  # ensures 'role' table is registered
from backend.models.employee import Employee
from backend.models.team import Team
from backend.models.attendance import Attendance
from backend.models.leave_request import LeaveRequest
from backend.models.overtime_request import OvertimeRequest
from backend.models.wfh_request import WFHRequest
from backend.models.specialization import Specialization