import uuid
import datetime

from app.main import db
from app.main.model.event import Event


def save_new_event(data):
    event = Event.query.filter_by(eventName=data['eventName']).first()
    if not event:
        new_event = Event(
            public_id=str(uuid.uuid4()),
            eventName=data['eventName'],
            dateCreated=datetime.datetime.utcnow(),
            priority = data['priority'],
            eventDate=data['eventDate'],
            eventDescription=data['eventDescription'],
            location=data['location'],
            fee=data['fee']
            
        )
        save_changes(new_event)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Event already exists. Please Log in.',
        }
        return response_object, 409


def get_all_events():
    return Event.query.all()


def get_an_event(public_id):
    return Event.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()