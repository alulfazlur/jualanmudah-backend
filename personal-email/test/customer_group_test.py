import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO


class TestGroupCustomerResource():

    def test_customer_group_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/customer-group/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_customer_group_staff(self, client, init_database):
        token = create_token_staff()
        res = client.post('/customer-group',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"name":"manager"})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_customer_group_staff(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/customer-group/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 200
 

class TestListCustomerGroup():
    
    def test_customer_group_get__list_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/customer-group/list',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200