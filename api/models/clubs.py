from ..utils import db

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship(
        'Users', 
        backref='users'
    )

    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    instagram = db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return f"<Clubs {self.name}"
    
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
        db.commit()
    
    def update(self):
        db.commit()
    
    def delete(self):
        db.session.delete(self)
        db.commit()