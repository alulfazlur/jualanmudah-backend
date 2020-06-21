from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    First_name = db.Column(db.String(2000))
    last_name = db.Column(db.String(2000))
    email = db.Column(db.String(200), unique=True, nullable=False)
    bod = db.Column(db.DateTime)
    address = db.Column(db.String(2000))
    gender = db.Column(db.String(200))
    company =  db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'First_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'bod': fields.DateTime,
        'address': fields.String,
        'gender': fields.String,
        'company': fields.String,
        'user_id': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
      
    }

    def __init__(self, First_name, last_name, email, bod, address, gender, company, user_id, created_at, updated_at):

        self.First_name = First_name
        self.last_name = last_name
        self.email = email
        self.bod = bod
        self.address = address
        self.gender = gender
        self.company = company
        self.last_name = last_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        
        

    def __repr__(self):
        return '<Customer %r>' % self.id