from settings import db

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)
    authorName = db.Column(db.String(50))
    publisher = db.Column(db.String(128))
    genre = db.Column(db.String(32))

    def get_all_books():
        return Book.query.all()

    #
    # def get_book(_bookId):
    #     return Book.json(Book.query.filter_by(bookId=_bookId).first())
    #
    # def delete_book(_bookId):
    #     is_successful = Book.query.filter_by(bookId=_bookId).delete()
    #     db.session.commit()
    #     return bool(is_successful)
    #
    # def update_book_price(_bookId, _price):
    #     book_to_update = Book.query.filter_by(bookId=_bookId).first()
    #     book_to_update.price = _price
    #     db.session.commit()
    #
    # def update_book_name(_bookId, _bookTitle):
    #     book_to_update = Book.query.filter_by(bookId=_bookId).first()
    #     book_to_update.bookTitle = _bookTitle
    #     db.session.commit()
    #
    # def update_book_rating(_bookId, _rating):
    #     book_to_update = Book.query.filter_by(bookId=_bookId).first()
    #     book_to_update.rating = _rating
    #     db.session.commit()
    #
    # def update_book_comments(_bookId, _comments):
    #     book_to_update = Book.query.filter_by(bookId=_bookId).first()
    #     book_to_update.comments = _comments
    #     db.session.commit()
    #
    # def replace_book(_bookId, _bookTitle, _price, _rating, _comments):
    #     book_to_replace = Book.query.filter_by(bookId=_bookId).first()
    #     book_to_replace.price = _price
    #     book_to_replace.bookTitle = _bookTitle
    #     book_to_replace.rating = _rating
    #     book_to_replace.comments = _comments
    #     db.session.commit()
    #
    # def __repr__(self):
    #     book_object = {
    #         'image_path': self.image_path,
    #         'title': self.title,
    #         'description': self.description,
    #         'price': self.price,
    #         'authorName': self.authorName,
    #         'publisher': self.publisher,
    #         'genre': self.genre
    #     }
    #     return json.dumps(book_object)

    def __str__(self):
        return f"{self.title}"

