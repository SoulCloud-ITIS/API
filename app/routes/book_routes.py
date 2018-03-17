from flask import request
from app import app, db
from app.models import Book, Response, User, UsersAndBooks
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from app.error_codes import ErrorCodes
from jwt import ExpiredSignatureError, InvalidTokenError
from app.helpers import BookWithMarks

book_already_exists_message = "Book with same name and author already exists"
BOOKS_PER_PAGE = 20


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


@app.route("/books", methods=["GET"])
@app.route("/books/<int:page>", methods=["GET"])
def get_books(page=1):
    books = Book.query.paginate(page, BOOKS_PER_PAGE, False).items
    return Book.schema.jsonify(books, True)


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


@app.route("/books/<token>", methods=['GET'])
def get_user_books(token):
    try:
        user_id = User.decode_auth_token(token)
        user = User.query.get(user_id)
        user_and_book_list = user.users_and_books

        books = [BookWithMarks(book.book, book.mark) for book in user_and_book_list]

        return BookWithMarks.schema.jsonify(books, True)
    except SQLAlchemyError as e:
        return Response.error_json(e)
    except ExpiredSignatureError:
        return Response.expired_token_json()
    except InvalidTokenError:
        return Response.invalid_token_json()
