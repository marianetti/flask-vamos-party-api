from flask_restx import (
    Namespace, 
    Resource, 
    fields 
)
from flask import (
    request, 
    jsonify
)

from ..models.users import User
from ..utils import db

from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from http import HTTPStatus

user_namespace = Namespace('users', description="namespace for users")

create_user_model = user_namespace.model(
    'User', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description="Name of user"),
        'user' : fields.String(required=True, description="Username"),
        'password_hash' : fields.String(required=True, description="User password"),
        'email' : fields.String(required=True, description="User email")
    }
)

update_user_model = user_namespace.model(
    'User', {
        'name': fields.String(required=False, description="Name of user"),
        'email' : fields.String(required=False, description="User email")
    }
)

return_user_model = user_namespace.model(
    'User', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description="Name of user"),
        'user' : fields.String(required=True, description="Username"),
        'password_hash' : fields.String(required=True, description="User password"),
        'email' : fields.String(required=True, description="User email")
    }
)

@user_namespace.route('/users')
class GetCreate(Resource):
    """
        Get all users
    """
    def get(self):
        try:
            users = User.query.all()
            return jsonify([user.json() for user in users], HTTPStatus.OK)
            
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """
        Create new user
    """
    @user_namespace.expect(create_user_model)
    @user_namespace.marshal_with(return_user_model)
    def post(self):
        try:
            data = request.get_json()
            new_user = User(
                name=data['name'], 
                user=data['user'], 
                password_hash=generate_password_hash(data['password']), 
                email=data['email']
            )
            
            new_user.save()

            return jsonify(new_user, HTTPStatus.CREATED)
        
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

@user_namespace.route('/user/<int:id>')
class GetUpdateDelete(Resource):

    """
        Get user by id
    """
    def get(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                return jsonify({'user' : user.json()}, HTTPStatus.OK)
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """ 
        Update user by id
    """
    @user_namespace.expect(update_user_model)
    @user_namespace.marshal(return_user_model)
    def put(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                data = request.get_json()
                user.name = data['name']
                user.email = data['email']
                user.update()
                return jsonify(user, HTTPStatus.OK)
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    def delete(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                user.delete()
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

