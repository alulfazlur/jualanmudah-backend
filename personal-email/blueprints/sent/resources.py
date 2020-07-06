from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.sent.model import Sent
from blueprints import db, app, staff_required, leader_required
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
import datetime
import time

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
        parser.add_argument('status', location='json')
        parser.add_argument('send_date', location='json')
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
            if args['sent_id'] is not None:
                qry.sent_id = args['sent_id']
            if claims['id'] is not None:
                qry.user_id = claims['id']
            if args['status'] is not None:
                qry.status = args['status']
            if args['send_date'] is not None:
                qry.send_date = args['send_date']
            if args['subject'] is not None:
                qry.subject = args['subject']
            if args['content'] is not None:
                qry.content = args['content']
            if args['device'] is not None:
                qry.device = args['device']
            if args['contact_id'] is not None:
                qry.contact_id = args['contact_id']
            if args['group_id'] is not None:
                qry.group_id = args['group_id']

            db.session.commit()

            # determine user 
            user = User.query.filter_by(id=claims['id']).first()
            marshaluser = marshal(user, User.response_fields)
            user_id = user.id
            
            # determine email address from user contact table
            from_mail = UserContact.query.filter_by(user_id=claims['id'])
            from_mail = from_mail.filter_by(id=qry.contact_id).first()
            marshaluserMail= marshal(from_mail, UserContact.response_fields)
            
            # determine email address customer from customer table
            qry_sent_member = CustomerMember.query.filter_by(group_id=qry.group_id)

            # send an email from flask mail 
            if len(args['send_date'])>5:
                senddate = args['send_date'].split(',')
                year = int(senddate[0])
                month = int(senddate[1])
                day = int(senddate[2])
                hour = int(senddate[3])
                mins = int(senddate[4])
                sec = int(senddate[5])
                sent_time = datetime.datetime(year,month,day,hour,mins,sec)
                time.sleep(sent_time.timestamp()- time.time())
            elif args['send_date'] == "now":
                sent.send_date = str(datetime.datetime.now())
                db.session.commit()
                pass
            str_get = "<img style='display: none'; src=https://lolbe.perintiscerita.shop/response/sent_id=" + str(args['sent_id'])
            content = args['content'] + str_get
            for member in qry_sent_member:
                customer = Customer.query.filter_by(user_id=claims['id'])
                customer = customer.filter_by(id=member.customer_id).first()
                marshalcustomer = marshal(customer, Customer.response_fields)
                result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name'], 
                marshalcustomer['email'], marshalcustomer['First_name'], args['subject'], 
                content + "/customer_id=" + str(marshalcustomer['id']) + "/>")
                track = Track(args['sent_id'], member.customer_id, "", "")
                db.session.add(track)
                db.session.commit()
            app.logger.debug('DEBUG : %s', qry)
            return marshal(qry, Sent.response_fields), 200
                

    # post to draft
    @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('status', location='json')
        parser.add_argument('subject', location='json')
        parser.add_argument('content', location='json')
        parser.add_argument('device', location='json')
        parser.add_argument('contact_id', location='json')
        parser.add_argument('group_id', location='json')
        args = parser.parse_args()
        
        claims = get_jwt_claims()
        user_id = User.query.filter_by(id=claims['id']).first()
        user_id = user_id.id

        sent = Sent(user_id, args['status'], args['subject'], args['content'],
        args['device'], args['contact_id'], args['group_id'], 0, 0, 0)

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
            MAIL_PASSWORD = 'bountyhunter',
        ))
        mail = Mail(app)
        msg = Message(subject, sender = fmail, recipients = [tmail])
        msg.html = HTMLmessage
        mail.send(msg)
        return "Sent"

    # post and direct to sent mail from flask mail
    @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('status', location='json', required=True)
        parser.add_argument('send_date', location='json', required=True)
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
        from_mail = from_mail.filter_by(id=args['contact_id']).first()
        marshaluserMail= marshal(from_mail, UserContact.response_fields)
        
        # save to database
        sent = Sent(user_id, args['status'], args['send_date'], args['subject'], 
        args['content'], args['device'],args['contact_id'], args['group_id'], 0, 0, 0)
        db.session.add(sent)
        db.session.commit()

        # determine email address customer from customer table
        qry_sent_member = CustomerMember.query.filter_by(group_id=args['group_id'])

        # send an email from flask mail 
        if len(args['send_date'])>5:
            senddate = args['send_date'].split(',')
            year = int(senddate[0])
            month = int(senddate[1])
            day = int(senddate[2])
            hour = int(senddate[3])
            mins = int(senddate[4])
            sec = int(senddate[5])
            sent_time = datetime.datetime(year,month,day,hour,mins,sec)
            time.sleep(sent_time.timestamp()- time.time())
        elif args['send_date'] == "now":
            sent.send_date = str(datetime.datetime.now())
            db.session.commit()
            pass
        str_get = "<img style='display: none'; src=http://0.0.0.0:5050/track/open?sent_id=" + str(sent.id)
        content = args['content'] + str_get
        for member in qry_sent_member:
            customer = Customer.query.filter_by(user_id=claims['id'])
            customer = customer.filter_by(id=member.customer_id).first()
            marshalcustomer = marshal(customer, Customer.response_fields)
            result = self.sendMessage(marshaluserMail['email_or_wa'], marshaluser['full_name'], 
            marshalcustomer['email'], marshalcustomer['First_name'], args['subject'], 
            content + "&customer_id=" + str(marshalcustomer['id']) + "/>")
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

