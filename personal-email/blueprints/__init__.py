import json
import logging
import config
import os
from functools import wraps
from flask_restful import fields, Resource, Api
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS, cross_origin
# from flask_mail import Mail


app = Flask(__name__)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)
jwt = JWTManager(app)


# app.config.update(dict(
#     DEBUG = True,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_USERNAME = 'jinadabf@gmail.com',
#     MAIL_PASSWORD = 'bountyhunter',
# ))
# mail = Mail(app)


@app.route("/")
def hello():
    return {"status": "OK"}, 200

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "admin":
            return {'status': 'FORBIDDEN', 'message': 'Admin Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def leader_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "leader":
            return {'status': 'FORBIDDEN', 'message': 'leader Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def staff_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        return fn(*args, **kwargs)
    return wrapper

if os.environ.get('FLASK_ENV', 'Production') == "Production":
    app.config.from_object(config.ProductionConfig)
elif os.environ.get('FLASK_ENV', 'Production') == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else :
        #ternyata cors pake method options di awal buat ngecek CORS dan harus di return kosong 200, jadi di akalin gini deh. :D
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'}

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({'method': request.method,
                                       'code': response.status,
                                       'uri': request.full_path,
                                       'request': requestData,
                                       'response': json.loads(response.data.decode('utf-8'))
                                       }))
    else:
        app.logger.error("")
    return response

from blueprints.auth import bp_auth
app.register_blueprint(bp_auth, url_prefix='/auth')

from blueprints.user.resources import bp_user
app.register_blueprint(bp_user, url_prefix='/user')

from blueprints.user_contact.resources import bp_user_contact
app.register_blueprint(bp_user_contact, url_prefix='/usercontact')

from blueprints.user_contact_group.resources import bp_user_contact_group
app.register_blueprint(bp_user_contact_group, url_prefix='/user_contact_group')

from blueprints.customer.resources import bp_customer
app.register_blueprint(bp_customer, url_prefix='/customer')

from blueprints.customer_member.resources import bp_customer_member
app.register_blueprint(bp_customer_member, url_prefix='/customer-member')

from blueprints.customer_group.resources import bp_customer_group
app.register_blueprint(bp_customer_group, url_prefix='/customer-group')

from blueprints.send_mailjet.resources import bp_mailjet
app.register_blueprint(bp_mailjet, url_prefix='/mailjet')

from blueprints.send_flask_mail.resources import bp_flaskmail
app.register_blueprint(bp_flaskmail, url_prefix='/flaskmail')

from blueprints.sent.resources import bp_sent
app.register_blueprint(bp_sent, url_prefix='/sent' )

from blueprints.tracking.resources import bp_track
app.register_blueprint(bp_track, url_prefix='/track')

from blueprints.admin.resources import bp_admin
app.register_blueprint(bp_admin, url_prefix='/admin')



db.create_all()
