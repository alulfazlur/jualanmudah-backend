from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Customer
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_customer = Blueprint('customer', __name__)
api = Api(bp_customer)

# using flask restful


class CustomerResource(Resource):

    # @staff_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry_user = Customer.query.filter_by(user_id=claims['id']).first()
        qry = qry_user.filter_by(id=id).first()
        if qry is not None:
            return marshal(qry, Customer.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @jwt_required
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
        qry_user = User.query.filter_by(id=claims['id']).first()
        print("=============================")
        print(qry_user)
        user_id = qry_user.id 

        customer = Customer(args['First_name'], args['last_name'], args['email'], 
        args['phone'], args['bod'], args['address'], args['gender'], args['company'],  user_id)

        db.session.add(customer)
        db.session.commit()
        app.logger.debug('DEBUG: %s', customer)

        return marshal(customer, Customer.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(CustomerResource, '', '/<id>')
