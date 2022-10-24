from flask import request
from flask_restx import Resource, Namespace
from flask_restx.reqparse import RequestParser

from dao.model.user import UserSchema
from implemented import user_service
from service.decorators import auth_required

user_ns = Namespace('users')
page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)


@user_ns.route('/')
class UsersView(Resource):

    def patch(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.update_user(data=data, refresh_token=header)

    def get(self):
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return UserSchema().dump(user_service.get_user_by_token(refresh_token=header))

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/password/')
class LoginView(Resource):
    @auth_required
    def put(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.update_password(data=data, refresh_token=header)
