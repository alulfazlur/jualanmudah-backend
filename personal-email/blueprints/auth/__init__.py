from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import hashlib
from blueprints import db, internal_required
from ..user.model import User

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)


class CreateTokenResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        qry_user = User.query.filter_by(username=args['username']).first()
        user_salt = qry_user.salt
        hash_pass = hashlib.sha512(
            ('%s%s' % (args['password'], user_salt)).encode('utf-8')).hexdigest()

        if hash_pass == qry_user.password:
            qry_user = marshal(qry_user, User.jwt_claim_fields)
            token = create_access_token(
                identity=args['username'], user_claims=qry_user)
            return {'token': token}, 200
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200


class RefreshTokenResource(Resource):

    @jwt_required
    @internal_required
    def post(self):
        current_user = get_jwt_claims()
        token = create_access_token(identity=current_user)
        return {'token': token}, 200


api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')
