from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime


app = Flask(__name__)
app.config['SQL_ALQUEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Duenos(db.Model):
    __tablename__ = 'duenos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    user = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)

    def json(self):
        return {
            'id' : self.id,
            'nombre' : self.nombre,
            'user' : self.user,
            'passwprd' : self.password,
            'email' : self.email
        }


class Discotecas(db.Model):
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


    def json(self):
        return {
            'id' : self.id,
            'duenos_id' : self.duenos_id,
            'nombre' : self.nombre,
            'direccion' : self.direccion,
            'instagram' : self.instagram
        }
    
class Eventos(db.Model):
    #Modificar nombres de Edad, link_venta
    #Buscar forma de attachear imagen para promocionar evento

    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    discotecas_id = db.Column(db.Integer, db.ForeignKey('discotecas.id'), nullable=False)
    discotecas = db.relationship(
        'Discotecas',
        backref='dicotecas'
    )

    nombre = db.Column(db.String(100), unique=False, nullable=False)
    fecha = db.Column(db.String(100), nullable=False)
    genero_musical = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    link_venta = db.Column(db.String(100), nullable=True) 
    numero_contacto = db.Column(db.String(15), nullable=True)

   

    def json(self):
        return {
            'id' : self.id,
            'discotecas_id' : self.discotecas_id,
            'nombre' : self.nombre,
            'fecha' : self.fecha,
            'genero_musical' : self.genero_musical,
            'edad' : self.edad,
            'link_venta' : self.link_venta,
            'numero_contacto' : self.numero_contacto
        }

db.create_all()

@app.route('/test', methods=['GET'])
def test():
    return make_response(
        jsonify({
            'message' : 'test route'
        }),
        200
    )

#Dueños endpoints

@app.route('/duenos', methods=['POST'])
def create_dueno():
    try:
        data = request.get_json()
        new_dueno = Duenos(
            nombre=data['nombre'], 
            user=data['user'], 
            password=data['password'], 
            email=data['email']
        )
        db.session.add(new_dueno)
        db.session.commit()
        return make_response(
            jsonify({
                'message' : 'dueño creado'
            }),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al crear dueño'
            }),
            500
        )
    
@app.route('/duenos', methods=['GET'])
def get_duenos():
    try:
        duenos = Duenos.query.all()
        return make_response(
            jsonify(
                [dueno.json() for dueno in duenos]
            ),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer los dueños'
            }),
            500
        )

@app.route('/duenos/<int:id>', methods=['GET'])
def get_dueno(id):
    try:
        dueno = Duenos.query.filter_by(id=id).first()
        if dueno:
            return make_response(
                jsonify({
                    'dueño' : dueno.json()
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'dueño no enconrado'
            }),
            404
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer dueño'
            }),
            500
        )

@app.route('/duenos/<int:id>', methods=['PUT'])
def update_dueno(id):
    try:
        dueno = Duenos.query.filter_by(id=id).first()
        if dueno:
            data = request.get_json()
            dueno.nombre = data['nombre']
            dueno.user = data['user']
            dueno.password = data['password']
            dueno.email = data['email']
            db.session.commit()
            return make_response(
                jsonify({
                    'message' : 'dueño modificado'
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'dueño no encontrado'
            }),
            404
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer al dueño'
            }),
            500
        )

@app.route('/duenos/<int:id>', methods=['DELETE'])
def delete_dueno(id):
    try:
        dueno = Duenos.query.filter_by(id=id).first()
        if dueno:
            db.session.delete(dueno)
            db.session.commit()
            return make_response(
                jsonify({
                    'message' : 'dueño eliminado'
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'dueño no encontrado'
            }),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al eliminar el dueño'
            }),
            500
        )


#Discotecas endpoints

@app.route('/discotecas', methods=['POST'])
def create_discoteca():
    try:
        data = request.get_json()
        new_discoteca = Discotecas(
            duenos_id=data['duenos_id'],
            nombre=data['nombre'], 
            direccion=data['direccion'], 
            instagram=data['instagram']
        )
        db.session.add(new_discoteca)
        db.session.commit()
        return make_response(
            jsonify({
                'message' : 'discoteca creada'
            }),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al crear discoteca'
            }),
            500
        )
    
