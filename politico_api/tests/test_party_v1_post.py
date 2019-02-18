# allow for import from the politico_app folder 
import sys
import json
import unittest
from politico_api.tests.functions_for_tests import bytes_to_dict
from politico_api.tests.config_test import BaseTest

class TestMandatoryFields(BaseTest):
    """
    This class will be used to test for the presence of all the required fields in the JSON of the POST data to the
    '/parties' route 
    the mandatory fields are: 
        party_name, party_hq_address, party_motto, party_members and party_logo_url
    """
    
    # this will test for the response when there is no party name in the POSTed JSON to '/parties'
    # should return a 404 error
    def test_party_name_not_present(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_hq_address="Kenya", party_logo_url="thelogo",
            party_motto="this is us", party_members=4000 # notice to party_name
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        
    # test for response when there is no party_hq_address in the POSTed JSON to '/parties'
    # should return a 404 error
    def test_party_hq_address_not_present(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_motto="this is us", party_members=4000 
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)

    # test for response when there is no party_logo_url in the POSTed JSON to '/parties'
    # should return a 404 error 
    def test_party_logo_url_not_present(self):
        response = self.client.post("/api/v1/parties", data = json.dumps(dict(
            party_name="another party", party_hq_address = "Kenya", party_motto="this is us", party_members=3000,
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        
    
    # test for response when there is no party_members in the POSTed JSON to '/parties'
    # should return a 404 error
    def test_party_members_not_present(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_hq_address="Kenya", party_motto="this is us"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)

    # test for response when there is no party_motto in the POSTed JSON to '/parties'
    # should return a 404 error
    def test_party_motto_not_present(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_hq_address="Kenya", party_members=3000
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
    
    # test for response when all the fields are present
    # should return a 200 status 
    def test_all_party_fields_present(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_hq_address="Kenya", party_motto="this is us", party_members=200
        )), content_type="application/json")

        # response_data = bytes_to_dict(response.data)
        self.assertEqual(response.status_code, 201)
    

class TestFieldsDataTypes(BaseTest):
    """
    This class will be used to test for the validity of the data types of JSON fields POSTed to the server's
    '/parties' route 
    e.g if a field is supposed to be an integer, only an integer will lead to the correct 200 response
    """
    
    
    # test if party_name only accepts strings. party_name will be an integer
    # should return 404
    def test_when_party_name_is_integer(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name=3, party_logo_url="thelogo", party_hq_address="Kenya", party_motto="this is us", party_members=200
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
    

    # test if party_logo_url only accepts strings. party_name will be a list
    # should return 404
    def test_when_party_logo_url_is_list(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url=[1, 2, 3], party_hq_address="Kenya", party_motto="this is us", party_members=200
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)


    # test if party_hq_address only accepts strings. party_hq_address will be a float
    # should return 404
    def test_when_party_hq_address_is_float(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_hq_address=21.1, party_motto="this is us", party_members=200
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
    
    # test if party_motto only accepts strings. party_name will be an integer
    # should return 404
    def test_when_party_motto_is_integer(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_hq_address="Kenya", party_motto=1, party_members=200
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)

    # test if party_members only accepts integer. party_members will be a String
    # should return 404
    def test_when_party_members_is_integer(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name="another party", party_logo_url="thelogo", party_hq_address="Kenya", party_motto="this is us", party_members="two hundred"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
    
    # test when all the fields have the correct values
    # should return 404
    def test_with_all_valid_fields(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(dict(
            party_name =  "DEMO", party_hq_address =  "HQ", party_logo_url = "LOGO", party_motto = "MOTO", party_members =  4000
        )), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        
