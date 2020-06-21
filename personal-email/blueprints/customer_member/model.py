from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

class CustomerMember(db.Model):
    __tablename__ = "customer_member"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'customer_id': fields.Integer,
        'group_id': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, customer_id, group_id, created_at, updated_at):

        self.customer_id = customer_id
        self.group_id = group_id
        self.created_at = created_at
        self.updated_at = updated_at
        
        

    def __repr__(self):
        return '<CustomerMember %r>' % self.id