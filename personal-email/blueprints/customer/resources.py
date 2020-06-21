from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Customer
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.user.model import User
from blueprints.user_contact_group.model import UserContactGroup
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required



bp_customer = Blueprint('customer', __name__)
api = Api(bp_user_contact)

# using flask restful
