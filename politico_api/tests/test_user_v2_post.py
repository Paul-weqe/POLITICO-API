import unittest
import sys 
import json

sys.path.insert(0, "../../..")
from politico_api import app
from politico_api.v2.models.user import UserModel


class TestJsonDataTypes(unittest.TestCase):

    """
    tests the data types of the json fields in the POST for "/api/v2/users"
    the username should be a string, the password a string and the email a string
    if not, it should return a 406 error with a valid error message
    """
    
    def setUp(self):
        self.client = app.test_client()

    # username should be string
    # we will test with an integer
    # should return a 406 error 
    def test_when_username_is_4000(self):
        response = self.client.post("/api/v2/users/signup", data=json.dumps(dict(
            username=4000, email="abc@abc.com", password="abcpassword"
        )))

        UserModel.restructure_database()
        self.assertEqual(response.status_code, 406)
    
    # email should be string
    # we will test with an integer
    # should return a 406 error
    def test_when_email_is_1(self):
        response = self.client.post("/api/v2/users/signup", data=json.dumps(dict(
            username="abc", email=4, password="abcpassword"
        )))

        UserModel.restructure_database()
        self.assertEqual(response.status_code, 406)
    
    # password should be a string
    # we will test when password is an integer
    # should return a 406 error
    def test_when_password_is_1(self):
        response = self.client.post("/api/v2/users/signup", data=json.dumps(dict(
            username="abc", email="abc@abc.com", password=1
        )))
        
        UserModel.restructure_database()
        self.assertEqual(response.status_code, 406)
    