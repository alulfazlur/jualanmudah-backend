from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import UserContactGroup
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_user_contact_group = Blueprint('user_contact_group', __name__)
api = Api(bp_user_contact_group)

# using flask restful


class UserContactGroupResource(Resource):

    # @staff_required
    def get(self, id=None):
        qry = UserContactGroup.query.get(id)
        if qry is not None:
            QRY = marshal(qry, UserContactGroup.response_fields)
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

    # @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
     
        args = parser.parse_args()

        user_contact = UserContactGroup(args['name'])

        db.session.add(user_contact)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_contact)
        return marshal(user_contact, UserContactGroup.response_fields), 200, {'Content-Type': 'application/json'}

    # @staff_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = User.query.filter_by(id=claims['id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json', required=True)
          
            args = parser.parse_args()
            qry.name = args['name']
            qry.contact_id = args['contact_id']
            qry.email_or_wa = args['email_or_wa']  
            db.session.commit()

            return marshal(qry, UserContactGroup.response_fields), 200

    # @staff_required
    def delete(self, id):
        qry = UserContactGroup.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200



api.add_resource(UserContactGroupResource, '', '/<id>')
