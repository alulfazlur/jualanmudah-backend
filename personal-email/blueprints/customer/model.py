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

    def __init__(self, First_name, last_name,email):

        self.user_id = user_id
        self.contact_group_id = contact_group_id
        self.email_or_wa = email_or_wa
        
        

    def __repr__(self):
        return '<UserContact %r>' % self.id