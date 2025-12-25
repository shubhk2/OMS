from backend.models import db


class Specialization(db.Model):
    __tablename__ = 'specialization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))

    def to_dict(self):
        return {'id': self.id, 'name': self.name}
# from backend.models import db
# from datetime import datetime




