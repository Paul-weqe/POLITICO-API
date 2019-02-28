"""
Tests writen for the '/api/v2/party' route
this includes creating and getting party information
"""
from politico_api.tests.v2.config_test_v2 import BaseTest
import json
import ast

class TestCreateParty(BaseTest):
    """
    Tests for the creation of a party
    The fields needed to create a party have been defined as self.create_party_data in the BaseTest
    """

    def test_with_valid_cridentials(self):
        # tests when all the fields required are used in their correct format
        party_data = self.create_party_data
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        print("##")
        print(response.data)
        self.assertEqual(response.status_code, 201)
        
    def test_with_fields_missing(self):
        # tests when one of the mandatory fields 'party_name' is not present
        party_data = self.create_party_data
        del party_data["party_name"]
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_name is a mandatory field", response.data)
    
    def test_with_wrong_datatypes(self):
        """
        tests when the wrong data types is used for one of the fields
        'party_name' is required to be a string but will be tested as an integer
        """
        party_data = self.create_party_data
        party_data["party_name"] = 10
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_name has to be a <class 'str'>", response.data)
    
    def test_invalid_logo(self):
        """
        The logo is required to be in a http URL format
        We will try to input the party_logo in another format that is not a valid URL
        """
        party_data = self.create_party_data

        # a URL is expected when we are inputing the party logo
        party_data["party_logo"] = "noT A uRl"
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_logo field has to be a url", response.data)
    
    def test_blank_field(self):
        """
        Tests when one of the mandatory fields is a blank
        we will use the 'party_name' as a blank field
        """
        party_data = self.create_party_data
        party_data["party_name"] =" "
        token = self.get_token()
        response = self.client.post("/api/v2/party", data=json.dumps(party_data), content_type="application/json",
                                query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"party_name cannot be empty", response.data)

class TestGetParties(BaseTest):
    """
    Tests for trying to get a list of all the parties
    this uses GET '/api/v2/party'
    """
    def test_valid_request(self):
        response = self.client.get("/api/v2/party")

        self.assertEqual(response.status_code, 200)
    
    def test_wrong_method(self):
        # When we try using the PUT method instead of the GET method
        response = self.client.put("/api/v2/party")

        self.assertEqual(response.status_code, 405)
        self.assertIn(b"That method cannot be used for this page", response.data)
    
    