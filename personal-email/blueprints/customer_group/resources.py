from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import CustomerGroup
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_customer_group = Blueprint('customer_group', __name__)
api = Api(bp_customer_group)

# using flask restful

class UserResource(Resource):

    # @internal_required
    def get(self, id=None):
        qry = CustomerGroup.query.get(id)
        if qry is not None:
            return marshal(qry, CustomerGroup.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')

        customer_group = Customer(args['customer_id'], args['group_id'])

        db.session.add(customer_group)
        db.session.commit()
        app.logger.debug('DEBUG: %s', customer_group)

        return marshal(customer_group, CustomerGroup.response_fields), 200, {'Content-Type': 'application/json'}
