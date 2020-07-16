import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO


class TestCustomerMemberResource():

    def test_customer_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/customer-member',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json',
                        query_string ={"group_id":1})
        res_json = json.loads(res.data)
        assert res.status_code == 200


    def test_post_customer_member_staff_none(self, client, init_database):
        token = create_token_staff()
        res = client.post('/customer-member',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"customer_id":1,"group_id":1})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_post_customer_member_staff(self, client, init_database):
        token = create_token_staff()
        res = client.post('/customer-member',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"customer_id":2,"group_id":2})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_customer_staff(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/customer-member/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_customer_staff_none(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/customer-member/10',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 404


class TestLeaderCustomerMember():

    def test_customer_get_staff_list(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/customer-member/leader',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json',
                        json={"group_id":1, "user_id": 3})
        res_json = json.loads(res.data)
        assert res.status_code == 200
