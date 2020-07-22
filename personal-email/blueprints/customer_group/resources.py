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

class CustomerGroupResource(Resource):

    @staff_required
    def get(self, id=None):
        """Gets a customer group by id

        Args:
            id (int): The id of the customer group

        Returns:
            json: A dictionary of customer group
        """
        qry = CustomerGroup.query.get(id)
        if qry is not None:
            return marshal(qry, CustomerGroup.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @staff_required
    def post(self):
        """Posts a customer group

        Args:
            name (str): The name of customer group
            status (bool): A status existed
                (default is True)

        Returns:
            json: A dictionary of customer group
        """
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

    @staff_required
    def patch(self, id):
        """Soft deletes a customer group

        Args:
            id (int): The id of the customer group

        Returns:
            json: A dictionary of customer group with status false
        """
        qry = CustomerGroup.query.get(id)
        qry.status = False
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.commit()
        return marshal(qry, CustomerGroup.response_fields), 200

    def options(self):
        return {}, 200

class ListCustomerGroup(Resource):

    @staff_required
    def get(self, id=None):
        """Gets a list of customer group

        Args:
            p (int): The sum of page
                (default is 1)
            rp (int): The sum of customer group in list in one page
                (default is 25)

        Returns:
            list: a list of json representing the customer group
        """
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        claims = get_jwt_claims()
        offset = (args['p']*args['rp']-args['rp'])

        qry = CustomerGroup.query.filter_by(user_id=claims['id'])
        qry = qry.filter_by(status=True)

        if qry.first() is None:
            return {'status': 'NOT_FOUND'}, 404
        rows=[]
        for row in qry.offset(offset).all():
            marshal_group= marshal(row, CustomerGroup.response_fields)
            rows.append(marshal_group)
        return rows, 200
    
    def options(self):
        return {}, 200
        
api.add_resource(CustomerGroupResource, '', '/<id>')
api.add_resource(ListCustomerGroup, '/list', '/<id>')