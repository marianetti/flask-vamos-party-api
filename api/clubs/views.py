from flask_restx import (
    Namespace, 
    Resource,
    fields
)
from flask import (
    request,
    jsonify
)

from ..models.clubs import Club
from ..utils import db

from http import HTTPStatus

club_namespace = Namespace('clubs', description="namespace for clubs")

create_club_model = club_namespace.model(
    'Club', {
        'id' : fields.Integer(),
        'user_id' : fields.Integer(required=True, description="Club owner"),
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
        'user_id' : fields.Integer(required=True, description="Club owner"),
        'name' : fields.String(required=True, description="Club name"),
        'address' : fields.String(required=True, description="Club address"),
        'instagram' : fields.String(required=False, description="Club instagram")
    }
)

@club_namespace.route('/clubs')
class GetCreate(Resource):
    """
        Return all clubs
    """
    def get(self):
        try:
            clubs = Club.query.all()
            return jsonify([club.json() for club in clubs]), HTTPStatus.OK
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """
        Create new club
    """
    @club_namespace.expect(create_club_model)
    @club_namespace.marshal_with(return_club_model)
    def post(self):
        try:
            data = request.get_json()
            new_club = Club(
                user_id=data['user_id'],
                name=data['name'],
                address=data['address'],
                instagram=data['instagram']
            )

            new_club.save()
            return jsonify(new_club, HTTPStatus.CREATED)
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        
@club_namespace.route('/clubs/<int:id>')
class GetUpdateDelete(Resource):

    """
        Get club by id
    """
    def get(self, id):
        try: 
            club = Club.query.filter_by(id=id).first()
            if club:
                return jsonify({'club' : club.json()}, HTTPStatus.OK)
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    """
        Update club by id
    """
    @club_namespace.expect(update_club_model)
    @club_namespace.marshal_with(return_club_model)
    def put(self, id):
        try:
            club = Club.query.filter_by(id=id).first()
            if club:
                data = request.get_json()
                club.name = data['name']
                club.address = data['address']
                club.instagram = data['instagram']
                club.update()
                return jsonify(club, HTTPStatus.OK)
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    """
        Delete club by id
    """
    def delete(self, id):
        try:
            club = Club.query.filter_by(id=id).first()
            if club:
                club.delete()
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        
