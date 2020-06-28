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

    # fungsi buat get mail dari mailjet by mailjet_id
    def getMailFromMailjet(self, mailjet_id):
        api_key = '13601c8ae59de0bbcfedc3658f3376f1'
        api_secret = 'b627d9619dd1e5c1f25b9b33ad684c5f'
        mailjet = Client(auth=(api_key, api_secret), version='v3')
        result = mailjet.message.get(1152921508360793791)
        return result.status_code, result.json()

    # fungsi untuk get list draft
    @internal_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry = Sent.query.filter_by(user_id=claims['id']).all()
        rows = []

        # get list sent, customer group, customer
        if qry is not None:
            for sent in qry:
                qry_member = CustomerMember.query.filter_by(group_id=sent.group_id)
                qry_member_cus = CustomerMember.query.filter_by(group_id=sent.group_id).first()
                array_customer = []
                for customer in qry_member:
                    customer = Customer.query.filter_by(id=customer.customer_id).first()
                    customer = marshal(customer, Customer.response_fields)
                    array_customer.append(customer)
                qry_group = CustomerGroup.query.filter_by(id=qry_member_cus.group_id).first()
                marshal_group = marshal(qry_group, CustomerGroup.response_fields)
                sent = marshal(sent, Sent.response_fields)
                sent['group_customer'] = marshal_group
                sent['customer'] =array_customer
                rows.append(sent)
                

                #========================================================home work++++++++++++++++++++++++++++++++++++++++++++++++++
                # menghitung rating open, clicked
                opened = 0
                clicked = 0
                sent = 0
                sent.mailjet_id
                list_mail = qry_sent.mailjet_id
                list_mail_id = list_mail.split('#')
                for index in range(0, len(list_mail_id)):
                    result = self.getMailFromMailjet(int(list_mail_id[index]))
                    status = result['Data'][0]['Status']
                    if status == "opened" or status == "clicked":
                        opened += 1
                    elif status == "clicked":
                        clicked += 1
                    elif status == "sent" or status == "opened" or status == "clicked":
                        sent += 1

            return rows, 200
        return {'status': 'NOT_FOUND'}, 404

    # fungsi untuk mengirim email melalui mailjet
    # FMAIL = MAIL_USERNAME
    def sendMessage(self, fmail, fname, tmail, tname, subject, text, HTMLmessage):
        app.config.update(dict(
            DEBUG = True,
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 587,
            MAIL_USE_TLS = True,
            MAIL_USE_SSL = False,
            MAIL_USERNAME = fmail,
            MAIL_PASSWORD = 'bountyhunter',
        ))
        mail = Mail(app)
        msg = Message(subject, sender = fmail, recipients = [tmail])
        msg.body = text
        msg.html = HTMLmessage
        mail.send(msg)
        return "Sent"
    

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
        app.config.update(dict(
            DEBUG = True,
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 587,
            MAIL_USE_TLS = True,
            MAIL_USE_SSL = False,
            MAIL_USERNAME = fmail,
            MAIL_PASSWORD = 'bountyhunter',
        ))
        mail = Mail(app)
        msg = Message(subject, sender = fmail, recipients = [tmail])
        msg.body = text
        msg.html = HTMLmessage
        mail.send(msg)
        return "Sent"

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

        # mengirim email ke customer satu per satu
        for member in qry_sent_member:
            customer = Customer.query.filter_by(id=member.customer_id).first()
            marshalcustomer = marshal(customer, Customer.response_fields)
            result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name']
            , marshalcustomer['email'], marshalcustomer['First_name'], args['subject']
            , args['reminder'], args['content'])

        # menyimpan ke databases
        status = "sent"
        sent = Sent(user_id, args['member_id'], status, args['subject']
        , args['reminder'], args['content'], args['device'], args['contact_id'], args['group_id'])
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


class getTrackingMail(Resource):

    # fungsi buat get mail dari mailjet by mailjet_id
    def getMailFromMailjet(self, mailjet_id):
        api_key = '13601c8ae59de0bbcfedc3658f3376f1'
        api_secret = 'b627d9619dd1e5c1f25b9b33ad684c5f'
        mailjet = Client(auth=(api_key, api_secret), version='v3')
        result = mailjet.message.get(1152921508360793791)
        return result.status_code, result.json()

    # fungsi untuk get list sent all mail dari  mailjet
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='args')
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        claims = get_jwt_claims()
        qry_sent = Sent.query.filter_by(user_id=claims['id'])
        qry_sent = qry_sent.filter_by(id=args['sent_id']).first()
        list_mail = qry_sent.mailjet_id
        list_mail_id = list_mail.split('#')

        rows = []
        for index in range(1, args['rp']):
            row = self.getMailFromMailjet(int(list_mail_id[index]))
            rows.append(row)

        return rows, 200


api.add_resource(SentResource, '', '/<id>')
api.add_resource(SendMailDirect, '/direct', '/<id>')
api.add_resource(getDraftById, '/draft', '<id>')
api.add_resource(getTrackingMail, '/tracking', '<id>')