from flask import Flask
from .db import db, migrate
from .models.books import Book
from .routes.book_routes import book_bp

#from .routes.hello_world_routes import hello_world_bp
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(book_bp)
#    app.register_blueprint(hello_world_bp)
    return app