# from BookModel import *
# from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
#
# db = SQLAlchemy(app)
#
# class BookRatings(db.Model):
#     __tablename__ = 'bookRatings'
#     id = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, nullable=False)
#     bookId = db.Column(db.Integer, nullable=False)
#     rating = db.Column(db.Integer)
#     comments = db.Column(db.String(254), nullable=True)
#
#     def __repr__(self):
#         return str({
#             'userId': self.userId,
#             'bookId': self.bookId,
#             'rating': self.rating,
#             'comments': self.comments
#         })
#
#
# def ratings_query():
#     return BookRatings.query()
#
# class BookRatingsForm(FlaskForm):
#     opts = QuerySelectField(query_factory=ratings_query, allow_blank=True)
#
#
# @app.route('/comments')
# def addcomments():
#     return render_template('comments.html')
#
#
#     # def getAllRatingsForBook(_bookId):
#     #     return [Book.json(book) for book in
#     #             (Book.query(Book.rating, Book.comments).filter_by(bookId=_bookId).all())]
#     #
#     #
#     # def getAllRatingsForBookForUser(_bookId, _userId):
#     #     return [Book.json(book) for book in
#     #             (db.session.query(Book, Book.rating, Book.comments).filter_by(bookId=_bookId).filter_by(userId=_userId).all())]
#
#
#
