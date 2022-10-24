from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import genre_service, user_service
from service.auth import generate_token, approve_token

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get("email")
        password = req_json.get("password")

        if not email and password:
            return "что то не передано", 401

        user = user_service.get_by_email(email=email)
        if user:
            return generate_token(
                email=email,
                password=password,
                password_hash=email.password,
                is_refresh=False
            )

    def put(self):
        req_json = request.json

        if not req_json.get("refresh"):
            return "refresh_token не передан", 401

        return approve_token(
            token=req_json.get("refresh_token")
        ), 200


@auth_ns.route('/login')
class LoginView(Resource):
    def post(self):
        data = request.json

        if data.get('email') and data.get('password'):
            return user_service.check(data.get('email'), data.get('password')), 201

        else:
            return 'Что то пошло не так', 401


    def put(self):
        data = request.json

        if data.get('access_token') and data.get('refresh_token'):
            return user_service.update_token(data.get('refresh_token')), 201

        else:
            return 'Someone else', 401
