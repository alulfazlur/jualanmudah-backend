from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class Sent(db.Model):
    __tablename__ = "sent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, autoincrement=True)
    member_id = db.Column(db.Integer, autoincrement=True)
    send_date = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    status = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(2000))
    reminder = db.Column(db.String(2000))
    content = db.Column(db.Text, nullable= False)
    device = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    send_mailjet = db.relationship('MailJet', backref='sent', lazy=True)
    

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'member_id': fields.Integer,
        'send_date': fields.DateTime,
        'status': fields.String,
        'subject': fields.String,
        'reminder': fields.String,
        'content': fields.String,
        'device' : fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
      
    }

    def __init__(self, user_id, member_id, status, subject, reminder, content,device):
        self.user_id = user_id
        self.member_id = member_id
        self.status = status
        self.subject = subject
        self.reminder = reminder
        self.content = content
        self.device = device   

    def __repr__(self):
        return '<Sent %r>' % self.id
