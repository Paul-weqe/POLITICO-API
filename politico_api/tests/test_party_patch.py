# allow for import from the politico_app folder 
import unittest
import sys
import json
sys.path.insert(0,'../..')

from politico_api.config import app 

class TestJsonDataTypes(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()

    # in /api/v1/parties/<partyID>/<partyName>-PATCH, the partyID should be an integer
    # we will use a string which should return a 404 error
    def test_party_when_partyID_is_string(self):
        response = self.client.patch("/api/v1/parties/notinteger/ODM")

        self.assertEqual(response.status_code, 404)

    # in /api/v1/parties/<partyID>/<partyName>-PATCH, the partyName should be a string
    # it should not contain special characters such as () 
    # we will use [notstring] in place of partyName and expect a 404 error
    def test_party_when_partyName_is_list(self):
        response = self.client.patch("/api/v1/parties/1/[notstring]")
        
        self.assertEqual(response.status_code, 404)

class TestMandatoryFields(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
    
    # PATCH for '/api/v1/parties/<partyID>/<partyName>' requires both partyID and partyName
    # We will test for what happens when we miss one of the fields. We expect a 405 status code
    def test_response_without_a_single_field(self):
        response = self.client.patch("/api/v1/parties/only_field")

        self.assertEqual(response.status_code, 405)
