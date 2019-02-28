"""
Tests writen for the '/api/v2/party' route
this includes creating and getting party information
"""
from politico_api.tests.v2.config_test_v2 import BaseTest
import json
import ast


class TestCreatePetition(BaseTest):
    """
    Tests for petition creation to a particular office
    we first login as an admin, create an office then try and create a petition against the particular office
    """

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
        """
        Creating a petition should be done against a particular office
        in this test, we try and see what happens when the office does not exist
        """
        token = self.get_token()
        petition_data = {
            "office": 1, "body": "This is not right"
        }
        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        self.assertIn(b"Office could not be found", response.data)
        self.assertEqual(response.status_code, 404)
    
    
    def test_with_missing_field(self):
        """
        the required fields in the creation of a petition are 'office' and 'body'
        in this method, we test what happens when we send the request without the 'body'
        """
        token = self.get_token()
        petition_data = {
            "office": 1
        }

        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        self.assertIn(b"body is a required field", response.data)
        self.assertEqual(response.status_code, 400)

    def test_with_wrong_datatype(self):
        """
        the data types required for the fields are integer for the office and string for the body
        we test what happens when the body is an integer
        """
        
        token = self.get_token()
        petition_data = {
            "office": 1, "body": 23
        } 

        response = self.client.post("/api/v2/petitions", data=json.dumps(petition_data), query_string={"db": "test"},
                            headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        self.assertIn(b"body must be a <class 'str'>", response.data)
        self.assertEqual(response.status_code, 400)
         
    