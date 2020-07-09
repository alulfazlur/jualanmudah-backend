import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO


class TestUserContactGroupResource():
    
    def test_get_contact_group(self, client, init_database):
        token =create_token_staff()
        res = client.get('/user_contact_group',
                        headers={'Authorization': 'Bearer '+ token},
                        # data=json.dumps(),
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200