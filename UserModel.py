# from flask_sqlalchemy import SQLAlchemy
# from settings import app
#
# db = SQLAlchemy(app)
#
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(80), nullable=False)
#     userId = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return str({
#             'name': self.name,
#             'password': self.password,
#             'email': self.email,
#             'userId': self.userId
#         })
#
#     def username_password_match(_name, _password, _email, _userId):
#         user = User.query.filter_by(name=_name).filter_by(password=_password).filter_by(email=_email).filter_by(userId=_userId).first()
#         if user is None:
#             return False
#         else:
#             return True
#
#     def getAllUsers():
#         return User.query.all()
#
#     def createUser(_name, _password, _email, _userId):
#         new_user = User(name=_name, password=_password, email=_email, userId=_userId)
#         db.session.add(new_user)
#         db.session.commit()
