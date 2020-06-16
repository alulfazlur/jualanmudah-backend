from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class UserContact(db.Model):
    __tablename__ = "user_contact"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,nullable= False)
    contact_group_id = db.Column(db.Integer,nullable= False)
    email_or_wa = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'contact_group_id': fields.Integer,
        'email_or_wa': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
      
    }

    def __init__(self, user_id, contact_group_id,email_or_wa):

        self.user_id = user_id
        self.contact_group_id = contact_group_id
        self.email_or_wa = email_or_wa
        
        

    def __repr__(self):
        return '<UserContact %r>' % self.id
