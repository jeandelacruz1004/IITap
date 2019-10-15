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
