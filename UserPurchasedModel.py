# from BookModel import *
#
# db = SQLAlchemy(app)
#
# class UserPurchased(db.Model):
#     __tablename__ = 'userPurchased'
#     id = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, nullable=False)
#     bookId = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return str({
#             'userId': self.userId,
#             'bookId': self.bookId
#         })
#
#     def getAllBooksForUser(_bookId, _userId):
#         return [Book.query.filter_by(userId=_userId).filter_by(bookId=_bookId).all()]
#
