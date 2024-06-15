from ..utils import db

class Discoteca(db.Model):
    __tablename__ = 'discotecas'

    id = db.Column(db.Integer, primary_key=True)
    duenos_id = db.Column(db.Integer, db.ForeignKey('duenos.id'), nullable=False)
    duenos = db.relationship(
        'Duenos', 
        backref='duenos'
    )

    nombre = db.Column(db.String(50), unique=True, nullable=False)
    direccion = db.Column(db.String(100), unique=True, nullable=False)
    instagram = db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return f"<Discoteca {self.nombre}"
    
    def json(self):
        return {
            'id' : self.id,
            'duenos_id' : self.duenos_id,
            'nombre' : self.nombre,
            'direccion' : self.direccion,
            'instagram' : self.instagram
        }