from backend.models import db
from datetime import datetime


class OvertimeRequest(db.Model):
    __tablename__ = 'overtime_request'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    for_date = db.Column(db.Date)
    extra_task_description = db.Column(db.Text)
    requested_minutes = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)  # 0=pending, 1=approved, 2=rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'for_date': self.for_date.isoformat() if self.for_date else None,
            'extra_task_description': self.extra_task_description,
            'requested_minutes': self.requested_minutes,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

