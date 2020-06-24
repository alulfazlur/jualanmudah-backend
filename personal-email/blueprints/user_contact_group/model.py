from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class UserContactGroup(db.Model):
    __tablename__ = "user_contact_group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    user_contact = db.relationship('UserContact', backref='user_contact_group', lazy=True)

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
      
    }

    def __init__(self, name):
        self.name = name
       
        
        

    def __repr__(self):
        return '<UserContactGroup %r>' % self.id
