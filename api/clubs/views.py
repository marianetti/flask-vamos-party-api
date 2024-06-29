from flask_restx import (
    Namespace, 
    Resource,
    fields
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from flask import (
    request,
    jsonify
)

from ..models.clubs import Club
from ..models.users import User
from ..utils import db

from http import HTTPStatus

club_namespace = Namespace('clubs', description="namespace for clubs")

create_club_model = club_namespace.model(
    'Club', {
        'id' : fields.Integer(),
        'user' : fields.Integer(description="Club owner"),
        'name' : fields.String(required=True, description="Club name"),
        'address' : fields.String(required=True, description="Club address"),
        'instagram' : fields.String(required=False, description="Club instagram")
    }
)

update_club_model = club_namespace.model(
    'Club', {
        'name' : fields.String(required=False, description="Club name"),
        'address' : fields.String(required=False, description="Club address"),
        'instagram' : fields.String(required=False, description="Club instagram")
    }
)

return_club_model = club_namespace.model(
    'Club', {
        'id' : fields.Integer(),
        'user' : fields.Integer(required=True, description="Club owner"),
        'name' : fields.String(required=True, description="Club name"),
        'address' : fields.String(required=True, description="Club address"),
        'instagram' : fields.String(required=False, description="Club instagram")
    }
)

@club_namespace.route('/')
class GetCreate(Resource):
    """
        Return all clubs
    """
    @club_namespace.marshal_with(return_club_model)
    @jwt_required()
    def get(self):
        try:
            clubs = Club.query.all()
            return clubs, HTTPStatus.OK
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """
        Create new club
    """
    @club_namespace.expect(create_club_model)
    @club_namespace.marshal_with(return_club_model)
    @jwt_required()
    def post(self):
        # try:
        data = club_namespace.payload

        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first_or_404()
        new_club = Club(
            name=data['name'],
            address=data['address'],
            instagram=data['instagram'],
            #user=data['user']
        )
        new_club.users = current_user
        new_club.save()
        return new_club, HTTPStatus.CREATED
        
        # except Exception as e:
        #     return e, HTTPStatus.INTERNAL_SERVER_ERROR
        
@club_namespace.route('/clubs/<int:club_id>')
class GetUpdateDelete(Resource):

    """
        Get club by id
    """
    @club_namespace.marshal_with(return_club_model)
    @jwt_required()
    def get(self, club_id):
        try: 
            club = Club.get_by_id(id=club_id)
            if club:
                return club, HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    """
        Update club by id
    """
    @club_namespace.expect(update_club_model)
    @club_namespace.marshal_with(return_club_model)
    @jwt_required()
    def put(self, club_id):
        try:
            club = Club.get_by_id(id=club_id)
            if club:
                data = club_namespace.payload
                club.name = data['name']
                club.address = data['address']
                club.instagram = data['instagram']
                club.update()
                return club, HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """
        Delete club by id
    """
    @jwt_required()
    def delete(self, club_id):
        try:
            club = Club.get_by_id(id=club_id)
            if club:
                club.delete()
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        
