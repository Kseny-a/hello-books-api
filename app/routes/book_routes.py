from flask import Blueprint, abort, make_response
#from app.models.books import books

book_bp = Blueprint("book_bp", __name__, url_prefix="/books")

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

        
