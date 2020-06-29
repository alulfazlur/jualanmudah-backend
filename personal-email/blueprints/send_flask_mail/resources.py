from mailjet_rest import Client
import os
from flask_mail import Message
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import FlaskMail
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.customer.model import Customer
from blueprints.sent.model import Sent
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints import app
from flask_mail import Mail


bp_flaskmail = Blueprint('flaskmail', __name__)
api = Api(bp_flaskmail)

class FlaskMailResource(Resource):

    def sendMessage(self, fmail, tmail, subject, text, HTMLmessage):
        app.config.update(dict(
            DEBUG = True,
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 587,
            MAIL_USE_TLS = True,
            MAIL_USE_SSL = False,
            MAIL_USERNAME = 'jinadabf@gmail.com',
            MAIL_PASSWORD = 'bountyhunter',
        ))
        mail = Mail(app)
        msg = Message(subject, sender = fmail, recipients = [tmail])
        msg.body = text
        msg.html = HTMLmessage
        mail.send(msg)
        return "Sent"
            
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fmail', location='json')
        parser.add_argument('fname', location='json')
        parser.add_argument('tmail', location='json')
        parser.add_argument('tname', location='json')
        parser.add_argument('subject', location='json')
        parser.add_argument('text', location='json')
        parser.add_argument('HTMLmessage', location='json')
        args = parser.parse_args()
        
        emailMessage = FlaskMail(args['fmail'], args['fname'], args['tmail'], args['tname'],
        args['subject'], args['text'],args['HTMLmessage'])
        db.session.add(emailMessage)
        db.session.commit()
        app.logger.debug('DEBUG: %s', args)

        return self.sendMessage(args['fmail'], args['tmail'],
        args['subject'], args['text'],args['HTMLmessage']), 200 


api.add_resource(FlaskMailResource, '', '')