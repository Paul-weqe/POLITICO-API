from politico_api.v2.views.votes.votes_blueprint import votes_blueprint_v2
from politico_api.tests.config_test_v2 import BaseTest
from politico_api.tests.functions_for_tests import bytes_to_dict
import json

class TestDataTypes(BaseTest):

    def test_when_all_fields_are_right(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email="voter1@voter1.com", password="voter1_password"
        )), content_type="application/json")

        received_dict = bytes_to_dict(response.data)
        token = received_dict["token"]

        response = self.client.post("/api/v2/votes/", data=json.dumps(dict(
            voter_id = 4, office_id = 1, candidate_id = 5, token=token
        )), content_type="application/json")

        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("successfully casted your vote...", response.data.decode("utf-8"))

    def test_when_candidate_id_is_string(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email="voter1@voter1.com", password="voter1_password"
        )), content_type="application/json")

        received_dict = bytes_to_dict(response.data)
        token = received_dict["token"]

        response = self.client.post("api/v2/votes", data=json.dumps(dict(
            voter_id=3, office_id=1, candidate_id="1", token=token
        )), content_type="application/json")

        print(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("candidate_id must be a <class 'int'>", response.data.decode("utf-8"))
    
    def test_when_office_id_is_string(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email="voter1@voter1.com", password="voter1_password"
        )), content_type="application/json")
        received_dict = bytes_to_dict(response.data)
        token = received_dict["token"]

        response = self.client.post("/api/v2/votes", data=json.dumps(dict(
            voter_id=3, office_id="2", candidate_id=1, token=token
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("office_id must be a <class 'int'>", response.data.decode("utf-8"))
    



