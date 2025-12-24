from backend.models import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30))
    role = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)
    specialization = db.Column(db.Integer, db.ForeignKey('specialization.id'))
    primary_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), default=1)
    status = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email = db.Column(db.String(25), default='shubhk2004@gmail.com')
    password = db.Column(db.String(255))
    curr_salary = db.Column(db.Numeric(10, 2), nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'role': self.role,
            'specialization': self.specialization,
            'primary_team_id': self.primary_team_id,
            'status': self.status,
            'email': self.email,
            'curr_salary': float(self.curr_salary) if self.curr_salary else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

