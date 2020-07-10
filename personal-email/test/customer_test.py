import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO


class TestCustomerResource():

    def test_customer_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/customer/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_customer_staff(self, client, init_database):
        token = create_token_staff()
        res = client.post('/customer',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"First_name":"derby", "last_name": "prayogo","email":"derby@gmail.com","phone":"0895122332","bod":"2020-06-06","address":"malang","gender":"male","company":"alterra"})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_customer_staff(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/customer/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 200
    
class TestListCustomer():

    def test_customer_get_staff_list(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/customer/list',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
class TestLeaderCustomer():

    def test_customer_get_leader_list(self, client, init_database):
        token =  create_token_leader()
        res = client.get('/customer/leader',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json',
                        json={"user_id":3})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_post_customer_leader(self, client, init_database):
        token = create_token_leader()
        res = client.post('/customer/leader',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"First_name":"mas", "last_name": "prayogo","email":"derby@gmail.com","phone":"0895122332","bod":"2020-06-06","address":"malang","gender":"male","company":"alterra","user_id":3})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    

