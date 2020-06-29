from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Sent
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact.model import UserContact
from blueprints.user_contact_group.model import UserContactGroup
from blueprints.customer.model import Customer
from blueprints.customer_group.model import CustomerGroup
from blueprints.customer_member.model import CustomerMember
from blueprints.tracking.model import Track
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints import app
from flask_mail import Mail
from flask_mail import Message

from mailjet_rest import Client
import os



bp_sent = Blueprint('sent', __name__)
api = Api(bp_sent)


class SentResource(Resource):

    # get all list draft and sent email
    @staff_required
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
            return rows, 200
        return {'status': 'NOT_FOUND'}, 404

    # fungsi untuk mengirim email melalui mailjet
    @staff_required
    def sendMessage(self, fmail, fname, tmail, tname, subject, HTMLmessage):
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
        msg.html = HTMLmessage
        mail.send(msg)
        return "Sent"
    

    # send an email from draft
    @staff_required
    def patch(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='json')
        parser.add_argument('subject', location='json')
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
            qry.status = "sent"
            qry.subject = args['subject']
            qry.content = args['content']
            qry.device = args['device']
            qry.contact_id = args['contact_id']
            qry.group_id = args['group_id']

            db.session.commit()

            # determine user 
            user = User.query.filter_by(id=claims['id']).first()
            marshaluser = marshal(user, User.response_fields)
            user_id = user.id
            
            # determine email address from user contact table
            from_mail = UserContact.query.filter_by(user_id=claims['id'])
            from_mail = from_mail.filter_by(contact_group_id=qry.contact_id).first()
            marshaluserMail= marshal(from_mail, UserContact.response_fields)
            
            # determine email address customer from customer table
            qry_sent_member = CustomerMember.query.filter_by(group_id=qry.group_id)

            # send an email from flask mail 
            # <img src="https://lolbe.perintiscerita.shop/response" style="display: none;" />
            str_get = "<img style='display: none'; src='https://lolbe.perintiscerita.shop/response/sent_id=" + str(sent.id)
            content = args['content'] + str_get
            for member in qry_sent_member:
                customer = Customer.query.filter_by(user_id=claims['id'])
                customer = customer.filter_by(id=member.customer_id).first()
                marshalcustomer = marshal(customer, Customer.response_fields)
                result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name'], 
                marshalcustomer['email'], marshalcustomer['First_name'], args['subject'], 
                content + "/customer_id=" + str(marshalcustomer['id']) + "/>")
                print("+++++++++++++++++=======================-----------------")
                print(content + "/customer_id=" + str(marshalcustomer['id']) + "'/>")
                track = Track(sent.id, member.customer_id, "", "")
                db.session.add(track)
                db.session.commit()
            app.logger.debug('DEBUG : %s', qry)
            return marshal(qry, Sent.response_fields), 200
                

    # post to draft
    @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('subject', location='json')
        parser.add_argument('content', location='json')
        parser.add_argument('device', location='json')
        parser.add_argument('contact_id', location='json')
        parser.add_argument('group_id', location='json')
        args = parser.parse_args()
        
        claims = get_jwt_claims()
        user_id = User.query.filter_by(id=claims['id']).first()
        user_id = user_id.id

        status = "draft"
        sent = Sent(user_id, status, args['subject'], args['content'],
        args['device'], args['contact_id'], args['group_id'])

        db.session.add(sent)
        db.session.commit()

        app.logger.debug('DEBUG : %s', sent)
        return marshal(sent, Sent.response_fields), 200

    
    @staff_required
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
    def sendMessage(self, fmail, fname, tmail, tname, subject, HTMLmessage):
        app.config.update(dict(
            DEBUG = True,
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 587,
            MAIL_USE_TLS = True,
            MAIL_USE_SSL = False,
            MAIL_USERNAME = fmail,
            MAIL_PASSWORD = 'bountyhunter',{'status': 'NOT_FOUND'}, 404
        msg.html = HTMLmessage
        mail.send(msg)
        return "Sent"

    # post and direct to sent mail from flask mail
    @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('subject', location='json', required=True)
        parser.add_argument('content', location='json', required=True)
        parser.add_argument('device', location='json', required=True)
        parser.add_argument('contact_id', location='json', required=True)
        parser.add_argument('group_id', location='json', required=True)
        args = parser.parse_args() 
        claims = get_jwt_claims()

        # determine user 
        user = User.query.filter_by(id=claims['id']).first()
        marshaluser = marshal(user, User.response_fields)
        user_id = user.id
        
        # determine email address from user contact table
        from_mail = UserContact.query.filter_by(user_id=claims['id'])
        from_mail = from_mail.filter_by(contact_group_id=args['contact_id']).first()
        marshaluserMail= marshal(from_mail, UserContact.response_fields)
        
        # save to database
        status = "sent"
        sent = Sent(user_id, status, args['subject'], args['content'], args['device'],
        args['contact_id'], args['group_id'])
        db.session.add(sent)
        db.session.commit()

        # determine email address customer from customer table
        qry_sent_member = CustomerMember.query.filter_by(group_id=args['group_id'])

        # send an email from flask mail 
        # <img src="https://lolbe.perintiscerita.shop/response" style="display: none;" />
        str_get = "<img style='display: none'; src='https://lolbe.perintiscerita.shop/response/sent_id=" + str(sent.id)
        content = args['content'] + str_get
        for member in qry_sent_member:
            customer = Customer.query.filter_by(user_id=claims['id'])
            customer = customer.filter_by(id=member.customer_id).first()
            marshalcustomer = marshal(customer, Customer.response_fields)
            result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name'], 
            marshalcustomer['email'], marshalcustomer['First_name'], args['subject'], 
            content + "/customer_id=" + str(marshalcustomer['id']) + "/>")
            print("+++++++++++++++++=======================-----------------")
            print(content + "/customer_id=" + str(marshalcustomer['id']) + "'/>")
            track = Track(sent.id, member.customer_id, "", "")
            db.session.add(track)
            db.session.commit()
        app.logger.debug('DEBUG : %s', sent)
        return marshal(sent, Sent.response_fields), 200

class getDraftById(Resource):

    # fungsi untuk get draft by id
    @staff_required
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
