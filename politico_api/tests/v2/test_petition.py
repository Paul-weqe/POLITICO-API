"""
This file will be used to test the elements contained in users_blueprint
Each class will be named Test<methodname> e.g if testing for POST, we will be naming the class TestPost
"""
from politico_api.tests.v2.config_test_v2 import BaseTest
import json
import ast


class TestCreatePetition(BaseTest):
    
    def test_with_valid_cridentials(self):

        # create the office against which to file a petition
        token = self.get_token()
        office_data = {
            "office_name": "President", "office_type": "legislative"
        }
        response = self.client.post("/api/v2/office", data=json.dumps(office_data), query_string={"db": "test"}, 
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        petition_data = {
            "office": 1, "body": "This is not right"
        }
        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")

        self.assertEqual(response.status_code, 201)

    def test_with_non_existing_office(self):
        token = self.get_token()
        petition_data = {
            "office": 1, "body": "This is not right"
        }
        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        self.assertIn(b"Office could not be found", response.data)
        self.assertEqual(response.status_code, 404)
    
    
    def test_with_missing_field(self):
        token = self.get_token()
        petition_data = {
            "office": 1
        }

        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        self.assertIn(b"body is a required field", response.data)
        self.assertEqual(response.status_code, 400)

    def test_with_wrong_datatype(self):
        token = self.get_token()
        petition_data = {
            "office": 1, "body": 23
        } 

        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        self.assertIn(b"body must be a <class 'str'>", response.data)
        self.assertEqual(response.status_code, 400)
         
    