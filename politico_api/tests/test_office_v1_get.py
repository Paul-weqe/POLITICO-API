# allow for import from the politico_app folder 
import sys
import json
import unittest
from politico_api.tests.config_test import BaseTest


# converts bytes responses to dictionaries. Meant for when the JSON response is received in bytes, it can be transformed to a dictionary
def bytes_to_dict(byte_input):
    dict_output = json.loads(byte_input.decode())
    return dict_output


class TestOfficeID(BaseTest):
    """
    This class carries out test on the officeID for the 'GET' method in the '/offices/<officeID>' route
    the description of each test is on the one or two line comment before each function that starts with "test_"
    """
    

    # test for if the officeID in the GET request for '/offices/<officeID>' is negative
    # should return a 404 error whenever the officeID is negative. 
    def test_offices_when_officeID_is_negative(self):
        response = self.client.get("/api/v1/offices/-1")
        response_data = bytes_to_dict(response.data)
        expected_data = { "status": 406, "error": "officeID cannot be zero or a negative number" }

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(response_data, expected_data)
    
    # test for if the officeID in the GET request for '/offices/<officeID>' is zero
    # should return a 404 error whenever the officeID is negative
    def test_offices_when_officeID_is_zero(self):
        response = self.client.get("/api/v1/offices/0")
        response_data = bytes_to_dict(response.data)
        expected_data = { "status": 406, "error": "officeID cannot be zero or a negative number" }

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(response_data, expected_data)
    
    # test for officeID with a number that is not an id of an office
    # this should return a 404 error since an office with the ID does not exist
    def test_offices_when_officeID_is_4000000(self):
        response = self.client.get("/api/v1/offices/4000000")
        response_data = bytes_to_dict(response.data)
        expected_data = { "status": 406, "error": "Could not find office with id 4000000" }

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(response_data, expected_data)
    
    # test for officeID with a number that is not real
    # these include -j and -i 
    def test_offices_when_officeID_not_real_numbers(self):
        response = self.client.get("/api/v1/offices/-j")

        self.assertEqual(response.status_code, 406)
    
    # test for officeID with a string instad of an integer. The string 'thisID' will be used
    # this should return a 404 error 
    def test_offices_when_officeID_is_string(self):
        response = self.client.get("/api/v1/offices/thisID")
        response_data = bytes_to_dict(response.data)
        expected_data = { "status": 406, "error": "office id must be an integer" }
        print(response_data)

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(response_data, expected_data)

class TestEmptyRequest(BaseTest):
    """
    This class is meant to test for a get request without any parameters
    basically sends a '/offices' without anything more
    """
    
    def test_response(self):
        response = self.client.get("/api/v1/offices")
        self.assertEqual(response.status_code, 200)
    

