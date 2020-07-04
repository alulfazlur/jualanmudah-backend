from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class Sent(db.Model):
    __tablename__ = "sent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    send_date = db.Column(db.String(50))
    status = db.Column(db.String(50))
    subject = db.Column(db.String(2000))
    content = db.Column(db.Text, nullable= False)
    device = db.Column(db.String(50))
    contact_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    open_rate = db.Column(db.String(20))
    click_rate = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    track = db.relationship('Track', backref='sent', lazy=True)
    
    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'status': fields.String,
        'send_date': fields.String,
        'subject': fields.String,
        'content': fields.String,
        'device' : fields.String,
        'contact_id': fields.Integer,
        'group_id': fields.Integer,
        'open_rate': fields.Integer,
        'click_rate': fields.Integer,
        'total_count': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,

    }

    def __init__(self, user_id, status, send_date, subject, content, device, contact_id, group_id, open_rate, click_rate, total_count):
        self.user_id = user_id
        self.status = status
        self.send_date = send_date
        self.subject = subject
        self.content = content
        self.device = device  
        self.contact_id = contact_id
        self.group_id = group_id
        self.open_rate = open_rate
        self.click_rate = click_rate
        self.total_count = total_count

    def __repr__(self):
        return '<Sent %r>' % self.id
