from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Sent
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_sent = Blueprint('sent', __name__)
api = Api(bp_sent)

# using flask restful


class SentResource(Resource):

    # @internal_required
    def get(self, id=None):
        qry = Sent.query.get(id)
        if qry is not None:
            QRY = marshal(qry, Sent.response_fields)
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

    # @internal_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=True)
        parser.add_argument('member_id', location='json', required=True)
        parser.add_argument('send_date', location='json', required=True)
        parser.add_argument('status', location='json', required=True)
        parser.add_argument('content', location='json', required=True)
        parser.add_argument('device', location='json', required=True)
        args = parser.parse_args()

        sent = User(args['user_id'],args['member_id'],args['send_date'],args['status'],args['content'],args['device'])

        db.session.add(sent)
        db.session.commit()

        app.logger.debug('DEBUG : %s', sent)
        return marshal(sent, Sent.response_fields), 200, {'Content-Type': 'application/json'}

    # @internal_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = User.query.filter_by(id=claims['id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', location='json', required=True)
            parser.add_argument('member_id', location='json', required=True)
            parser.add_argument('send_date', location='json', required=True)
            parser.add_argument('status', location='json', required=True)
            parser.add_argument('content', location='json', required=True)
            parser.add_argument('device', location='json', required=True)
          
            args = parser.parse_args()
            qry.user_id = args['user_id']
            qry.member_id = args['member_id']
            qry.send_date = args['send_date']
            qry.status = args['status']
            qry.content = args['content']
            qry.device = args[device]  
            db.session.commit()

            return marshal(qry, Sent.response_fields), 200

    # @internal_required
    def delete(self, id):
        qry = Sent.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200



api.add_resource(SentResource, '', '/<id>')
