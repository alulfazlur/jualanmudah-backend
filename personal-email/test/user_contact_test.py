import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO
class TestUserContactResource():
    def test_post_staff_contact(self, client, init_database):
        token = create_token_staff()
        res = client.post('/usercontact',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        data=json.dumps({"user_id":3, "contact_id": 1,"email_or_wa":"jinadabf@gmail.com","password":"bountyhunter"}))
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_patch_staff_contact(self, client, init_database):
        token = create_token_staff()
        res = client.patch('/usercontact/3',
                        content_type='application/json',
                        headers={'Authorization': 'Bearer '+ token},
                        data=json.dumps({"user_id":3, "contact_id": 1,"email_or_wa":"jinadabf@gmail.com","password":"bountyhunter"}))
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_staff_contact(self, client, init_database):
        token = create_token_staff()
        res = client.delete('/usercontact/1',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 200


class TestListUserContact():

    def test_get_contact_list(self, client, init_database):
        token =create_token_staff()
        res = client.get('/usercontact/list',
                        headers={'Authorization': 'Bearer '+ token},
                        # data=json.dumps(),
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestUserContactLeader():

    def test_get_contact_leader(self, client, init_database):
        token =create_token_leader()
        res = client.get('/usercontact/leader',
                        headers={'Authorization': 'Bearer '+ token},
                        data=json.dumps({"user_id":2}),
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200