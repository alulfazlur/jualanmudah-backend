from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import SentWhatsapp
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



bp_sent_WA = Blueprint('sent_whatsapp', __name__)
api = Api(bp_sent_WA)


class SentWhatsAppResource(Resource):

    # get customer group by id
    @staff_required
    def get(self, id=None):
        qry = SentWhatsapp.query.get(id)
        # if qry is not None:
        return marshal(qry, SentWhatsapp.response_fields), 200
        # return {'status': 'NOT_FOUND'}, 404

    # post and direct to sent mail from flask mail
    @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('content', location='json', required=True)
        parser.add_argument('contact_id', location='json', required=True)
        parser.add_argument('group_id', location='json', required=True)
        args = parser.parse_args() 
        claims = get_jwt_claims()

        qry_sent_member = CustomerMember.query.filter_by(group_id=args['group_id'])
        list_phone = []
        for member in qry_sent_member:
            customer = Customer.query.filter_by(user_id=claims['id'])
            customer = customer.filter_by(id=member.customer_id).first()
            print(marshal(customer, Customer.response_fields))
            
            if customer.phone is not None:
                list_phone.append(customer.phone)
        
        # save to database
        sent = SentWhatsapp(claims['id'], args['content'], args['contact_id'], args['group_id'], len(list_phone), str(list_phone))
        db.session.add(sent)
        db.session.commit()

       
        app.logger.debug('DEBUG : %s', sent)
        return marshal(sent, SentWhatsapp.response_fields), 200

    @staff_required
    def delete(self, id):
        qry = SentWhatsapp.query.get(id)
        # if qry is None:
        #     return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    @staff_required
    def options(self):
        return {}, 200

class ListWhatsApp(Resource):

    # get list data sentWA
    @staff_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        claims = get_jwt_claims()
        offset = (args['p']*args['rp']-args['rp'])

        qry = SentWhatsapp.query.filter_by(user_id=claims['id'])
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            marshal_wa = marshal(row, SentWhatsapp.response_fields)
            rows.append(marshal_wa)
        return rows, 200
    
    def options(self):
        return {}, 200


api.add_resource(SentWhatsAppResource, '', '/<id>')
api.add_resource(ListWhatsApp, '/list', '/<id>')