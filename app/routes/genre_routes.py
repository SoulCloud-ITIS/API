from app import app, db
from app.models import Genre, User, UsersAndGenres, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from jwt import ExpiredSignatureError, InvalidTokenError
from app.error_codes import ErrorCodes

USER_GENRES_CHECK_RESULT_MESSAGE = "User's genres check result"


@app.route("/genres", methods=['GET'])
def get_all_genres():
    genres = Genre.query.all()
    return Genre.schema.jsonify(genres, True)


@app.route("/genres/check/<token>")
def check_user_genres(token):
    try:
        user_id = User.decode_auth_token(token)
        user = User.query.get(user_id)
        if len(user.genres) == 0:
            return Response(USER_GENRES_CHECK_RESULT_MESSAGE, False, 0).to_json()
        else:
            return Response(USER_GENRES_CHECK_RESULT_MESSAGE, True, 0).to_json()
    except IntegrityError:
        return Response("Genre already exists", False, ErrorCodes.genreAlreadyExists).to_json()
    except SQLAlchemyError as e:
        return Response.error_json(e)
    except ExpiredSignatureError:
        return Response.expired_token_json()
    except InvalidTokenError:
        return Response.invalid_token_json()


@app.route("/genres/<genre_id>/<token>", methods=['POST'])
def set_user_genres(token, genre_id):
    try:
        user_id = User.decode_auth_token(token)
        user_and_genre = UsersAndGenres(user_id, genre_id)
        db.session.add(user_and_genre)
        db.session.commit()
        return Response.success_json()
    except IntegrityError:
        return Response("Genre already exists", False, ErrorCodes.genreAlreadyExists).to_json()
    except SQLAlchemyError as e:
        return Response.error_json(e)
    except ExpiredSignatureError:
        return Response.expired_token_json()
    except InvalidTokenError:
        return Response.invalid_token_json()
