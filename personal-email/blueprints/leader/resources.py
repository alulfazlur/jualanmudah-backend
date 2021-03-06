from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.sent.model import Sent
from blueprints import db, app, staff_required, leader_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.sent.model import Sent
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

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)


class UserLeaderListStaff(Resource):
    
    # get all list user leader by status
    @leader_required
    claims = get_jwt_claims ()
    def get(self, id=None):
        qry = User.query.filter_by(leader_id=claims["id"])
        if qry is not None:
            rows = []
            for row in qry:
                marshalstaff=marshal(row, User.response_fields).first()
                rows.append(marshalstaff)
            return rows, 200
        return {'status': 'NOT_FOUND'}, 404
    
    # delete an user
    @leader_required
    def delete(self, id):
        qry = User.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200

class SentLeader(Resource):

    # get all list sent and draft by user_id
    @leader_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry = Sent.query.filter_by(user_id=args['user_id']).all()
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
    
    # delete a sent email
    @leader_required
    def delete(self, id):
        qry = Sent.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
    
    def options(self):
        return {}, 200
    
# class QueryStaff(Resource):
#     # get all list customer from staff
#     @leader_required
#     claims = get_jwt_claims ()
#     def get(self, id=None):
#         qry = Customer.query.filter_by(user_id=claims["id"])
#         if qry is not None:
#             rows = []
#             for row in qry:
#                 marshalstaff=marshal(row, User.response_fields).first()
#                 rows.append(marshalstaff)

#             return rows, 200
#         return {'status': 'NOT_FOUND'}, 404
    





api.add_resource(SentAdmin, '', '/<id>')