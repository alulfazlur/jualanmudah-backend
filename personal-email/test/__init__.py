import pytest 
import logging
import json
import hashlib
import uuid
import os
from sqlalchemy.sql import func
from blueprints import app, cache, db
from flask import Flask, request, json
from blueprints.user.model import User
from blueprints.user_contact.model import UserContact
from blueprints.user_contact_group.model import UserContactGroup
from blueprints.customer.model import Customer
from blueprints.customer_member.model import CustomerMember
from blueprints.customer_group.model import CustomerGroup
from blueprints.sent.model import Sent
from blueprints.tracking.model import Track

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()
    
    salt = uuid.uuid4().hex
    encoded = ('%s%s' %("admin", salt)).encode('utf-8')
    hashpass = hashlib.sha512(encoded).hexdigest()
    encoded2 = ('%s%s' %("leader", salt)).encode('utf-8')  
    hashpass2 = hashlib.sha512(encoded2).hexdigest()
    encoded3 = ('%s%s' %("staff", salt)).encode('utf-8') 
    hashpass3 = hashlib.sha512(encoded3).hexdigest()
    encoded4 = ('%s%s' %("helper", salt)).encode('utf-8') 
    hashpass4 = hashlib.sha512(encoded3).hexdigest()
    user_admin = User(full_name= "bapa admin",username='admin', password=hashpass, salt=salt, status="admin", address="malang", position="admin", user_image="awesome",leader_id=None)
    user_leader = User(full_name="bapa leader",username='leader', password=hashpass2, salt=salt, status="leader", address="malang", position="manager", user_image="awesome",leader_id=None)
    user_staff = User(full_name="bapa staff",username='staff', password=hashpass3, salt=salt, status="staff", address="malang", position="staff", user_image="awesome",leader_id=2)
    user_helper = User(full_name="bapa helper",username='helper', password=hashpass4, salt=salt, status="helper", address="malang", position="helper", user_image="awesome",leader_id=2)        
        
    db.session.add(user_admin)
    db.session.add(user_leader)
    db.session.add(user_staff)
    db.session.add(user_helper)
    db.session.commit()
    
    user_contact_group = UserContactGroup(name="email")
    db.session.add(user_contact_group)
    db.session.commit()

    user_contact = UserContact(user_id=2, contact_group_id=1, email_or_wa="romli@alterra.id",password="alta123")
    db.session.add(user_contact)
    user_contact = UserContact(user_id=3, contact_group_id=1, email_or_wa="derby@alterra.id",password="alta123")
    db.session.add(user_contact)
    db.session.commit()
    
    customer = Customer(First_name="Derby",last_name="Prayogo", email="derby@alterra.id",phone="08934551",bod="1997-06-01",address="sby",gender="male",company="alta",user_id=2)
    db.session.add(customer)
    customer = Customer(First_name="ajay",last_name="klaten", email="ajay@alterra.id",phone="0893455134",bod="1997-06-02",address="ML",gender="male",company="astra",user_id=2)
    db.session.add(customer)
    db.session.commit()
    
    customer_group = CustomerGroup(name="manager")
    db.session.add(customer_group)
    customer_group = CustomerGroup(name="staff")
    db.session.add(customer_group)
    db.session.commit()
    
    customer_member = CustomerMember(customer_id=1,group_id=1,)
    db.session.add(customer_member)
    db.session.commit()

    sent = Sent(user_id =3,send_date="",status="",subject="warming up", content= "bagi-bagi uang",device="email",contact_id=1, group_id=1,open_rate=1,click_rate=1,total_sent=1)
    db.session.add(sent)
    db.session.commit()

    track = Track(sent_id =1, customer_id=1,status_open="opened",status_click="clicked")
    db.session.add(sent)
    db.session.commit()

    yield db
    
    db.drop_all()
    
    
def create_token_admin():
    token = cache.get('test-token-admin')
    if token is None:
        data={
            'username': 'admin',
            'password': 'admin'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-admin', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token


def create_token_leader():
    token = cache.get('test-token-leader')
    if token is None:
        data={
            'username': 'leader',
            'password': 'leader'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-leader', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token

def create_token_staff():
    token = cache.get('test-token-staff')
    if token is None:
        data={
            'username': 'staff',
            'password': 'staff'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-staff', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token

def create_token_helper():
    token = cache.get('test-token-helper')
    if token is None:
        data={
            'username': 'helper',
            'password': 'helper'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-helper', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token