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


app = Flask(__name__)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)
jwt = JWTManager(app)

@app.route("/")
def hello():
    return {"status": "OK"}, 200

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['internal']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
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

from blueprints.client.resources import bp_client
app.register_blueprint(bp_client, url_prefix='/client')

from blueprints.category.resources import bp_category
app.register_blueprint(bp_category, url_prefix='/category')

from blueprints.payment.resources import bp_payment
app.register_blueprint(bp_payment, url_prefix='/payment')

from blueprints.product.resources import bp_product
app.register_blueprint(bp_product, url_prefix='/product')

from blueprints.receipt.resources import bp_receipt
app.register_blueprint(bp_receipt, url_prefix='/receipt')

from blueprints.shipping.resources import bp_shipping
app.register_blueprint(bp_shipping, url_prefix='/shipping')

from blueprints.transaction.resources import bp_transaction
app.register_blueprint(bp_transaction, url_prefix='/transaction')

from blueprints.user.resources import bp_user
app.register_blueprint(bp_user, url_prefix='/user')

from blueprints.register import bp_register
app.register_blueprint(bp_register, url_prefix='/register')

db.create_all()
