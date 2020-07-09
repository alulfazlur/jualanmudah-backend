from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app, staff_required, leader_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact.model import UserContact
from blueprints.user_contact_group.model import UserContactGroup
from blueprints.customer.model import Customer
from blueprints.customer_group.model import CustomerGroup
from blueprints.customer_member.model import CustomerMember
from blueprints.tracking.model import Track
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints import app
from flask_mail import Mail
from flask_mail import Message
import datetime
import time
import xlrd 

bp_input_node = Blueprint('input_node', __name__)
api = Api(bp_input_node)

class InputnodeResource(Resource):

    @staff_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location_file', location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()

        # Reading an node file using Python 
        # Give the location of the file 
        loc = args['location_file']
        # "/home/alta12/Downloads/testing.xlsx" 
        
        # To open Workbook 
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)

        # Extracting number of rows 
        sum_row = sheet.nrows

        node= sheet.cell_value

        rows=[]
        for index in range(1, sum_row):
            customer = Customer(str(node(index, 1)), str(node(index, 2)), str(node(index, 3)), 
            str(node(index, 4)),str(node(index, 5)), str(node(index, 6)), str(node(index, 7)), 
            str(node(index, 8)), claims['id'])
            print(str(node(index, 1)), str(node(index, 2)), str(node(index, 3)), 
            str(node(index, 4)),str(node(index, 5)), str(node(index, 6)), str(node(index, 7)), 
            str(node(index, 8)), claims['id'])
            marshal_customer = marshal(customer, Customer.response_fields)
            print("=============+++++++++++++---------------")
            print(marshal_customer)
            db.session.add(customer)
            db.session.commit()

            member = CustomerMember(customer.id, int(node(index, 9)))
            marshal_group_customer = marshal(member, CustomerMember.response_fields)
            marshal_customer['member'] = marshal_group_customer
            print("=============+++++++++++++---------------")
            print(marshal_group_customer)
            rows.append(marshal_customer)
            db.session.add(member)
            db.session.commit()

            app.logger.debug('DEBUG: %s', customer)
        return rows, 200

api.add_resource(InputnodeResource, '', '/<id>')