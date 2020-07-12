from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.sent.model import Sent
from blueprints import db, app, staff_required
from sqlalchemy import desc
from blueprints.tracking.model import Track
from blueprints.user.model import User
from blueprints.user_contact.model import UserContact
from blueprints.user_contact_group.model import UserContactGroup
from blueprints.customer.model import Customer
from blueprints.customer_group.model import CustomerGroup
from blueprints.customer_member.model import CustomerMember
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints import app
from flask_mail import Mail
from flask_mail import Message


bp_track = Blueprint('track', __name__)
api = Api(bp_track)

class TrackList(Resource):

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='args')
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry = Track.query.filter_by(sent_id=args['sent_id'])
        if qry is not None:
            rows = []
            for track in qry:
                marshal_track = marshal(track, Track.response_fields)
                rows.append(marshal_track)
            return rows, 200
        return {'status': 'NOT_FOUND'}, 404
        
class TrackOpen(Resource):

     # @staff_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='args')
        parser.add_argument('customer_id', location='args')
        args = parser.parse_args()
        # claims = get_jwt_claims()
        qry = Track.query.filter_by(sent_id=args['sent_id'])
        qry = qry.filter_by(customer_id=args['customer_id']).first()
        if qry is not None:
            qry.status_open = "opened"
            db.session.commit()
            QRY = marshal(qry, Track.response_fields) 
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

class TrackClick(Resource):
      # @staff_required
    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('sent_id', location='args')
        parser.add_argument('customer_id', location='args')
        args = parser.parse_args()
        # claims = get_jwt_claims()
        qry = Track.query.filter_by(sent_id=args['sent_id'])
        qry = qry.filter_by(customer_id=args['customer_id']).first()
        if qry is not None:
            qry.status_click = "clicked"
            db.session.commit()
            QRY = marshal(qry, Track.response_fields) 
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

api.add_resource(TrackList, '', '<id>')
api.add_resource(TrackOpen, '/open', '<id>')
api.add_resource(TrackClick, '/click', '<id>')

