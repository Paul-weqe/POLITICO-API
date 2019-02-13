import sys
import json
import unittest
from politico_api.v1 import create_app
from politico_api.tests.functions_for_tests import bytes_to_dict
app = create_app() 


class TestPartyId(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
    
    # write test for when the ID is not an integer
    # we will write for when the partyid is a string - 'notinteger'
    # we expect a 406 - not allowed error
    def test_for_when_partyid_is_string(self):
        response = self.client.delete("/api/v1/parties/notinteger")

        received_data = bytes_to_dict(response.data)
        expected_data = {"error":"partyID has to be a number", "status": 406}

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(expected_data, received_data)
    

    # test for if the partyID in '/api/v1/parties/<partyID>' is negative
    # should return a 406 error
    def test_for_when_partyid_is_negative(self):
        response = self.client.delete("/api/v1/parties/-1")

        received_data = bytes_to_dict(response.data)
        expected_data = {"status": 406, "error": "partyID cannot be 0 or a negative number"}

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(received_data, expected_data)

    # test for when a partyID that is not part of the current parties
    # should return a 404 error
    def test_for_when_partyid_is_4000(self):
        response = self.client.delete("/api/v1/parties/4000")

        expected_data = { "status": 406, "error": "unable to delete party with ID 4000" }
        received_data = bytes_to_dict(response.data)
        
        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(expected_data, received_data)
    
    # test for when for when the partyID is zero
    # should return a 406 error
    def test_for_when_partyid_is_zero(self):
        response = self.client.delete("/api/v1/parties/0")

        expected_data = {"status": 406, "error": "partyID cannot be 0 or a negative number"}
        received_data = bytes_to_dict(response.data)

        self.assertEqual(response.status_code, 406)
        self.assertDictEqual(expected_data, received_data)
    