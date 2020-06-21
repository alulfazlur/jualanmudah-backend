from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

class CustomerGroup(db.Model):
    __tablename__ = "customer_group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    customer_member = db.relationship('CustomerMember', backref='customer_group', lazy=True)


    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, name, created_at, updated_at):

        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        
        

    def __repr__(self):
        return '<CustomerGroup %r>' % self.id