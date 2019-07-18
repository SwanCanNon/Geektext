from settings import db
from BookModel import Book


class BookRatingsAndComments(db.Model):
    __tablename__ = 'bookRatings'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    bookId = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)
    comments = db.Column(db.String(254), nullable=True)

    def __repr__(self):
        return str({
            'userId': self.userId,
            'bookId': self.bookId,
            'rating': self.rating,
            'comments': self.comments
        })


def get_all_ratings_for_book(_bookId):
    return BookRatingsAndComments.query.filter_by(bookId=_bookId).first()


def add_rating_and_comment(_userId, _bookId, _rating, _comments):
    new_rating_and_comment = BookRatingsAndComments(userId=_userId, bookId=_bookId, rating=_rating, comments=_comments)
    db.session.add(new_rating_and_comment)
    db.session.commit()

# def getAllRatingsForBookForUser(_bookId, _userId):
#     list_of_comments = Book.get_all_books().query.filter_by(userId=_userId)
#     return



