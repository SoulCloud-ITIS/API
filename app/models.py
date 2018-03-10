import jwt
import datetime

from app import app
from app import db, ma


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('user_email', db.String(120), unique=True)
    password = db.Column('user_password', db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<E-mail %r>' % self.email

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'password')


class ResponseSchema(ma.Schema):
    class Meta:
        fields = ('message', 'success', 'error_code')


class Response:
    schema = ResponseSchema()

    def __init__(self, message, success, error_code):
        self.message = message
        self.success = success
        self.error_code = error_code

    @staticmethod
    def success_json():
        response = Response('Success', True, 0)
        return Response.schema.jsonify(response)

    @staticmethod
    def error_json(error, error_code):
        response = Response(error.__str__, False, error_code)
        return Response.schema.jsonify(response)

    def to_json(self):
        return self.schema.jsonify(self)
