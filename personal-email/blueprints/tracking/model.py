from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class Track(db.Model):
    __tablename__ = "track"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    send_date = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    status = db.Column(db.String(50))
    subject = db.Column(db.String(2000))
    content = db.Column(db.Text, nullable= False)
    device = db.Column(db.String(50))
    contact_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    
    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'send_date': fields.DateTime,
        'status': fields.String,
        'subject': fields.String,
        'content': fields.String,
        'device' : fields.String,
        'contact_id': fields.Integer,
        'group_id': fields.Integer,
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
