from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), unique=True, nullable=False)
    last_name = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, default=20)
    salt = db.Column(db.String(255))
    internal = db.Column(db.Boolean, default=False, nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=False) 
    post = db.relationship('Post', backref='user', lazy=True)
    follow = db.relationship('Follow', backref='user', lazy=True)

    response_fields = {
        'id': fields.Integer,
        'first_name': fields.String,
        'last_name': fields.String,
        'username': fields.String,
        'password': fields.String,
        'email': fields.String,
        'internal': fields.Boolean,
      
    }
    jwt_claim_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'internal': fields.Boolean
    }
    def __init__(self, first_name,last_name, username,password,salt, email,internal):
        
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.salt = salt
        self.email = email
        self.internal = internal
        

    def __repr__(self):
        return '<User %r>' % self.id
