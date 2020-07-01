from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.sent.model import Sent
from blueprints import db, app, staff_required, admin_required
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


class SentAdmin(Resource):

    # get all list draft and sent email
    @admin_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('leader_id', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry = Sent.query.filter_by(user_id=args['leader_id']).all()
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

api.add_resource(SentAdmin, '', '/<id>')