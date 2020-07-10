import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO
class TestUserStaff():
    def test_user_get(self, client, init_database):
        token =create_token_staff()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    def test_post_staff(self, client, init_database):
        token = create_token_leader()
        with open('/home/alta1/Downloads/kementan.png', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.post('/user',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'full_name':'tes',
                              'username':"derby",
                              'password':'alta123',
                              'status':"staff",
                              'address':"malang",
                              'position':"staff",
                              'leader_id': 2,
                             
                            #   'user_image':(imgStringIO1, 'img1.png')
                            })
        res_json = json.loads(res.data)
        assert res.status_code == 200


    def test_patch_staff(self, client, init_database):
        token = create_token_leader()
        with open('/home/alta1/Downloads/kementan.png', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.patch('/user/3',
                        content_type='multipart/form-data',
                        headers={'Authorization': 'Bearer ' + token},
                        data={'full_name':'tes',
                              'username':"derby",
                              'password':'alta123',
                              'status':"staff",
                              'address':"malang",
                              'position':"staff",
                              'leader_id': 2,
                             
                            #   'user_image':(imgStringIO1, 'img1.png')
                            })
        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestLeaderStaff():
    def test_post_leader(self, client, init_database):
       
        with open('/home/alta1/Downloads/kementan.png', 'rb') as img1:
            imgStringIO1 = BytesIO(img1.read())
        res = client.post('/user/leader',
                        content_type='multipart/form-data',
                        data={'full_name':'tes',
                              'username':"derby",
                              'password':'alta123',
                              'status':"leader",
                              'address':"malang",
                              'position':"leader",
                              'leader_id': 0,
                             
                            #   'user_image':(imgStringIO1, 'img1.png')
                            })
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_leader_get(self, client, init_database):
        token =create_token_leader()
        res = client.get('/user/leader',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_leader_delete(self, client, init_database):
        token = create_token_leader()
        res = client.delete('/user/3',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json')
        # res_json = json.loads(res.data)
        assert res.status_code == 200