import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO


class TestSentResource():

    def test_sent_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/sent',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # def test_sent_get_staff_none(self, client, init_database):
    #     token =  create_token_staff()
    #     res = client.get('/sent/5',
    #                     headers={'Authorization': 'Bearer '+ token},
    #                     content_type='application/json')
    #     res_json = json.loads(res.data)
        # assert res.status_code == 404


    def test_post_sent_staff(self, client, init_database):
        token = create_token_staff()
        res = client.post('/sent',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"status":"", "send_date": "now","subject":"mock","content":"2020-06-06","device":"email","contact_id":2,"group_id":1})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_patch_sent_staff(self, client, init_database):
        token = create_token_staff()
        res = client.patch('/sent',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        json={"status":"opened", "send_date": "now","send_id":1,"subject":"mock","content":"2020-06-06","device":"email","contact_id":1,"group_id":1})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_sent_staff(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/sent/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_sent_staff_none(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/sent/10',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        # assert res.status_code == 
        assert res.status_code == 404
    


# class TestSendMailDirect():

#     def test_sent_post_leader(self, client, init_database):
#         token =  create_token_staff()
#         res = client.post('/sent/direct',
#                         content_type='application/json',
#                         headers={'Authorization': 'Bearer '+ token},
#                         json={"status":"", "send_date": "now","subject":"mock","content":"2020-06-06","device":"email","contact_id":1,"group_id":1})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
class TestgetDraftById():

    def test_sent_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/sent/draft',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json',
                        query_string=1)
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
#     def test_post_customer_leader(self, client, init_database):
#         token = create_token_leader()
#         res = client.post('/sent/leader',
#                         content_type='application/json',
#                         headers={'Authorization': 'Bearer '+ token},
#                         json={"First_name":"mas", "last_name": "prayogo","email":"derby@gmail.com","phone":"0895122332","bod":"2020-06-06","address":"malang","gender":"male","company":"alterra","user_id":3})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

    

