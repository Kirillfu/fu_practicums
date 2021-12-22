from hashlib import sha256
from uuid import uuid4
from datetime import date

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

from users_storage import JSONUsersStorage

app = Flask(__name__)
api = Api(app)

users = JSONUsersStorage('users.json')

user_args_parser = reqparse.RequestParser().add_argument(
    'password', type=str, help='Password of the user is required',
    required=True
)


def abort_if_username_exists(username):
    if username in users:
        abort(409, message='User with this username is already exists')


def abort_if_username_not_exists(username):
    if username not in users:
        abort(404, message='Could not find user with this username')


def get_password_hash(password):
    salt = uuid4().hex
    return salt + sha256((password + salt).encode()).hexdigest()


class User(Resource):

    def get(self, username):
        abort_if_username_not_exists(username)
        return users[username]

    def put(self, username):
        abort_if_username_exists(username)
        password = user_args_parser.parse_args()['password']
        today = date.today()
        current_date = today.strftime("%d/%m/%Y")
        users[username] = {
            'password': get_password_hash(password),
            'registrationDate':current_date
        }
        return users[username], 201

    def delete(self, username):
        abort_if_username_not_exists(username)
        del users[username]
        return '', 204


api.add_resource(User, '/user/<string:username>')

if __name__ == '__main__':
    app.run()