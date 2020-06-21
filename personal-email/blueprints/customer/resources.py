from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Customer
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_customer = Blueprint('customer', __name__)
api = Api(bp_customer)

# using flask restful


class UserResource(Resource):

    # @internal_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry_user = Customer.query.filter_by(user_id=claims['id']).first()
        qry = qry_user.filter_by(id=id).first()
        if qry is not None:
            return marshal(qry, Customer.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
        
