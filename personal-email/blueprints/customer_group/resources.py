from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import CustomerGroup
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_customer_group = Blueprint('customer_group', __name__)
api = Api(bp_customer_group)

# using flask restful

class CustomerGroupResource(Resource):

    # get customer group by id
    @staff_required
    def get(self, id=None):
        qry = CustomerGroup.query.get(id)
        # if qry is not None:
        return marshal(qry, CustomerGroup.response_fields), 200
        # return {'status': 'NOT_FOUND'}, 404

    # post customer group
    @staff_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('status', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        
        customer_group = CustomerGroup( args['name'], claims['id'], args['status'])

        db.session.add(customer_group)
        db.session.commit()
        app.logger.debug('DEBUG: %s', customer_group)

        return marshal(customer_group, CustomerGroup.response_fields), 200, {'Content-Type': 'application/json'}

    # delete customer group
    @staff_required
    def patch(self, id):
        qry = CustomerGroup.query.get(id)

        qry.status = False
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

     
        db.session.delete(qry)

        db.session.commit()


class ListCustomerGroup(Resource):

    # get call list customer group
    @staff_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        claims = get_jwt_claims()
        offset = (args['p']*args['rp']-args['rp'])

        qry = CustomerGroup.query.filter_by(user_id=claims['id'])

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry = CustomerGroup.query
        print("==============----------------------")
        print(qry)
        # if qry is None:
        #     return {'status': 'NOT_FOUND'}, 404

        rows=[]
        for row in qry.offset(offset).all():
            marshal_group= marshal(row, CustomerGroup.response_fields)
            rows.append(marshal_group)
        return rows, 200
        
api.add_resource(CustomerGroupResource, '', '/<id>')
api.add_resource(ListCustomerGroup, '/list', '/<id>')