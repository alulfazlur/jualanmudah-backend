from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import UserContact
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_user_contact = Blueprint('user_contact', __name__)
api = Api(bp_user_contact)

# using flask restful


class UserContactResource(Resource):

    # @internal_required
    def get(self, id=None):
        qry = UserContact.query.get(id)
        if qry is not None:
            QRY = marshal(qry, UserContact.response_fields)
            user = User.query.filter_by(user_id=QRY['id']).first()
            contact_list = UserContactGroup.query.filter_by(contact_group_id=QRY['id']).first()
            QRY['User'] = marshal(user, User.response_fields)
            QRY['contact_list'] = marshal(contact_list,UserContactGroup.response_fields)
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

    # @internal_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=True)
        parser.add_argument('contact_id', location='json', required=True)
        parser.add_argument('email_or_wa', location='json',required=True)
        args = parser.parse_args()

        user_contact = User(args['user_id'],args['contact_id'],  args['email_or_wa'])

        db.session.add(user_contact)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_contact)
        return marshal(user_contact, UserContact.response_fields), 200, {'Content-Type': 'application/json'}

    # @internal_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = User.query.filter_by(id=claims['id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', location='json', required=True)
            parser.add_argument('contact_id', location='json', required=True)
            parser.add_argument('email_or_wa', location='json',required=True)
            args = parser.parse_args()
            qry.user_id = args['user_id']
            qry.contact_id = args['contact_id']
            qry.email_or_wa = args['email_or_wa']  
            db.session.commit()

            return marshal(qry, UserContact.response_fields), 200

    # @internal_required
    def delete(self, id):
        qry = UserContact.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200



api.add_resource(UserContactResource, '', '/<id>')
