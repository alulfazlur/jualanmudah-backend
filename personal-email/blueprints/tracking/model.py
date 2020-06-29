from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class Track(db.Model):
    __tablename__ = "track"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sent_id = db.Column(db.Integer, db.ForeignKey('sent.id'))
    customer_id = db.Column(db.Integer)
    status_open = db.Column(db.String(50))
    status_click = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    
    response_fields = {
        'id': fields.Integer,
        'sent_id': fields.Integer,
        'customer_id':

        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,

    }

    def __init__(self, user_id, status, subject, content, device, contact_id, group_id):
        self.user_id = user_id
        self.status = status
        self.subject = subject
        self.content = content
        self.device = device  
        self.contact_id = contact_id
        self.group_id = group_id

    def __repr__(self):
        return '<Sent %r>' % self.id
