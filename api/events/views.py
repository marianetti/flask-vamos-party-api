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

from ..models.events import Event
from ..models.users import User
from ..models.clubs import Club

from http import HTTPStatus

event_namespace = Namespace('events', description="namespace for events")

create_event_model = event_namespace.model(
    'Event', {
        'id' : fields.Integer(),
        'club' : fields.Integer(required=True, description="Club where the event is"),
        'name' : fields.String(required=True, description="Name of the event"),
        'date' : fields.String(required=True, description="Date of the event"),
        'style' : fields.String(required=True, description="Type of party"),
        'age' : fields.String(required=True, description="Minimum age for the event"),
        'buy_link' : fields.String(required=False, description="Where to buy the ticket for the event"),
        'contact' : fields.String(required=False, description="Phone number related to the event")
    }
)

update_event_model = event_namespace.model(
    'Event', {
        'name' : fields.String(required=True, description="Name of the event"),
        'date' : fields.String(required=True, description="Date of the event"),
        'style' : fields.String(required=True, description="Type of party"),
        'age' : fields.String(required=True, description="Minimum age for the event"),
        'buy_link' : fields.String(required=False, description="Where to buy the ticket for the event"),
        'contact' : fields.String(required=False, description="Phone number related to the event")
    }
)

return_event_model = event_namespace.model(
    'Event', {
        'id' : fields.Integer(),
        'club' : fields.Integer(required=True, description="Club where the event is"),
        'name' : fields.String(required=True, description="Name of the event"),
        'date' : fields.String(required=True, description="Date of the event"),
        'style' : fields.String(required=True, description="Type of party"),
        'age' : fields.String(required=True, description="Minimum age for the event"),
        'buy_link' : fields.String(required=False, description="Where to buy the ticket for the event"),
        'contact' : fields.String(required=False, description="Phone number related to the event")
    }
)

@event_namespace.route('/')
class GetCreate(Resource):
    """
        Get all events
    """
    @event_namespace.marshal_with(return_event_model)
    def get(self):
        try:
            events = Event.query.all()
            return events, HTTPStatus.OK
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    
    """
        Create new event
    """
    @event_namespace.expect(create_event_model)
    @event_namespace.marshal_with(return_event_model)
    @jwt_required()
    def post(self):

        data = event_namespace.payload

        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        current_club = Club.query.filter_by(user=current_user.id).first()
        print(current_club)

        new_event = Event(
            name=data['name'],
            date=data['date'],
            style=data['style'],
            age=data['age'],
            buy_link=data['buy_link'],
            contact=data['contact']
        )
        new_event.clubs = current_club
        new_event.save()

        return new_event, HTTPStatus.CREATED
 
    
@event_namespace.route('/event/<int:event_id>')
class GetUpdateDelete(Resource):

    """
        Get event by id
    """
    @event_namespace.marshal_list_with(return_event_model)
    @jwt_required()
    def get(self, event_id):

        event = Event.get_by_id(id=event_id)

        return event, HTTPStatus.OK


    """
        Update event by id
    """
    @event_namespace.expect(update_event_model)
    @event_namespace.marshal_list_with(return_event_model)
    @jwt_required()
    def put(self, event_id):
        try:
            event = Event.query.filter_by(id=event_id).first()
            if event:
                data = event_namespace.payload
                event.name = data['name']
                event.date = data['date']
                event.style = data['style']
                event.age = data['age']
                event.buy_link = data['buy_link']
                event.contact = data['contact']
                event.update()
                return event, HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        
    """
        Delete event by id
    """
    @jwt_required()
    def delete(self, event_id):
        try:
            event = Event.query.filter_by(id=id).first()
            if event:
                event.delete()
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        

