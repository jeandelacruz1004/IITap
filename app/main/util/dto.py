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

    parser = api.parser()
    parser.add_argument('email', type=str, help='user email address', location='form')
    parser.add_argument('rfID', type=str, help='user id', location='form')
    parser.add_argument('username', type=str, help='user username', location='form')
    parser.add_argument('password', type=str, help='user password', location='form')
    parser.add_argument('public_id', type=str, help='user identifier', location='form')


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

    parser = api.parser()
    parser.add_argument('email', type=str, help='user email address', location='form')
    parser.add_argument('password', type=str, help='user password', location='form')

class EventDto:
    api = Namespace('event', description='event related operations')
    event = api.model('event', {
        'eventName': fields.String(required=True, description='event name'),
        'eventDate': fields.String(required=True, description='event date'),
        'priority': fields.String(required=True, description='event priority'),
        'eventDescription': fields.String(description='event description'),
        'location': fields.String(required=True, description='event location '),
        'fee': fields.String(required=True, description='event fee'),
        'host': fields.String(required=True, description='event host'),
        'public_id': fields.String(description='event Identifier')
    })

    parser = api.parser()
    parser.add_argument('eventName', type=str, help='event name', location='form')
    parser.add_argument('eventDate', type=str, help='event date', location='form')
    parser.add_argument('priority', type=str, help='event priority', location='form')
    parser.add_argument('eventDescription', type=str, help='event description', location='form')
    parser.add_argument('location', type=str, help='event location', location='form')
    parser.add_argument('fee', type=str, help='event fee', location='form')
    parser.add_argument('host', type=str, help='event host', location='form')
    parser.add_argument('public_id', type=str, help='event Identifier', location='form')