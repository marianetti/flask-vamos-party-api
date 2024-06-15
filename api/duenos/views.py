from flask_restx import Namespace, Resource, jsonify, fields 
from flask import request

from ..models.duenos import Dueno
from ..utils import db

from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

duenos_namespace = Namespace('duenos', description="namespace para dueños")

create_duenos_model = duenos_namespace.model(
    'Dueno', {
        'id' : fields.Integer(),
        'nombre' : fields.String(required=True, description="Nombre dueño"),
        'user' : fields.String(required=True, description="Nombre de usuario"),
        'password_hash' : fields.String(required=True, description="Contraseña de usuario"),
        'email' : fields.String(required=True, description="Email de usuario")
    }
)

duenos_model = duenos_namespace.model(
    'Dueno', {
        'id' : fields.Integer(),
        'nombre' : fields.String(required=True, description="Nombre dueño"),
        'user' : fields.String(required=True, description="Nombre de usuario"),
        'password_hash' : fields.String(required=True, description="Contraseña de usuario"),
        'email' : fields.String(required=True, description="Email de usuario")
    }
)

@duenos_namespace.route('/duenos')
class GetCreate(Resource):

    def get(self):
        try:
            duenos = Dueno.query.all()
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
    
    @duenos_namespace.expect(create_duenos_model)
    @duenos_namespace.marshal_with()
    def post(self):
        try:
            data = request.get_json()
            new_dueno = Dueno(
                nombre=data['nombre'], 
                user=data['user'], 
                password_hash=generate_password_hash(data['password']), 
                email=data['email']
            )
            
            new_dueno.save()

            return new_dueno, HTTPStatus.CREATED
        
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

@duenos_namespace.route('/dueno/<int:dueno_id>')
class GetUpdateDelete(Resource):

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
