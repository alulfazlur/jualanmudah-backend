from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import MailJet
from blueprints import db, app

from mailjet_rest import Client
import os

# import base64
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import pickle
# import os
# from google_auth_oauthlib.flow import Flow, InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# from google.auth.transport.requests import Request
# from blueprints.penjual.model import Penjual
# from blueprints.produk_kategori.model import ProdukKategori
# from sqlalchemy import desc
# from blueprints import internal_required
# from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
# from blueprints import admin_required, seller_required, buyer_required

bp_mailjet = Blueprint('mailjet', __name__)
api = Api(bp_mailjet)

class MailJetResource(Resource):

#     def Create_Service(self, client_secret_file, api_name, api_version, *scopes):
#         print(client_secret_file, api_name, api_version, scopes, sep='-')
#         CLIENT_SECRET_FILE = client_secret_file
#         API_SERVICE_NAME = api_name
#         API_VERSION = api_version
#         SCOPES = [scope for scope in scopes[0]]
#         print(SCOPES)
    
#         cred = None
    
#         pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
#         # print(pickle_file)
    
#         if os.path.exists(pickle_file):
#             with open(pickle_file, 'rb') as token:
#                 cred = pickle.load(token)
    
#         if not cred or not cred.valid:
#             if cred and cred.expired and cred.refresh_token:
#                 cred.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
#                 cred = flow.run_local_server()
    
#             with open(pickle_file, 'wb') as token:
#                 pickle.dump(cred, token)
    
#         try:
#             service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
#             print(API_SERVICE_NAME, 'service created successfully')
#             return service
#         except Exception as e:
#             print('Unable to connect.')
#             print(e)
#             return None
    
#     def convert_to_RFC_datetime(self, year=1900, month=1, day=1, hour=0, minute=0):
#         dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
#         return dt

#     def sendMessage(self, to, subject, message):
#         # CLIENT_SECRET_FILE = 'client_secret.json'
#         API_NAME = 'gmail'
#         API_VERSION = 'v1'
#         SCOPES = ['https://mail.google.com/']
        
#         service = self.Create_Service({
#     "installed": {
#       "client_id": "224287002670-7rkug2d7aavrq98dlvn6mm12suaf0sul.apps.googleusercontent.com",
#       "project_id": "quickstart-1592293311977",
#       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#       "token_uri": "https://oauth2.googleapis.com/token",
#       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#       "client_secret": "LB1kSJFCuAqStnYKKZcz09RW",
#       "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
#     }
#   }
#   , API_NAME, API_VERSION, SCOPES)
        
#         emailMsg = message
#         mimeMessage = MIMEMultipart()
#         mimeMessage['to'] = to
#         mimeMessage['subject'] = subject
#         mimeMessage.attach(MIMEText(emailMsg, 'plain'))
#         raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        
#         notif = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
#         return notif

    def sendMessage(self, fmail, fname, tmail, tname, subject, text, HTMLmessage):
        api_key = 'c678d961386dc4f4ca937db65790ae15'
        api_secret = '751173a0270f92eef81cfadfff9193f1'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        nama = fmail
        data = {
        'Messages': [
            {
            "From": {
                "Email": fmail,
                "Name": fname
            },
            "To": [
                {
                "Email": tmail,
                "Name": tname
                }
            ],
            "Subject": subject,
            "TextPart": text,
            "HTMLPart": HTMLmessage,
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code, result.json()
        
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fmail', location='json')
        parser.add_argument('fname', location='json')
        parser.add_argument('tmail', location='json')
        parser.add_argument('tname', location='json')
        parser.add_argument('subject', location='json')
        parser.add_argument('text', location='json')
        parser.add_argument('HTMLmessage', location='json')
        args = parser.parse_args()
        
        emailMessage = EmailMessage(args['fmail'], args['fname'], args['tmail'], args['tname'],
        args['subject'], args['text'],args['HTMLmessage'])
        db.session.add(emailMessage)
        db.session.commit()
        app.logger.debug('DEBUG: %s', args)

        return self.sendMessage(args['fmail'], args['fname'], args['tmail'], args['tname'],
        args['subject'], args['text'],args['HTMLmessage']), 200 

api.add_resource(MailJetResource, '', '')