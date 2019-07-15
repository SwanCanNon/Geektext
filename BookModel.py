from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

class Book(db.Model):
    __tablename__ = 'books'
