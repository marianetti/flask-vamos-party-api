from ..utils import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Colduumn(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.name}"

    def json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'user' : self.user,
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


