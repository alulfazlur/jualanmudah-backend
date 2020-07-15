from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class SentWhatsapp(db.Model):
    __tablename__ = "sent_whatsapp"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.Text, nullable= False)
    contact_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    total_sent = db.Column(db.Integer, default=0)
    list_phone = db.Column(db.String(5000))
    created_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    
    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'content': fields.String,
        'contact_id': fields.Integer,
        'group_id': fields.Integer,
        'total_sent': fields.Integer,
        'list_phone': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,

    }

    def __init__(self, user_id, content, contact_id, group_id, total_sent, list_phone):
        self.user_id = user_id
        self.content = content 
        self.contact_id = contact_id
        self.group_id = group_id
        self.total_sent = total_sent
        self.list_phone = list_phone

    def __repr__(self):
        return '<Sent %r>' % self.id
