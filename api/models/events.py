from ..utils import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    style = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    buy_link = db.Column(db.String(100), nullable=True) 
    contact = db.Column(db.String(15), nullable=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    club = db.Column(db.Integer(), db.ForeignKey('clubs.id'), nullable=False) 


    def __repr__(self):
        return f"<Event {self.name}"
    
    def json(self):
        return {
            'id' : self.id,
            'club_id' : self.user_id,
            'name' : self.name,
            'date' : self.date,
            'style' : self.style,
            'age' : self.age,
            'buy_link' : self.buy_link,
            'contact' : self.contact
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)