@app.route('/discotecas', methods=['GET'])
def get_discotecas():
    try:
        discotecas = Discotecas.query.all()
        return make_response(
            jsonify(
                [discoteca.json() for discoteca in discotecas]
            ),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer las discotecas'
            }),
            500
        )

@app.route('/discotecas/<int:id>', methods=['GET'])
def get_discoteca(id):
    try:
        discoteca = Discotecas.query.filter_by(id=id).first()
        if discoteca:
            return make_response(
                jsonify({
                    'discoteca' : discoteca.json()
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'discoteca no encontrada'
            }),
            404
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer discoteca'
            }),
            500
        )

@app.route('/discotecas/<int:id>', methods=['PUT'])
def update_discoteca(id):
    try:
        discoteca = Discotecas.query.filter_by(id=id).first()
        if discoteca:
            data = request.get_json()
            discoteca.dueno_id = data['duenos_id']
            discoteca.nombre = data['nombre']
            discoteca.direccion = data['direccion']
            discoteca.instagram = data['instagram']
            db.session.commit()
            return make_response(
                jsonify({
                    'message' : 'discoteca modificada'
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'discoteca no encontrada'
            }),
            404
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer la discoteca'
            }),
            500
        )

@app.route('/discotecas/<int:id>', methods=['DELETE'])
def delete_discoteca(id):
    try:
        discoteca = Discotecas.query.filter_by(id=id).first()
        if discoteca:
            db.session.delete(discoteca)
            db.session.commit()
            return make_response(
                jsonify({
                    'message' : 'discoteca eliminada'
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'discoteca no encontrada'
            }),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al eliminar discoteca'
            }),
            500
        )

#Eventos endpoints

@app.route('/eventos', methods=['POST'])
def create_evento():
    try:
        data = request.get_json()
        new_evento = Eventos(
            discotecas_id=data['discotecas_id'],
            nombre=data['nombre'], 
            fecha=data['fecha'], 
            genero_musical=data['genero_musical'],
            edad=data['edad'],
            link_venta=data['link_venta'],
            numero_contacto=data['numero_contacto']

        )
        db.session.add(new_evento)
        db.session.commit()
        return make_response(
            jsonify({
                'message' : 'evento creado'
            }),
            200
        )
    except Exception as e:
        print(e)
        return make_response(
            jsonify({
                'message' : 'error al crear evento',
            }),
            500
        )
    
@app.route('/eventos', methods=['GET'])
def get_eventos():
    try:
        eventos = Eventos.query.all()
        return make_response(
            jsonify(
                [evento.json() for evento in eventos]
            ),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer los eventos'
            }),
            500
        )

@app.route('/eventos/<int:id>', methods=['GET'])
def get_evento(id):
    try:
        evento = Eventos.query.filter_by(id=id).first()
        if evento:
            return make_response(
                jsonify({
                    'evento' : evento.json()
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'evento no encontrado'
            }),
            404
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer eventos'
            }),
            500
        )

@app.route('/eventos/<int:id>', methods=['PUT'])
def update_eventos(id):
    try:
        evento = Eventos.query.filter_by(id=id).first()
        if evento:
            data = request.get_json()
            evento.discotecas_id = data['discotecas_id']
            evento.nombre = data['nombre']
            evento.fecha = data['fecha']
            evento.genero_musical = data['genero_musical']
            evento.edad = data['edad']
            evento.link_venta = data['link_venta']
            evento.numero_contacto = data['numero_contacto']
            db.session.commit()
            return make_response(
                jsonify({
                    'message' : 'evento modificado'
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'evento no encontrado'
            }),
            404
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al traer el evento'
            }),
            500
        )

@app.route('/eventos/<int:id>', methods=['DELETE'])
def delete_evento(id):
    try:
        evento = Eventos.query.filter_by(id=id).first()
        if evento:
            db.session.delete(evento)
            db.session.commit()
            return make_response(
                jsonify({
                    'message' : 'evento eliminado'
                }),
                200
            )
        return make_response(
            jsonify({
                'message' : 'evento no encontrado'
            }),
            200
        )
    except:
        return make_response(
            jsonify({
                'message' : 'error al eliminar evento'
            }),
            500
        )









