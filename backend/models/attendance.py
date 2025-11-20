from backend.models import db
from datetime import datetime, date, time


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    check_in_time = db.Column(db.Time, primary_key=True, default=datetime.utcnow().time)
    date = db.Column(db.Date, primary_key=True, default=date.today)
    check_out_time = db.Column(db.Time, nullable=True)
    break_time = db.Column(db.Time, default=time(0, 0, 0))
    overtime_minutes = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'employee_id': self.employee_id,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'date': self.date.isoformat() if self.date else None,
            'break_time': self.break_time.isoformat() if self.break_time else None,
            'overtime_minutes': self.overtime_minutes,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

