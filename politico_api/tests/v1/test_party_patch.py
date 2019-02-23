# allow for import from the politico_app folder 
import unittest
import sys
import json
from politico_api.tests.functions_for_tests import bytes_to_dict
from politico_api.tests.config_test import BaseTest

class TestJsonDataTypes(BaseTest):

    # in /api/v1/parties/<partyID>/<partyName>-PATCH, the partyID should be an integer
    # we will use a string which should return a 404 error
    def test_party_when_partyID_is_string(self):
        response = self.client.patch("/api/v1/parties/notinteger", data=json.dumps(dict(
            party_name="DOIDS"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 405)

class TestMandatoryFields(BaseTest):
    
    # PATCH for '/api/v1/parties/<partyID>/<partyName>' requires both partyID and partyName
    # We will test for what happens when we miss one of the fields. We expect a 405 status code
    def test_response_without_a_single_field(self):
        response = self.client.patch("/api/v1/parties/only_field", data=json.dumps(dict(
            party_name="POLITICO"
        )) ,content_type="application/json")

        # self.assertDictEqual()
        self.assertEqual(response.status_code, 405)
        
