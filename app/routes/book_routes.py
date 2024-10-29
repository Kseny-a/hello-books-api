from flask import Blueprint, abort, make_response, request
from app.models.books import Book
from ..db import db


book_bp = Blueprint("book_bp", __name__, url_prefix="/books")

@book_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    
    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201


@book_bp.get("")
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description,
                }
        )
    return books_response

@book_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

def validate_book(book_id):

    try:
        book_id = int(book_id)
    except:
        response = {"message": f"Book {book_id} invalid."} 
        abort(make_response(response, 400))


    query = db.select(Book).where(Book.id==book_id)
    book = db.session.scalar(query)

    if not book:
        response = {"message": f"Book {book_id} not found."} 
        abort(make_response(response, 404))

    return book    


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

        
