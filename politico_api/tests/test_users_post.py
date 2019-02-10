import unittest
import json 
import sys 
sys.path.insert(0, "../..")

from politico_api.tests.functions_for_tests import bytes_to_dict
from politico_api.config import app 


class TestPresenceOfMandatoryFields(unittest.TestCase):

    """
    This tests for the presence of the mandatory fields
    """
    
    def setUp(self):
        self.client = app.test_client()
    
    """
    def test_result_when_first_name_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            last_name="LastName", other_name="OtherName", email="abc@abc.com", phone_number="07-7273749-345", passport_url="http://pass-url",
            is_admin=False 
        )))
        
        expected_response = { "status": 406, "error": "first_name is a mandatory field" }
        received_response = bytes_to_dict(response.data)
        
        self.assertDictEqual(expected_response, received_response)
        self.assertEqual(response.status_code, 404)

        
    def test_result_when_last_name_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name = "Paul", other_name="OtherName", email="abc@abc.com", phone_number="07-7273749-345", passport_url="http://pass-url",
            is_admin=False
        )))
        
        expected_response = { "status": 406, "error": "last_name is a mandatory field" }
        received_response = bytes_to_dict(response.data)
        
        self.assertDictEqual(expected_response, received_response)
        self.assertEqual(response.status_code, 404)

    def test_result_when_other_name_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name="Paul", last_name="LastName", email="abc@abc.com", phone_number="07-7273749-345", passport_url="http://pass-url",
            is_admin=False 
        )))
        
        expected_response = { "status": 406, "error": "other_name is a mandatory field" }
        received_response = bytes_to_dict(response.data)
        
        self.assertDictEqual(expected_response, received_response)

        self.assertEqual(response.status_code, 404)

    def test_result_when_email_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name="Paul", last_name="LastName", other_name="OtherName", phone_number="07-7273749-345", passport_url="http://pass-url",
            is_admin=False 
        )))
        
        expected_response = { "status": 406, "error": "email is a mandatory field" }
        received_response = bytes_to_dict(response.data)
        
        self.assertDictEqual(expected_response, received_response)
        self.assertEqual(response.status_code, 404)

    def test_result_when_phone_number_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name="Paul", last_name="LastName", other_name="OtherName", email="abc@abc.com", passport_url="http://pass-url", is_admin=False 
        )))
        
        expected_response = { "status": 406, "error": "phone_number is a mandatory field" }
        received_response = bytes_to_dict(response.data)
        
        self.assertDictEqual(expected_response, received_response)
        self.assertEqual(response.status_code, 406)

    def test_result_when_passport_url_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name="Paul", last_name="LastName", other_name="OtherName", email="abc@abc.com", phone_number="07-7273749-345", is_admin=False 
        )))
        
        expected_response = { "status": 406, "error": "passport_url is a mandatory field" }
        received_response = bytes_to_dict(response.data)
        
        self.assertDictEqual(expected_response, received_response)
        self.assertEqual(response.status_code, 406)

    def test_result_when_is_admin_not_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name="Paul", last_name="LastName", other_name="OtherName", email="abc@abc.com", phone_number="07-7273749-345", 
            passport_url="http://pass-url",
        )))
        expected_response = { "status": 406, "error": "is_admin is a mandatory field" }
        received_response = bytes_to_dict(response.data)

        self.assertEqual(response.status_code, 406)    
        self.assertDictEqual(expected_response, received_response)

    def test_result_when_all_fields_are_present(self):
        response = self.client.post("/api/v1/users/", data=json.dumps(dict(
            first_name="Paul", last_name="Smith", other_name="OtherName", email="abc@abc.com", phone_number="0771727347", 
            passport_url="http://pass-url", is_admin=True
        )))

        self.assertEqual(response.status_code, 200)
    """