class getAllDraft(Resource):

    # get all list only draft 
    @staff_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry = Sent.query.filter_by(user_id=claims['id'])
        qry = qry.filter_by(status="draft")
        rows = []
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

class getAllSent(Resource):

    # get all list only draft 
    @staff_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry = Sent.query.filter_by(user_id=claims['id'])
        qry = qry.filter_by(status="sent")
     
        rows = []
        if qry is not None:
            track_list = []
            for sent in qry:
                qry_track = Track.query.filter_by(sent_id=sent.id)
                # if qry_track is not None:
                count_open_rate = 0
                count_click_rate = 0
                count_total = 0
                track_list = []
                for track in qry_track:
                    count_total += 1
                    if track.status_open == "opened":
                        count_open_rate += 1
                    elif track.status_click == "clicked":
                        count_click_rate += 1
                    marshaltrack = marshal(track, Track.response_fields)
                    track_list.append(marshaltrack)
                sent.open_rate = count_open_rate
                sent.click_rate = count_click_rate
                sent.total_sent = count_total
                db.session.commit()

                qry_member = CustomerMember.query.filter_by(group_id=sent.group_id)
                qry_member_cus = CustomerMember.query.filter_by(group_id=sent.group_id).first()

                array_customer = []
                for customer in qry_member:
                    customer = Customer.query.filter_by(id=customer.customer_id).first()
                    customer = marshal(customer, Customer.response_fields)
                    array_customer.append(customer)
                qry_group = CustomerGroup.query.filter_by(id=qry_member_cus.group_id).first()
                marshal_group = marshal(qry_group, CustomerGroup.response_fields)
                marshal_sent = marshal(sent, Sent.response_fields)
                marshal_sent['group_customer'] = marshal_group
                marshal_sent['customer'] = array_customer
                marshal_sent['track'] = track_list
                rows.append(marshal_sent)
            return rows, 200
        return {'status': 'NOT_FOUND'}, 404


api.add_resource(SentResource, '', '/<id>')
api.add_resource(SendMailDirect, '/direct', '/<id>')
api.add_resource(getDraftById, '/draft', '/<id>')
api.add_resource(getAllDraft, '/draft-list', '/<id>')
api.add_resource(getAllSent, '/sent-list', '/<id>')
