from ..utils import db

from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    clubs = db.relationship('Club', backref='users', lazy=True)


    def __repr__(self):
        return f"<User {self.username}"

    def json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'username' : self.user,
            'password_hash' : self.password_hash,
            'email' : self.email
        }

    def save(self):
        db.session.add(self)
        db.session.commit() 

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_by_id(cls, id):
        return cls.query.get_or_404(id)



