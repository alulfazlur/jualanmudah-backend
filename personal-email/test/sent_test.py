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
    #     token =  create_token_helper()
    #     res = client.get('/sent',
    #                     headers={'Authorization': 'Bearer '+ token},
    #                     content_type='application/json')
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 404


    def test_post_sent_staff(self, client, init_database):
        token = create_token_staff()
        res = client.post('/sent',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        data=json.dumps({"status":"draft", "send_date": "now","subject":"mock","content":"2020-06-06","device":"email","contact_id":2,"group_id":1}))
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_patch_sent_staff_error(self, client, init_database):
        token = create_token_staff()
        res = client.patch('/sent',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        data=json.dumps({"status":"sent", "send_date": "now","sent_id":10,"subject":"mock","content":"<p>a</p>","device":"email","contact_id":1,"group_id":2,"words":"",
                        "link":""}))
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_patch_sent_staff(self, client, init_database):
        token = create_token_staff()
        res = client.patch('/sent',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        data=json.dumps({"status":"sent",
                        "send_date": "now",
                        "sent_id":2,
                        "subject":"mock",
                        "content":"<p>a</p>",
                        "device":"email",
                        "contact_id":1,
                        "group_id":1,
                        "words":"link",
                        "link":"youtube.com"}))
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
        res = client.delete('/sent/9999999',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        # assert res.status_code == 
        assert res.status_code == 404
    


# class TestSendMailDirect():

#     def test_post_direct_sent_staff(self, client, init_database):
#         token = create_token_staff()
#         res = client.post('/sent/direct',
#                         content_type='application/json',
#                         json={"status":"", "send_date": "now","subject":"mock","content":"2020-06-06","device":"email","contact_id":1,"group_id":1,"words":"klik aja","link":"youtube.com"},
#                         headers={'Authorization': 'Bearer '+ token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
# class TestgetDraftById():

#     def test_sent_get_draft(self, client, init_database):
#         token =  create_token_staff()
#         res = client.get('/sent/draft',
#                         headers={'Authorization': 'Bearer '+ token},
#                         content_type='application/json',
#                         query_string={"draft_id":2})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
# class TestGetAllDraft():
#     def test_sent_get_all_draft(self, client, init_database):
#         token =  create_token_staff()
#         res = client.get('/sent/draft-list',
#                         headers={'Authorization': 'Bearer '+ token},
#                         content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 200  

# class TestGetAllSent():
#     def test_sent_get_all_sent(self, client, init_database):
#         token =  create_token_staff()
#         res = client.get('/sent/sent-list',
#                         headers={'Authorization': 'Bearer '+ token},
#                         content_type='application/json')
#         res_json = json.loads(res.data)
#         assert res.status_code == 200 
    

