from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return str({
            'name': self.name,
            'password': self.password,
            'email': self.email
        })

    def username_password_match(_name, _password, _email):
        user = User.query.filter_by(name=_name).filter_by(password=_password).filter_by(email=_email).first()
        if user is None:
            return False
        else:
            return True

    def getAllUsers():
        return User.query.all()

    def createUser(_name, _password, _email):
        new_user = User(name=_name, password=_password, email=_email)
        db.session.add(new_user)
        db.session.commit()
