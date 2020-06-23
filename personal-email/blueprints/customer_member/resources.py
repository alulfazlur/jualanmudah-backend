from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import CustomerMember
from blueprints import db, app, internal_required
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

    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('group_id', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry_customer = Customer.query.filter_by(user_id=claims['id']).first()
        qry_group = CustomerGroup.query.get(args["group_id"])
        marshalgroup = marshal(qry_group,CustomerGroup.response_fields)
        print("=====================================================")
        print(marshalgroup)
        qry_member = CustomerMember.query.filter_by(customer_id=qry_customer.id)
        qry_member = qry_member.filter_by(group_id=args["group_id"])
        print("=====================================================")
        print(qry_member)

        for member in qry_member:
            print("=====================================================")
            print(member)
            customer = Customer.query.filter_by(id=member.customer_id).first()    
            marshalcustomer = marshal(customer,Customer.response_fields)
            marshalgroup["anggota"]= marshalcustomer

        # print("================================================================")
        # print(qry_customer)
        # qry_customer_member = CustomerMember.query.filter_by(customer_id=qry_user.id).first()
        # qry = qry_customer_member.filter_by(id=id).first()
        # if qry is not None:
        #     return marshal(qry, Customer.response_fields), 200
        # return {'status': 'NOT_FOUND'}, 404
        return marshalgroup,200
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

api.add_resource(CustomerMemberResource, '', '/<id>')