from flask import request
from app import app, db
from app.models import Book, Response, User, UsersAndBooks
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from app.error_codes import ErrorCodes
from jwt import ExpiredSignatureError, InvalidTokenError

book_already_exists_message = "Book with same name and author already exists"


@app.route("/books", methods=['POST'])
def add_book():
    name = request.form['name']
    author = request.form['author']
    description = request.form['description']
    text_url = request.form['text_url']
    coef_love = request.form['coef_love']
    coef_fantastic = request.form['coef_fantastic']
    coef_fantasy = request.form['coef_fantasy']
    coef_detective = request.form['coef_detective']
    coef_adventure = request.form['coef_adventure']
    coef_art = request.form['coef_art']

    try:
        book = Book.query.filter_by(name=name).first()
        if book is None or not book.author == author:
            new_book = Book(name, author, description, text_url, coef_love, coef_fantastic, coef_fantasy,
                            coef_detective, coef_adventure, coef_art)
            db.session.add(new_book)
            db.session.commit()
            return Response.success_json()
        else:
            return Response(book_already_exists_message, False, ErrorCodes.bookAlreadyExists).to_json()
    except (SQLAlchemyError, DBAPIError) as e:
        return Response.error_json(e)


@app.route("/books/<book_id>/<token>", methods=['POST'])
def add_user_book(book_id, token):
    try:
        user_id = User.decode_auth_token(token)

        users_and_books = UsersAndBooks(user_id, book_id)
        db.session.add(users_and_books)
        db.session.commit()
        return Response.success_json()
    except IntegrityError:
        return Response("Book already exists or not found.", False, ErrorCodes.bookAlreadyExists).to_json()
    except SQLAlchemyError as e:
        return Response.error_json(e)
    except ExpiredSignatureError:
        return Response.expired_token_json()
    except InvalidTokenError:
        return Response.invalid_token_json()
