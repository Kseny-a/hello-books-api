from flask import Blueprint, abort, make_response, request, Response
from app.models.books import Book
from ..db import db
from .route_utilities import validate_model


bp = Blueprint("book_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    try:

        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))    

    db.session.add(new_book)
    db.session.commit()
    response = new_book.to_dict()

    # response = {
    #     "id": new_book.id,
    #     "title": new_book.title,
    #     "description": new_book.description,
    # }
    return response, 201


@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()
# {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }

@bp.get("")
def get_all_books():
    # create a basic select query without any filtering
    query = db.select(Book)

    # If we have a `title` query parameter, we can add on to the query object
    title_param = request.args.get("title")
    if title_param:
        # Match the title_param exactly, including capitalization
        # query = query.where(Book.title == title_param)

        # If we want to allow partial matches, we can use the % wildcard with `like()`
        # If `title_param` contains "Great", the code below will match 
        # both "The Great Gatsby" and "Great Expectations"
        # query = query.where(Book.title.like(f"%{title_param}%"))

        # If we want to allow searching case-insensitively, 
        # we can use ilike instead of like
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    # If we have other query parameters, we can continue adding to the query. 
    # As we did above, we must reassign the `query`` variable to capture the new clause we are adding. 
    # If we don't reassign `query``, we are calling the `where` function but are not saving the resulting filter
    description_param = request.args.get("description")
    if description_param:
        # In case there are books with similar titles, we can also filter by description
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    books = db.session.scalars(query.order_by(Book.id))
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return books_response


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# @book_bp.get("")

# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description,})
        
#     return books_response

# @book_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book_id(book_id)
#     return {
#             "id": book.id,
#             "title": book.title,
#             "description": book.description,}


# def validate_book_id(book_id):
#     try:
#         book_id == int(book_id)
#     except ValueError:
#         response = {"message": f"Book {book_id} invalid."} 
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book
#     response = {"message": f"Book {book_id} not found."}  

#     abort(make_response(response, 404))

        
