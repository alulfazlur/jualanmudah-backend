from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import User
from blueprints import db, app, leader_required
from blueprints.firebase.upload import UploadToFirebase 
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import uuid
import hashlib,werkzeug


bp_user = Blueprint('user', __name__)
api = Api(bp_user)

# using flask restful


class UserResource(Resource):

    # @staff_required
    def get(self, id=None):
        qry = User.query.get(id)
        if qry is not None:
            QRY = marshal(qry, User.response_fields)
            
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

    # @staff_required
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
        image = args['user_image']
        upload_image = UploadToFirebase ()
        link = upload_image.UploadImage(image,"user_image")
        salt = uuid.uuid4().hex
        hash_pass = hashlib.sha512(
            ('%s%s' % (args['password'], salt)).encode('utf-8')).hexdigest()
        user = User(args['full_name'],
                    args['username'], hash_pass, salt, args['status'], args['address'], args['position'],link)

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        return marshal(user, User.response_fields), 200, {'Content-Type': 'application/json'}

    # @staff_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = User.query.filter_by(id=claims['id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('full_name', location='json', required=True)
            parser.add_argument('username', location='json',
                                type=int, required=True)
            parser.add_argument('password', location='json',
                                required=True)
            parser.add_argument('address', location='json', required=True)
            parser.add_argument('position', location='json', required=True)
            args = parser.parse_args()

            qry.full_name = args['full_name']
            qry.username = args['username']
            qry.password = args['password']
            qry.address = args['address']
            qry.status = args['position']
            
            db.session.commit()

            return marshal(qry, User.response_fields), 200

    @leader_required
    def delete(self, id):
        qry = User.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200


# class UserList(Resource):
#     def __init__(self):
#         pass

#     # @staff_required
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('p', type=int, location='args', default=1)
#         parser.add_argument('rp', type=int, location='args', default=25)
#         parser.add_argument('sex', location='args',
#                             help='invalid status', choices=('male', 'female'))
#         parser.add_argument('orderby', location='args',
#                             help='invalid order by value', choices=('age', 'sex'))
#         parser.add_argument('sort', location='args',
#                             help='invalid sort value', choices=('desc', 'asc'))

#         args = parser.parse_args()
#         offset = (args['p'] * args['rp']) - args['rp']
#         qry = User.query
#         if args['sex'] is not None:
#             qry = qry.filter_by(sex=args['sex'])

#         if args['orderby'] is not None:
#             if args['orderby'] == 'age':
#                 if args['sort'] == 'desc':
#                     qry = qry.order_by(desc(User.age))
#                 else:
#                     qry = qry.order_by(User.age)
#             elif args['orderby'] == 'sex':
#                 if args['sort'] == 'desc':
#                     qry = qry.order_by(desc(User.sex))
#                 else:
#                     qry = qry.order_by(User.sex)
#         rows = []
#         for row in qry.limit(args['rp']).offset(offset).all():
#             rows.append(marshal(row, User.response_fields))
#         return rows, 200


# api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '', '/<id>')
