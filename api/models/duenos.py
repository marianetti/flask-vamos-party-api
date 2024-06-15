from ..utils import db

class Dueno(db.Model):
    __tablename__ = 'duenos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    user = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return f"<Dueño {self.nombre}"

    def json(self):
        return {
            'id' : self.id,
            'nombre' : self.nombre,
            'user' : self.user,
            'passwprd' : self.password,
            'email' : self.email
        }

    def save(self):
        db.session.add(self)
        db.session.commit() 


