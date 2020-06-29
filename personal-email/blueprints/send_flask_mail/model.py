from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Column

class FlaskMail(db.Model):
    __tablename__ = 'flaskmail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fmail = db.Column(db.String(2000))
    fname = db.Column(db.String(2000))
    tmail = db.Column(db.String(2000))
    tname = db.Column(db.String(2000))
    subject = db.Column(db.String(2000))
    text = db.Column(db.String(2000))
    HTMLmessage = db.Column(db.String(2000))
    sent_id = db.Column(db.Integer, db.ForeignKey('sent.id'))

    response_fields = {
        'id': fields.Integer,
        'fmail': fields.String,
        'fname': fields.String,
        'tmail': fields.String,
        'tname': fields.String,
        'subject': fields.String,
        'text': fields.String,
        'HTMLmessage': fields.String,
        # 'sent_id': fields.Integer
    }

    def __init__(self, fmail, fname, tmail, tname, subject, text, HTMLmessage):
        self.fmail = fmail
        self.fname = fname
        self.tmail = tmail
        self.tname = tname
        self.subject = subject
        self.text = text
        self.HTMLmessage = HTMLmessage
        # self.sent_id = sent_id
    
    def __repr__(self):
        return '<FlaskMail %r>' % self.id
