from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'rfID': fields.String(required=True, description='user ID address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class EventDto:
    api = Namespace('event', description='event related operations')
    event = api.model('event', {
        'eventName': fields.String(required=True, description='name of the event'),
        'eventDate': fields.String(required=True, description='date of the event'),
        'eventDescription': fields.String(required=True, description='event description'),
        'location': fields.String(required=True, description='event location'),
        'fee': fields.String(description='event fee'),
        'public_id': fields.String(description='event Identifier')
    })