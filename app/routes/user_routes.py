from flask import request
from app import app, db
from app.models import User, UserSchema, Response
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.error_codes import ErrorCodes
import hashlib

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/registration", methods=["POST"])
def reg_user():
    email = request.form['email']
    password = request.form['password']

    md5 = hashlib.md5()
    md5.update(password.encode("UTF-8"))

    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email, md5.hexdigest())
        try:
            db.session.add(new_user)
            db.session.commit()

            auth_token = new_user.encode_auth_token()
            if auth_token:
                return Response(auth_token, True, 0).to_json()

            return Response("Error generating token", False, ErrorCodes.generateTokenError).to_json()
        except (SQLAlchemyError, DBAPIError) as e:
            return Response.error_json(e, ErrorCodes.internalError)
    else:
        return Response('User already exists', False, ErrorCodes.userAlreadyExists).to_json()


@app.route("/login", methods=["POST"])
def login_user():
    email = request.form['email']
    password = request.form['password']

    md5 = hashlib.md5()
    md5.update(password.encode("UTF-8"))

    try:
        user = User.query.filter_by(email=email).first()
        if user is None or not user.password == md5.hexdigest():
            return Response("Invalid email or password", False, ErrorCodes.userNotFoundError).to_json()
        auth_token = user.encode_auth_token()
        if auth_token:
            return Response(auth_token.decode(), True, 0).to_json()
    except Exception as e:
        print(e)
        return Response.error_json(e, ErrorCodes.internalError)
