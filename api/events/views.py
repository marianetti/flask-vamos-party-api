from flask_restx import (
    Namespace, 
    Resource, 
    fields 
)
from flask import (
    request, 
    jsonify
)

from ..models.events import Event
from ..utils import db

from http import HTTPStatus

event_namespace = Namespace('events', description="namespace for events")

create_event_model = event_namespace.model(
    'Event', {
        'id' : fields.Integer(),
        'club_id' : fields.Integer(required=True, description="Club where the event is"),
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
        'club_id' : fields.Integer(required=True, description="Club where the event is"),
        'name' : fields.String(required=True, description="Name of the event"),
        'date' : fields.String(required=True, description="Date of the event"),
        'style' : fields.String(required=True, description="Type of party"),
        'age' : fields.String(required=True, description="Minimum age for the event"),
        'buy_link' : fields.String(required=False, description="Where to buy the ticket for the event"),
        'contact' : fields.String(required=False, description="Phone number related to the event")
    }
)

@event_namespace.route('/events')
class GetCreate(Resource):
    """
        Get all events
    """
    def get(self):
        try:
            events = Event.query.all()
            return jsonify([event.json() for event in events], HTTPStatus.OK)
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    
    """
        Create new event
    """
    @event_namespace.expect(create_event_model)
    @event_namespace.marshal_with(return_event_model)
    def post(self):
        try:
            data = request.get_json()
            new_event = Event(
                club_id=data['club_id'],
                name=data['name'],
                date=data['date'],
                style=data['style'],
                age=data['age'],
                buy_link=data['buy_link'],
                contact=data['contact']
            )
            new_event.save()
            return jsonify(new_event, HTTPStatus.CREATED)
        
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    
@event_namespace.route('/event/<int:id>')
class GetUpdateDelete(Resource):

    """
        Get event by id
    """
    def get(self, id):
        try:
            event = Event.query.filter_by(id=id).first()
            if event:
                return jsonify({'event' : event.json()}, HTTPStatus.OK)
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    
    """
        Update event by id
    """
    @event_namespace.expect(update_event_model)
    @event_namespace.marshal_with(return_event_model)
    def put(self, id):
        try:
            event = Event.query.filter_by(id=id).first()
            if event:
                data = request.get_json()
                event.name = data['name']
                event.date = data['date']
                event.style = data['style']
                event.age = data['age']
                event.buy_link = data['buy_link']
                event.contact = data['contact']
                event.update()
                return jsonify(event, HTTPStatus.OK)
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        
    """
        Delete event by id
    """
    def delete(self, id):
        try:
            event = Event.query.filter_by(id=id).first()
            if event:
                event.delete()
                return HTTPStatus.OK
            else:
                return HTTPStatus.NOT_FOUND
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        

