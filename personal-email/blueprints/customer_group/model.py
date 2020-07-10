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
    user_id = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    customer_member = db.relationship('CustomerMember', backref='customer_group', lazy=True)


    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'user_id': fields.Integer,
        'status': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, name, user_id, status):

        self.name = name
        self.user_id = user_id  
        self.status = status   

    def __repr__(self):
        return '<CustomerGroup %r>' % self.id