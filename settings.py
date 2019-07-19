from flask import Flask, flash, render_template, redirect, make_response, request, url_for, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

import pymysql
import mysql.connector

pymysql.install_as_MySQLdb()
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user



# from UserModel import User
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '\xdf\xec\xf0e\x96@h\xa8\xc9\xf9\xbe\x0b\xac^\x0ci[\x17\xa6\xb8/H<\x94'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://testuser:test@localhost/geek_text"

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:YES@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:aa09@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bce5ce263e3ba7:1543b1ce@us-cdbr-iron-east-02.cleardb.net/heroku_e86cfb095c1e8fa"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


connection = mysql.connector.connect(host='localhost',
                                     database='geek_text',
                                     user='testuser',
                                     password='test')
