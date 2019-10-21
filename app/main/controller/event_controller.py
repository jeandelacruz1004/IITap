from flask import request
from flask_restplus import Resource

from ..util.dto import EventDto
from ..service.event_service import save_new_event, get_all_events, get_an_event

api = EventDto.api
_event = EventDto.event


@api.route('/event')
class EventList(Resource):
    @api.doc('list_of_created_events')
    @api.marshal_list_with(_event, envelope='data')
    def get(self):
        """List all created events"""
        return get_all_events()

    @api.response(201, 'Event successfully created.')
    @api.doc('create a new event')
    @api.expect(_event, validate=True)
    def post(self):
        """Creates a new Event """
        data = request.json
        return save_new_event(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Event identifier')
@api.response(404, 'Event not found.')
class Event(Resource):
    @api.doc('get an event')
    @api.marshal_with(_event)
    def get(self, public_id):
        """get an event given its identifier"""
        event = get_an_event(public_id)
        if not event:
            api.abort(404)
        else:
            return event