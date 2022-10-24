from flask import request
from flask_restx import Resource, Namespace
from flask_restx.reqparse import RequestParser

from dao.model.movie import MovieSchema
from implemented import movie_service
from service.decorators import auth_required, admin_required

movie_ns = Namespace('movies')
page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):

        all_movies = movie_service.get_all(**page_parser.parse_args())
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    @auth_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
