from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, default=20)
    salt = db.Column(db.String(255))
    status =db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False) 
    position = db.Column(db.String(50), nullable=False)
    user_image =  db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    customer = db.relationship('Customer', backref='user', lazy=True)
    user_contact = db.relationship('UserContact', backref='user', lazy=True)

    response_fields = {
        'id': fields.Integer,
        'full_name': fields.String,
        'username': fields.String,
        'password': fields.String,
        'status': fields.Boolean,
        'address': fields.String,
        'position': fields.String,
        'user_image' : fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
      
    }
    jwt_claim_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'status': fields.String
    }
    def __init__(self, full_name, username,password,salt,status,address,position,user_image):
        
        self.full_name = full_name
        self.username = username
        self.password = password
        self.salt = salt
        self.status = status
        self.address = address
        self.position = position
        self.user_image = user_image

    def __repr__(self):
        return '<User %r>' % self.id
