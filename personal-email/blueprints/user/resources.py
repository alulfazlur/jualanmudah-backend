from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import User
from blueprints import db, app, leader_required, staff_required
from blueprints.firebase.upload import UploadToFirebase 
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import uuid
import hashlib,werkzeug


bp_user = Blueprint('user', __name__)
api = Api(bp_user)

# using flask restful


class UserStaff(Resource):

    @staff_required
    def get(self, id=None):
        claims = get_jwt_claims()
        qry = User.query.get(claims['id'])
        if qry is not None:
            QRY = marshal(qry, User.response_fields)
            return QRY, 200
        # return {'status': 'NOT_FOUND'}, 404

    # post a user only for staff
    @leader_required
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='form', required=True)
        parser.add_argument('username', location='form', required=True)
        parser.add_argument('password', location='form',
                            required=True)
        parser.add_argument('status', location='form', choices=["admin","leader","staff"])
        parser.add_argument('address', location='form', required=True)
        parser.add_argument('position', location='form', required=True)
        parser.add_argument('user_image', location='files', type= werkzeug.datastructures.FileStorage,required=False)
        args = parser.parse_args()
        claims = get_jwt_claims()
        leaderId= claims['id']
        image = args['user_image']
        upload_image = UploadToFirebase ()
        link = upload_image.UploadImage(image,"user_image")
        salt = uuid.uuid4().hex
        hash_pass = hashlib.sha512(
            ('%s%s' % (args['password'], salt)).encode('utf-8')).hexdigest()
        user = User(args['full_name'],
                    args['username'], hash_pass, salt, args['status'], args['address'], args['position'],link, leaderId)

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        return marshal(user, User.response_fields), 200, {'Content-Type': 'application/json'}

    @leader_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = User.query.filter_by(id=claims['id']).first()
        # if qry is None:
        #     return {'status': 'NOT_FOUND'}, 404
        # else:
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='form', required=True)
        parser.add_argument('username', location='form', required=True)
        parser.add_argument('password', location='form',
                            required=True)
        parser.add_argument('status', location='form', choices=["admin","leader","staff"])
        parser.add_argument('address', location='form', required=True)
        parser.add_argument('position', location='form', required=True)
        parser.add_argument('user_image', location='files', type= werkzeug.datastructures.FileStorage,required=False)
        args = parser.parse_args()


        image = args['user_image']
        upload_image = UploadToFirebase ()
        link = upload_image.UploadImage(image,"user_image")
        if args['full_name'] is not None:
            qry.full_name = args['full_name']
        if args['username'] is not None:
            qry.username = args['username']
        if args['password'] is not None:
            qry.password = args['password']
        if args['address'] is not None:
            qry.address = args['address']
        if args['position'] is not None:
            qry.position = args['position']
        # if args['user_image'] is not None:
        #     qry.user_image = link
        
        db.session.commit()

        return marshal(qry, User.response_fields), 200

    def options(self):
        return {}, 200

class UserLeader(Resource):

    # post an leader
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='form', required=True)
        parser.add_argument('username', location='form', required=True)
        parser.add_argument('password', location='form',
                            required=True)
        parser.add_argument('address', location='form', required=True)
        parser.add_argument('position', location='form', required=True)
        parser.add_argument('user_image', location='files', type= werkzeug.datastructures.FileStorage,required=False)
        args = parser.parse_args()
        claims = get_jwt_claims()
        status = "leader"
        leaderId= 0
        image = args['user_image']
        upload_image = UploadToFirebase ()
        link = upload_image.UploadImage(image,"user_image")
        salt = uuid.uuid4().hex
        hash_pass = hashlib.sha512(
            ('%s%s' % (args['password'], salt)).encode('utf-8')).hexdigest()
        user = User(args['full_name'],
                    args['username'], hash_pass, salt, status, args['address'], args['position'], link, leaderId)

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        return marshal(user, User.response_fields), 200, {'Content-Type': 'application/json'}

    # get list staff user by leader_id
    @leader_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        claims = get_jwt_claims()

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])

        qry = User.query.filter_by(leader_id=claims['id'])
        if qry is not None:
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                marshalstaff=marshal(row, User.response_fields)
                rows.append(marshalstaff)
            return rows, 200
        return {'status': 'NOT_FOUND'}, 404

    # delete an user
    @leader_required
    def delete(self, id):
        qry = User.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200

api.add_resource(UserStaff, '', '/<id>')
api.add_resource(UserLeader, '/leader', '/<id>')
