from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Sent
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact.model import UserContact
from blueprints.user_contact_group.model import UserContactGroup
from blueprints.customer.model import Customer
from blueprints.customer_group.model import CustomerGroup
from blueprints.customer_member.model import CustomerMember
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

from mailjet_rest import Client
import os



bp_sent = Blueprint('sent', __name__)
api = Api(bp_sent)


class SentResource(Resource):

    # fungsi untuk mengirim email melalui mailjet
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

    # fungsi untuk get list draft
    @internal_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry = Sent.query.filter_by(user_id=claims['id']).all()
        rows = []
        if qry is not None:
            for sent in qry:
                rows.append(marshal(sent, Sent.response_fields))
            return rows, 200
        return {'status': 'NOT_FOUND'}, 404

    # fungsi untuk mengirim email dari draft
    @internal_required
    def patch(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='json')
        # parser.add_argument('user_id', location='json')
        parser.add_argument('member_id', location='json')
        # parser.add_argument('status', location='json', required=True, choices=['draft', 'sent'])
        parser.add_argument('subject', location='json')
        parser.add_argument('reminder', location='json')
        parser.add_argument('content', location='json')
        parser.add_argument('device', location='json')
        parser.add_argument('contact_id', location='json')
        parser.add_argument('group_id', location='json')  

        args = parser.parse_args()
        claims = get_jwt_claims()
        qry_sent = Sent.query.filter_by(user_id=claims['id'])
        qry = qry_sent.filter_by(id=args['sent_id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            qry.sent_id = args['sent_id']
            qry.user_id = claims['id']
            qry.member_id = args['member_id']
            qry.status = "sent"
            qry.subject = args['subject']
            qry.reminder = args['reminder']
            qry.content = args['content']
            qry.device = args['device']
            qry.contact_id = args['contact_id']
            qry.group_id = args['group_id']

            db.session.commit()

            # menentukan user nama pengirim email
            user = User.query.filter_by(id=claims['id']).first()
            marshaluser = marshal(user, User.response_fields)

            # menentukan content dari tabel sent
            # qry_sent = Sent.query.filter_by(user_id=claims['id'])
            # sent = qry_sent.filter_by(id=marshaluser['id']).first()
            # marshalsent= marshal(sent, Sent.response_fields)

            # menentukan email user contact mail
            to_mail = UserContact.query.filter_by(user_id=claims['id'])
            to_mail = to_mail.filter_by(contact_group_id=args['contact_id']).first()
            marshaluserMail= marshal(to_mail, UserContact.response_fields)
        
            # menentukan email customer
            qry_customer = Customer.query.filter_by(user_id=claims['id']).first()
            qry_sent_member = CustomerMember.query.filter_by(id=args['member_id'])
            qry_sent_member = qry_sent_member.filter_by(customer_id=qry_customer.id)
            qry_sent_member = qry_sent_member.filter_by(group_id=args['group_id'])
            
            # mengirim email ke customer satu per satu
            for member in qry_sent_member:
                customer = Customer.query.filter_by(id=member.customer_id).first()
                marshalcustomer = marshal(customer, Customer.response_fields)
                result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name']
                , marshalcustomer['email'], marshalcustomer['First_name'], args['subject']
                , args['reminder'], args['content'])
                print("==============================================================")
                print(result)

            return marshal(qry, Sent.response_fields), 200
            

    # post draft
    @internal_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        parser.add_argument('member_id', location='json')
        # parser.add_argument('status', location='json', required=True, choices=['draft', 'sent'])
        parser.add_argument('subject', location='json')
        parser.add_argument('reminder', location='json')
        parser.add_argument('content', location='json')
        parser.add_argument('device', location='json')
        parser.add_argument('contact_id', location='json')
        parser.add_argument('group_id', location='json')
        args = parser.parse_args()
        
        claims = get_jwt_claims()
        user_id = User.query.filter_by(id=claims['id']).first()
        user_id = user_id.id

        status = "draft"
        mailjet_id = ""
        sent = Sent(user_id, args['member_id'], status, args['subject'], args['reminder'], 
        args['content'], args['device'], args['contact_id'], args['group_id'], mailjet_id)

        db.session.add(sent)
        db.session.commit()

        app.logger.debug('DEBUG : %s', sent)
        return marshal(sent, Sent.response_fields), 200, {'Content-Type': 'application/json'}

    
    # @internal_required
    def delete(self, id):
        qry = Sent.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200

class SendMailDirect(Resource):

    # fungsi untuk mengirim email melalui mailjet
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

    # post dan langsung dikirim melalui mailjet
    @internal_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=True)
        parser.add_argument('member_id', location='json', required=True)
        parser.add_argument('subject', location='json', required=True)
        parser.add_argument('reminder', location='json', required=True)
        parser.add_argument('content', location='json', required=True)
        parser.add_argument('device', location='json', required=True)
        parser.add_argument('contact_id', location='json', required=True)
        parser.add_argument('group_id', location='json', required=True)
        args = parser.parse_args()
        
        claims = get_jwt_claims()
        user = User.query.filter_by(id=claims['id']).first()
        user_id = user.id

        # menentukan user nama pengirim email
        marshaluser = marshal(user, User.response_fields)
        
        # menentukan email user contact mail
        to_mail = UserContact.query.filter_by(user_id=claims['id'])
        to_mail = to_mail.filter_by(contact_group_id=args['contact_id']).first()
        marshaluserMail= marshal(to_mail, UserContact.response_fields)
        
        # menentukan email customer
        qry_customer = Customer.query.filter_by(user_id=claims['id']).first()
        qry_sent_member = CustomerMember.query.filter_by(id=args['member_id'])
        qry_sent_member = qry_sent_member.filter_by(customer_id=qry_customer.id)
        qry_sent_member = qry_sent_member.filter_by(group_id=args['group_id'])
        
        # field mailjet_id yang akan disimpan
        mailjet_id = ""

        # mengirim email ke customer satu per satu
        for member in qry_sent_member:
            customer = Customer.query.filter_by(id=member.customer_id).first()
            marshalcustomer = marshal(customer, Customer.response_fields)
            result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name']
            , marshalcustomer['email'], marshalcustomer['First_name'], args['subject']
            , args['reminder'], args['content'])

            # resultdummy = {
            #         "Messages": [
            #             {
            #             "Status": "success",
            #             "To": [
            #                 {
            #                 "Email": "passenger1@mailjet.com",
            #                 "MessageUUID": "123",
            #                 "MessageID": 456,
            #                 "MessageHref": "https://api.mailjet.com/v3/message/456"
            #                 }
            #             ]
            #             }
            #         ]
            #         }
            # message_id = str(resultdummy['Messages'][0]['To'][0]['MessageID'])

             # mengamabil MessageID mailjet
            message_id = str(result['Messages'][0]['To'][0]['MessageID'])
            mailjet_id +=  "#" + message_id + "#"
        
        # menyimpan ke databases
        status = "sent"
        sent = Sent(user_id, args['member_id'], status, args['subject']
        , args['reminder'], args['content'], args['device'], args['contact_id'], args['group_id'], mailjet_id)
        db.session.add(sent)
        db.session.commit()

        app.logger.debug('DEBUG : %s', sent)
        return marshal(sent, Sent.response_fields), 200

class getDraftById(Resource):

    # fungsi untuk get draft by id
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('draft_id', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()

        qry_sent = Sent.query.filter_by(user_id=claims['id'])
        qry_draft = qry_sent.filter_by(id=args['draft_id']).first()

        if qry_draft is not None:
            return marshal(qry_draft, Sent.response_fields), 200
        return {'status': 'NOT FOUND'}, 404



api.add_resource(SentResource, '', '/<id>')
api.add_resource(SendMailDirect, '/direct', '/<id>')
api.add_resource(getDraftById, '/draft', '<id>')