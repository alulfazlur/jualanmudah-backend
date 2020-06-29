from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Column

class EmailMessage(db.Model):
    __tablename__ = 'table_email__message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_email = db.Column(db.String(2000))
    subject_email = db.Column(db.String(2000))
    message_email = db.Column(db.String(2000))

    response_fields = {
        'id': fields.Integer,
        'customer_email': fields.String,
        'subject_email': fields.String,
        'message_email': fields.String,
    }

    def __init__(self, customer_email, subject_email, message_email):
        self.customer_email = customer_email
        self.subject_email = subject_email
        self.message_email = message_email
    
    def __repr__(self):
        return '<EmailMessage %r>' % self.id
