from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import UserContact
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_user_contact = Blueprint('user_contact', __name__)
api = Api(bp_user_contact)

# using flask restful


class UserContactResource(Resource):

    # @staff_required
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

    # @staff_required
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=True)
        parser.add_argument('contact_id', location='json', required=True)
        parser.add_argument('email_or_wa', location='json',required=True)
        parser.add_argument('password', location='json')
        args = parser.parse_args()

        user_contact = UserContact(args['user_id'],args['contact_id'],args['email_or_wa'],args['password'])

        db.session.add(user_contact)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_contact)
        return marshal(user_contact, UserContact.response_fields), 200, {'Content-Type': 'application/json'}

    # @staff_required
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
            parser.add_argument('password', location='json')
            args = parser.parse_args()
            qry.user_id = args['user_id']
            qry.contact_id = args['contact_id']
            qry.email_or_wa = args['email_or_wa']
            qry.password = args['password']
            db.session.commit()

            return marshal(qry, UserContact.response_fields), 200

    # @staff_required
    def delete(self, id):
        qry = UserContact.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200

class ListUserContact(Resource):

    @staff_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])

        claims = get_jwt_claims()
        qry_user_contact = UserContact.query.filter_by(user_id=claims['id'])
        
        rows = []
        for row in qry_user_contact.limit(args['rp']).offset(offset).all():
            user_contact_list = (marshal(row, UserContact.response_fields))
            rows.append(user_contact_list) 

        return rows, 200

api.add_resource(UserContactResource, '', '/<id>')
api.add_resource(ListUserContact, '/list', '/<id>')
