from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    favorite_genre = db.Column(db.String)



class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    password = fields.Str()
    role = fields.Str()
