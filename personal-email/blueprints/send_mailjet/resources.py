from mailjet_rest import Client
import os

from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import MailJet
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.customer.model import Customer
from blueprints.sent.model import Sent
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_mailjet = Blueprint('mailjet', __name__)
api = Api(bp_mailjet)

class MailJetResource(Resource):

    def sendMessage(self, fmail, fname, tmail, tname, subject, text, HTMLmessage):
        api_key = 'c678d961386dc4f4ca937db65790ae15'
        api_secret = '751173a0270f92eef81cfadfff9193f1'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        nama = fmail
        data = {
        'Messages': [
            {
            "From": {
                "Email": fmail,
                "Name": fname
            },
            "To": [
                {
                "Email": tmail,
                "Name": tname
                }
            ],
            "Subject": subject,
            "TextPart": text,
            "HTMLPart": HTMLmessage,
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code, result.json()
        
    
    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('fmail', location='json')
    #     parser.add_argument('fname', location='json')
    #     parser.add_argument('tmail', location='json')
    #     parser.add_argument('tname', location='json')
    #     parser.add_argument('subject', location='json')
    #     parser.add_argument('text', location='json')
    #     parser.add_argument('HTMLmessage', location='json')
    #     args = parser.parse_args()
        
    #     emailMessage = EmailMessage(args['fmail'], args['fname'], args['tmail'], args['tname'],
    #     args['subject'], args['text'],args['HTMLmessage'])
    #     db.session.add(emailMessage)
    #     db.session.commit()
    #     app.logger.debug('DEBUG: %s', args)

    #     return self.sendMessage(args['fmail'], args['fname'], args['tmail'], args['tname'],
    #     args['subject'], args['text'],args['HTMLmessage']), 200 

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry_sent = Sent.query.filter_by(user_id=claims['id']).first()
        print("=================================================")
        print(qry_sent)



api.add_resource(MailJetResource, '', '')