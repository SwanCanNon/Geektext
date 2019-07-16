from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bookId = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comments = db.Column(db.String(254), nullable=True)

    def json(self):
        return {'bookTitle': self.bookTitle, 'price': self.price, 'bookId': self.bookId, 'rating': self.rating, 'comments': self.comments}

    def add_book(_bookTitle, _price, _bookId, _rating, _comments):
        new_book = Book(bookTitle=_bookTitle, price=_price, bookId=_bookId, rating=_rating, comments=_comments)
        db.session.add(new_book)
        db.session.commit()

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def get_book(_bookId):
        return Book.json(Book.query.filter_by(bookId=_bookId).first())

    def delete_book(_bookId):
        is_successful = Book.query.filter_by(bookId=_bookId).delete()
        db.session.commit()
        return bool(is_successful)

    def update_book_price(_bookId, _price):
        book_to_update = Book.query.filter_by(bookId=_bookId).first()
        book_to_update.price = _price
        db.session.commit()

    def update_book_name(_bookId, _bookTitle):
        book_to_update = Book.query.filter_by(bookId=_bookId).first()
        book_to_update.bookTitle = _bookTitle
        db.session.commit()

    def update_book_rating(_bookId, _rating):
        book_to_update = Book.query.filter_by(bookId=_bookId).first()
        book_to_update.rating = _rating
        db.session.commit()

    def update_book_comments(_bookId, _comments):
        book_to_update = Book.query.filter_by(bookId=_bookId).first()
        book_to_update.comments = _comments
        db.session.commit()

    def replace_book(_bookId, _bookTitle, _price, _rating, _comments):
        book_to_replace = Book.query.filter_by(bookId=_bookId).first()
        book_to_replace.price = _price
        book_to_replace.bookTitle = _bookTitle
        book_to_replace.rating = _rating
        book_to_replace.comments = _comments
        db.session.commit()

    def __repr__(self):
        book_object = {
            'bookTitle': self.bookTitle,
            'price': self.price,
            'bookId': self.bookId,
            'rating': self.rating,
            'comments': self.comments
        }
        return json.dumps(book_object)

