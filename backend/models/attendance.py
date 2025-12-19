from backend.models import db
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import ARRAY, TIME


class Attendance(db.Model):
    __tablename__ = 'attendance'

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    check_in_time = db.Column(db.Time, primary_key=True, default=datetime.utcnow().time)
    date = db.Column(db.Date, primary_key=True, default=date.today)
    check_out_time = db.Column(db.Time, nullable=True)
    # integer total break seconds for the attendance row
    total_break_time = db.Column(db.Integer, default=0)
    # arrays of TIME values to record multiple break starts/ends in the same attendance row
    break_start_times = db.Column(ARRAY(TIME), nullable=True)
    break_end_times = db.Column(ARRAY(TIME), nullable=True)
    overtime_minutes = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        # format total_break_time seconds to HH:MM:SS
        total_break_seconds = self.total_break_time or 0
        hrs, rem = divmod(total_break_seconds, 3600)
        mins, secs = divmod(rem, 60)
        return {
            'employee_id': self.employee_id,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'date': self.date.isoformat() if self.date else None,
            'total_break_time': f"{int(hrs):02}:{int(mins):02}:{int(secs):02}",
            'break_start_times': [t.isoformat() for t in self.break_start_times] if self.break_start_times else [],
            'break_end_times': [t.isoformat() for t in self.break_end_times] if self.break_end_times else [],
            'overtime_minutes': self.overtime_minutes,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
