from flask import Flask, flash, render_template, redirect, make_response, request, url_for, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user

from BookModel import *
import json


import jwt, datetime
# from UserModel import User
from functools import wraps

# from BookRatingsModel import BookRatings
# from UserPurchasedModel import UserPurchased

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://testuser:test@localhost/geek_text"

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:YES@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:aa09@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bce5ce263e3ba7:1543b1ce@us-cdbr-iron-east-02.cleardb.net/heroku_e86cfb095c1e8fa"

db = SQLAlchemy(app)
migrate = Migrate(app, db)