import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token_admin,create_token_leader,create_token_staff, init_database
from io import BytesIO


class TestTrackList():

    def test_track_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/track',
                        headers={'Authorization': 'Bearer '+ token},
                        content_type='application/json',
                        query_string={
                            "sent_id":1
                        })
        res_json = json.loads(res.data)
        assert res.status_code == 200


class TestTrackOpen():

    def test_track_open_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/track/open',
                        content_type='application/json',
                        query_string={
                            "sent_id":2,
                            "customer_id":2
                        })
        res_json = json.loads(res.data)
        assert res.status_code == 404


class TestTrackClick():

    def test_track_click_get_staff(self, client, init_database):
        token =  create_token_staff()
        res = client.get('/track/click',
                        content_type='application/json',
                        query_string={
                            "sent_id":2,
                            "customer_id":2
                        })
        res_json = json.loads(res.data)
        assert res.status_code == 404
