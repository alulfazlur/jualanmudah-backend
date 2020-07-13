from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Customer
from blueprints import db, app, staff_required, leader_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import quickemailverification

bp_customer = Blueprint('customer', __name__)
api = Api(bp_customer)

class CustomerResource(Resource):

    @staff_required
    def get(self,id):
        claims = get_jwt_claims()
        qry_user = Customer.query.filter_by(user_id=claims['id'])
        qry = qry_user.filter_by(id=id).first()
        # if qry is not None:
        return marshal(qry, Customer.response_fields), 200
        # return {'status': 'NOT_FOUND'}, 404

    @staff_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('First_name', location='json', required=True)
        parser.add_argument('last_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone', location='json', required=True)
        parser.add_argument('bod', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('gender', location='json', choices=['male', 'female'])
        parser.add_argument('company', location='json')
        # parser.add_argument('user_id', type=int location='json')
        
        args = parser.parse_args()
        claims = get_jwt_claims()

        client = quickemailverification.Client('cf42a86c0859259680f2fa74a3f4f3c2bbf1eb52511f9273d672c4bca43c') # Replace API_KEY with your API Key
        checking = client.quickemailverification()
        response = checking.verify(args['email'])  # Email address which need to be verified
        validation = response.body['result']

        customer = Customer(args['First_name'], args['last_name'], args['email'], 
        args['phone'], args['bod'], args['address'], args['gender'], args['company'],  claims['id'], validation)

        db.session.add(customer)
        db.session.commit()
        app.logger.debug('DEBUG: %s', customer)

        return marshal(customer, Customer.response_fields), 200

    @staff_required
    def delete(self, id):
        qry = Customer.query.get(id)
        # if qry is None:
        #     return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
    
    def options(self):
        return {}, 200

class ListCustomer(Resource):

    # get list data customer
    @staff_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        claims = get_jwt_claims()
        offset = (args['p']*args['rp']-args['rp'])

        qry = Customer.query.filter_by(user_id=claims['id'])
        # if qry is not None:
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            marshalcustomer = marshal(row, Customer.response_fields)
            rows.append(marshalcustomer)
        return rows, 200
        # return {'status': 'NOT_FOUND'}, 404

    def options(self):
        return {}, 200

class LeaderCustomer(Resource):

    # get list data customer by user_id for leader
    @leader_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])

        qry = Customer.query.filter_by(user_id=args['user_id'])
        # if qry is not None:
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            marshalcustomer = marshal(row, Customer.response_fields)
            rows.append(marshalcustomer)
        return rows, 200
        # return {'status': 'NOT_FOUND'}, 404

    # post data customer staff for leader
    @leader_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('First_name', location='json', required=True)
        parser.add_argument('last_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone', location='json', required=True)
        parser.add_argument('bod', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('gender', location='json', choices=['male', 'female'])
        parser.add_argument('company', location='json')
        parser.add_argument('user_id', type=int, location='json')
        
        args = parser.parse_args()
        claims = get_jwt_claims()
  
        client = quickemailverification.Client('cf42a86c0859259680f2fa74a3f4f3c2bbf1eb52511f9273d672c4bca43c') # Replace API_KEY with your API Key
        checking = client.quickemailverification()
        response = checking.verify(args['email'])  # Email address which need to be verified
        validation = response.body['result']

        customer = Customer(args['First_name'], args['last_name'], args['email'], 
        args['phone'], args['bod'], args['address'], args['gender'], args['company'], args['user_id'], validation)

        db.session.add(customer)
        db.session.commit()
        app.logger.debug('DEBUG: %s', customer)

        return marshal(customer, Customer.response_fields), 200, {'Content-Type': 'application/json'}
    
    def options(self):
        return {}, 200

api.add_resource(CustomerResource, '', '/<id>')
api.add_resource(ListCustomer, '/list', '/<id>')
api.add_resource(LeaderCustomer, '/leader', '/<id>')
