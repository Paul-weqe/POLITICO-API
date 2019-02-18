import sys
import json
import unittest
from politico_api.tests.functions_for_tests import bytes_to_dict
from politico_api.tests.config_test import BaseTest


class TestPartyId(BaseTest):
    
    # write test for when the ID is not an integer
    # we will write for when the partyid is a string - 'notinteger'
    # we expect a 406 - not allowed error
    def test_for_when_partyid_is_string(self):
        response = self.client.delete("/api/v1/parties/notinteger")
        self.assertEqual(response.status_code, 405)
    

    # test for if the partyID in '/api/v1/parties/<partyID>' is negative
    # should return a 406 error
    def test_for_when_partyid_is_negative(self):
        response = self.client.delete("/api/v1/parties/-1")
        self.assertEqual(response.status_code, 405)

    # test for when a partyID that is not part of the current parties
    # should return a 404 error
    def test_for_when_partyid_is_4000(self):
        response = self.client.delete("/api/v1/parties/4000")
        self.assertEqual(response.status_code, 404)

    
    # test for when for when the partyID is zero
    # should return a 406 error
    def test_for_when_partyid_is_zero(self):
        response = self.client.delete("/api/v1/parties/0")
        self.assertEqual(response.status_code, 400)