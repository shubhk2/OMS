from backend.models import db
from datetime import datetime

class LeaveType(db.Model):
    __tablename__ = 'leave_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    approval_type = db.Column(db.Integer, comment='0-only hr, 1-only tl, 2-both')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'approval_type': self.approval_type
        }

class LeaveRequest(db.Model):
    __tablename__ = 'leave_request'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_type.id'))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    reason = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)  # 0: Pending, 1: Approved, 2: Declined
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    leave_type = db.relationship('LeaveType')
    # employee = db.relationship('Employee') # Avoid circular import if possible, or use string

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type_id': self.leave_type_id,
            'leave_type_name': self.leave_type.name if self.leave_type else None,
            'from_date': self.from_date.isoformat() if self.from_date else None,
            'to_date': self.to_date.isoformat() if self.to_date else None,
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

