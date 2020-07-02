from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import CustomerMember
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.customer_group.model import CustomerGroup
from blueprints.customer.model import Customer
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_customer_member = Blueprint('customer_member', __name__)
api = Api(bp_customer_member)

# using flask restful

class CustomerMemberResource(Resource):

    # get list member of customer by group_id
    @staff_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('group_id', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry_customer = Customer.query.filter_by(user_id=claims['id'])
        qry_group = CustomerGroup.query.get(args["group_id"])
        marshalgroup = marshal(qry_group,CustomerGroup.response_fields)
        qry_member = CustomerMember.query.filter_by(group_id=args['group_id'])

        rows = []
        for member in qry_member:
            customer = Customer.query.filter_by(id=member.customer_id).first()    
            marshalcustomer = marshal(customer,Customer.response_fields)
            rows.append(marshalcustomer)
        marshalgroup["anggota"]= rows
        return marshalgroup,200

    # post customer member
    @staff_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('customer_id', location='json')
        parser.add_argument('group_id', location='json')
        args = parser.parse_args()

        customer_member = CustomerMember(args['customer_id'], args['group_id'])

        db.session.add(customer_member)
        db.session.commit()
        app.logger.debug('DEBUG: %s', customer_member)

        return marshal(customer_member, CustomerMember.response_fields), 200, {'Content-Type': 'application/json'}

    # delete customer member
    @staff_required
    def delete(self, id):
        qry = CustomerMember.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

class LeaderCustomerMember(Resource):

    # post customer member by user_id for leader
    @staff_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('group_id', location='json')
        parser.add_argument('user_id', location ='json')
        args = parser.parse_args()
        qry_customer = Customer.query.filter_by(user_id=args['user_id'])
        qry_group = CustomerGroup.query.get(args["group_id"])
        marshalgroup = marshal(qry_group,CustomerGroup.response_fields)
        qry_member = CustomerMember.query.filter_by(group_id=args['group_id'])
        rows = []
        for member in qry_member:
            customer = Customer.query.filter_by(id=member.customer_id).first()    
            marshalcustomer = marshal(customer,Customer.response_fields)
            rows.append(marshalcustomer)
        marshalgroup["anggota"]= rows
        return marshalgroup, 200


api.add_resource(CustomerMemberResource, '', '/<id>')