import jwt
import datetime
import simplejson

from app import app
from app import db, ma
from sqlalchemy.orm import relationship, backref
from app.error_codes import ErrorCodes
from marshmallow import fields


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('user_email', db.String(120), unique=True)
    password = db.Column('user_password', db.String(128))

    books = relationship("Book", secondary="users_and_books")
    genres = relationship("Genre", secondary="users_and_genres")

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
            raise
        except jwt.InvalidTokenError:
            raise


class BookSchema(ma.Schema):
    class Meta:
        json_module = simplejson
        fields = ('id', 'name', 'author', 'description', 'url')


class Book(db.Model):
    schema = BookSchema()
    schema_many = BookSchema(many=True)

    __tablename__ = "books"
    id = db.Column('book_id', db.Integer, primary_key=True)
    name = db.Column('book_name', db.String(120))
    author = db.Column('book_author', db.String(120))
    description = db.Column('book_description', db.Text())
    url = db.Column("book_url", db.Text())

    genres = relationship("Genre", secondary="coefficients")
    users = relationship("User", secondary="users_and_books")

    def __init__(self, name, author, description, url):
        self.name = name
        self.author = author
        self.description = description
        self.url = url


class UserAndBooksSchema(ma.Schema):
    book = fields.Nested(Book.schema)
    mark = fields.Boolean()


class UsersAndBooks(db.Model):
    schema = UserAndBooksSchema()

    __tablename__ = 'users_and_books'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    mark = db.Column(db.Boolean)

    user = relationship(User, backref=backref("users_and_books", cascade="all, delete-orphan"))
    book = relationship(Book, backref=backref("users_and_books", cascade="all, delete-orphan"))

    def __init__(self, user_id, book_id, mark=False):
        self.user_id = user_id
        self.book_id = book_id
        self.mark = mark


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

    @staticmethod
    def expired_token_json():
        return Response("Token expired. Please log in again.", False, ErrorCodes.tokenExpired).to_json()

    @staticmethod
    def invalid_token_json():
        return Response("Invalid token. Please log in again.", False, ErrorCodes.invalidToken).to_json()

    def to_json(self):
        return self.schema.jsonify(self)


class GenreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class Genre(db.Model):
    schema = GenreSchema()

    __tablename__ = "genres"
    id = db.Column("genre_id", db.Integer, primary_key=True)
    name = db.Column("genre_name", db.String(120))

    users = relationship("User", secondary="users_and_genres")
    books = relationship("Book", secondary="coefficients")

    def __init__(self, name):
        self.name = name


class UsersAndGenres(db.Model):
    __tablename__ = "users_and_genres"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), primary_key=True)

    user = relationship(User, backref=backref("users", cascade="all, delete-orphan"))
    genre = relationship(Genre, backref=backref("genres", cascade="all, delete-orphan"))

    def __init__(self, user_id, genre_id):
        self.user_id = user_id
        self.genre_id = genre_id


class Coefficient(db.Model):
    __tablename__ = "coefficients"
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), primary_key=True)
    value = db.Column("value", db.Numeric)

    book = relationship(Book, backref=backref("books", cascade="all, delete-orphan"))
    genre = relationship(Genre, backref=backref("genres_books", cascade="all, delete-orphan"))

    def __init__(self, book_id, genre_id, value):
        self.book_id = book_id
        self.genre_id = genre_id
        self.value = value
