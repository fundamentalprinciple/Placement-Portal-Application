from uuid import uuid4
from .database import db
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('admin','company','student'), nullable=False)
    
