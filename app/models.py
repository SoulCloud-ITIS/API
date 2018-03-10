import jwt
import datetime

from app import app
from app import db, ma
from sqlalchemy.orm import relationship, backref


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('user_email', db.String(120), unique=True)
    password = db.Column('user_password', db.String(128))

    books = relationship("Book", secondary="users_and_books")

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


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column('book_id', db.Integer, primary_key=True)
    name = db.Column('book_name', db.String(120))
    author = db.Column('book_author', db.String(120))
    description = db.Column('book_description', db.Text())
    text_url = db.Column('book_text_url', db.String(120))
    coef_love = db.Column('book_coef_love', db.Numeric())
    coef_fantastic = db.Column('book_coef_fantastic', db.Numeric())
    coef_fantasy = db.Column('book_coef_fantasy', db.Numeric())
    coef_detective = db.Column('book_coef_detective', db.Numeric())
    coef_adventure = db.Column('book_coef_adventure', db.Numeric())
    coef_art = db.Column('book_coef_art', db.Numeric())

    users = relationship("User", secondary="users_and_books")

    def __init__(self, name, author, description, text_url, coef_love, coef_fantastic, coef_fantasy, coef_detective,
                 coef_adventure, coef_art):
        self.name = name
        self.author = author
        self.description = description
        self.text_url = text_url
        self.coef_love = coef_love
        self.coef_fantastic = coef_fantastic
        self.coef_fantasy = coef_fantasy
        self.coef_detective = coef_detective
        self.coef_adventure = coef_adventure
        self.coef_art = coef_art


class UsersAndBooks(db.Model):
    __tablename__ = 'users_and_books'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    mark = db.Column(db.Boolean)

    user = relationship(User, backref=backref("users_and_books", cascade="all, delete-orphan"))
    book = relationship(Book, backref=backref("users_and_books", cascade="all, delete-orphan"))


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
    def error_json(error, error_code=500):
        response = Response(error.__str__, False, error_code)
        return Response.schema.jsonify(response)

    def to_json(self):
        return self.schema.jsonify(self)
