"""
This file will be used to test the elements contained in users_blueprint
Each class will be named Test<methodname> e.g if testing for POST, we will be naming the class TestPost
"""
from politico_api.tests.v2.config_test_v2 import BaseTest
import json
import ast

class TestCreateParty(BaseTest):
    def test_with_valid_cridentials(self):
        party_data = self.create_party_data
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        print("##")
        print(response.data)
        self.assertEqual(response.status_code, 201)
        
    def test_with_fields_missing(self):
        party_data = self.create_party_data
        del party_data["party_name"]
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_name is a mandatory field", response.data)
    
    def test_with_wrong_datatypes(self):
        party_data = self.create_party_data
        party_data["party_name"] = 10
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_name has to be a <class 'str'>", response.data)
    
    def test_invalid_logo(self):
        party_data = self.create_party_data

        # a URL is expected when we are inputing the party logo
        party_data["party_logo"] = "not a url"
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_logo field has to be a url", response.data)
    
    def test_blank_field(self):
        party_data = self.create_party_data
        party_data["party_name"] =" "
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_name cannot be empty", response.data)

class TestGetParties(BaseTest):

    def test_valid_request(self):
        response = self.client.get("/api/v2/party")

        self.assertEqual(response.status_code, 200)
    
    def test_wrong_method(self):
        response = self.client.put("/api/v2/party")

        self.assertEqual(response.status_code, 405)
        self.assertIn(b"That method cannot be used for this page", response.data)
    
    