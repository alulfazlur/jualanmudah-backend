import configparser
from datetime import timedelta

cfg = configparser.ConfigParser()
cfg.read('config.cfg')


class Config():
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = cfg['secret_key']['key']
    JWT_ACCES_TOKEN_EXPIRES = timedelta(days=1)
    FIREBASECONFIG = {
            "apiKey" : cfg['firebase']['apiKey'],
            "authDomain" : cfg['firebase']['authDomain'],
            "databaseURL" : cfg['firebase']['databaseURL'],
            "projectId" : cfg['firebase']['projectId'],
            "storageBucket" : cfg['firebase']['storageBucket'],
            "messagingSenderId" : cfg['firebase']['messagingSenderId'],
            "appId" : cfg['firebase']['appId'],
            "measurementId" : cfg['firebase']['measurementId']
    }
    
    MAIL_SERVER=cfg['flaskmail']['mail_server']
    MAIL_PORT = cfg['flaskmail']['mail_port']
    MAIL_USERNAME =cfg['flaskmail']['mail_username']
    MAIL_PASSWORD = cfg['flaskmail']['mail_password']
    MAIL_USE_TLS = cfg['flaskmail']['mail_tls']
    MAIL_USE_SSL = cfg['flaskmail']['mail_ssl']


class DevelopmentConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
    APP_PORT = 5000


class ProductionConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 100000
    APP_PORT = 5050


class TestingConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 100000
    APP_PORT = 5050
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s_testing' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = cfg['secret_key']['key']
    JWT_ACCES_TOKEN_EXPIRES = timedelta(days=1)
