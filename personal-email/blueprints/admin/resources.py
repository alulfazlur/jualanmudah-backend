from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.sent.model import Sent
from blueprints import db, app, staff_required
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

from mailjet_rest import Client
import os



bp_sent = Blueprint('sent', __name__)
api = Api(bp_sent)


class SentResource(Resource):