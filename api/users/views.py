from flask_restx import (
    Namespace, 
    Resource, 
    fields 
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from flask import (
    request
)

from ..models.users import User

from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from werkzeug.exceptions import (
    Conflict,
    BadRequest
)
from http import HTTPStatus

user_namespace = Namespace('users', description="namespace for users")

create_user_model = user_namespace.model(
    'User', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description="Name of user"),
        'username' : fields.String(required=True, description="Username"),
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
        'username' : fields.String(required=True, description="Username"),
        'password_hash' : fields.String(required=True, description="User password"),
        'email' : fields.String(required=True, description="User email")
    }
)

login_user_model = user_namespace.model(
    'Login', {
        'email' : fields.String(requires=True, description='Email for login'),
        'password' : fields.String(required=True, description='Password for login')
    }
)


@user_namespace.route('/login')
class Login(Resource):

    @user_namespace.expect(login_user_model)
    def post(self):

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and (check_password_hash(user.password_hash, password)):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response={
                'access_token':access_token,
                'refresh_token':refresh_token
            }

            return response, HTTPStatus.OK

        raise BadRequest("Invalid Username or Password")
        


@user_namespace.route('/refresh')
class Refresh(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {
            'access_token' : access_token
        }, HTTPStatus.OK


@user_namespace.route('/')
class GetCreate(Resource):
    """
        Get all users
    """
    @user_namespace.marshal_with(return_user_model)
    @jwt_required()
    def get(self):
        try:
            users = User.query.all()
            return users, HTTPStatus.OK
            
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """
        Create new user
    """
    @user_namespace.expect(create_user_model)
    @user_namespace.marshal_with(return_user_model)
    @jwt_required()
    def post(self):
        try:
            data = user_namespace.payload
            new_user = User(
                name=data['name'], 
                username=data['username'], 
                password_hash=generate_password_hash(data['password_hash']), 
                email=data['email']
            )
            new_user.save()

            return new_user, HTTPStatus.CREATED
        
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

@user_namespace.route('/user/<int:user_id>')
class GetUpdateDelete(Resource):

    """
        Get user by id
    """
    @user_namespace.marshal_with(return_user_model)
    @jwt_required()
    def get(self, user_id):
        try:
            user = User.get_by_id(id=user_id)
            if user:
                return user, HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """ 
        Update user by id
    """
    @user_namespace.expect(update_user_model)
    @user_namespace.marshal_with(return_user_model)
    @jwt_required()
    def put(self, user_id):
        try:
            user = User.get_by_id(id=user_id)
            if user:
                data = request.get_json()
                user.name = data['name']
                user.email = data['email']
                user.update()
                return  user, HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    @jwt_required()
    def delete(self, user_id):
        try:
            user = User.get_by_id(id=user_id)
            if user:
                user.delete()
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

