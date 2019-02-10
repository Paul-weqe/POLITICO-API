import unittest
import json 
import sys 
sys.path.insert(0, "../..")

from politico_api.tests.functions_for_tests import bytes_to_dict
from politico_api.config import app

class TestPartyID(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
    
    # the partyID can only be a positive number
    # we will use -1 to test what happens when a negative number is used for the userID
    # we expect a 406 error since the activity cannot be allowed
    """
    def test_response_when_partyid_is_negative(self):
        response = self.client.get("/api/v1/users/-1")
        self.assertEqual(response.status_code, 406)
    

    # the partyID only starts from 1
    # we will use 0 to test what happens when 0 is used for the userID
    # a 406 error is expected since the activity is not allowed
    def test_response_when_partyid_is_zero(self):
        response = self.client.get("/api/v1/users/0")
        self.assertEqual(response.status_code, 406)

    
    # since this route looks for a specific user, the userID must be an id of a user that exists
    # this method tests for what happens when a userID is entered that does not exist as an id of any of the users
    # a 404 error is expected since the user does not exist
    def test_response_when_partyid_does_not_exist(self):
        response = self.client.get("/api/v1/users/4000")
        self.assertEqual(response.status_code, 404)
    

    # the userID is the id of a specific user which is an integer. 
    # this method tests for when a string is used instead of an integer
    # this should bring a 406 error which will tell the user that the specified action is not permitted
    def test_response_when_partyid_is_not_an_integer(self):
        response = self.client.get("/api/v1/users/notinteger")
        self.assertEqual(response.status_code, 406)
        """
