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
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(2000))
    bod = db.Column(db.DateTime)
    address = db.Column(db.String(2000))
    gender = db.Column(db.String(200))
    company =  db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # customer_member = db.relationship('CustomerMember', backref='customer', lazy=True)
    customer_member = db.relationship('CustomerMember', cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        'id': fields.Integer,
        'First_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'bod': fields.DateTime,
        'address': fields.String,
        'gender': fields.String,
        'company': fields.String,
        'user_id': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
      
    }

    def __init__(self, First_name, last_name, email, phone, bod, address, gender, company, user_id):

        self.First_name = First_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.bod = bod
        self.address = address
        self.gender = gender
        self.company = company
        self.user_id = user_id
        
        

    def __repr__(self):
        return '<Customer %r>' % self.id