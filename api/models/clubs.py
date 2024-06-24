from ..utils import db
from datetime import datetime

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    instagram = db.Column(db.String(50), unique=True, nullable=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    events = db.relationship('Event', backref='clubs', lazy=True)

    def __repr__(self):
        return f"<Club {self.id}"
    
    def json(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'name' : self.name,
            'address' : self.address,
            'instagram' : self.instagram
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()