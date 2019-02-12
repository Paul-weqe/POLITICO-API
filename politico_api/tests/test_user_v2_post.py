import unittest
import sys 
import json

sys.path.insert(0, "../../..")
from politico_api.config import app
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
    

    # tests when all the strings are of the required data type
    def test_with_all_json_fields_correct(self):
        response = self.client.post("/api/v2/users/signup", data=json.dumps(dict(
            username="abc", email="abc@abc.com", password="abcpassword"
        )))

        UserModel.restructure_database()
        self.assertEqual(response.status_code, 200)

# class TestRequiredFields(unittest.TestCase):
#     """
#     The required fields are the ones that are mandatory to be present in the JSON for the request to be successful
#     in the POST for "/api/v2/users", the required fields are 'username', 'email' and 'password'
#     """

#     def setUp(self):
#         self.client = app.test_client()

#     # tests for when the email is not part of the json data
#     def test_when_email_is_absent(self):
#         response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
#             username="absentemailusername", password="absentemailpassword"
#         )))

#         UserModel.restructure_database()
#         self.assertEqual(response.status_code, 406)
    
#     # test for when username is not part of the json data
#     def test_when_username_is_absent(self):
#         response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
#             email="absentusernameemail", password="absentusernamepassword"
#         )))

#         UserModel.restructure_database()
#         self.assertEqual(response.status_code, 406)
    
#     # test when password is absent
#     def test_when_password_is_absent(self):
#         response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
#             email="absentpasswordemail", username="absentpasswordusername"
#         )))

#         UserModel.restructure_database()
#         self.assertEqual(response.status_code, 406)
    
#     # test when all the mandatory fields are present
#     def test_all_fields_present(self):
#         response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
#             email="abc@abc.com", username="abc", password="abcpassword"
#         )))

#         UserModel.restructure_database()
#         self.assertEqual(response.status_code, 200)

# class TestUserExists(unittest.TestCase):

#     def setUp(self):
#         self.client = app.test_client()
    
#     # check if an email being used already exists
#     def test_email_already_used(self):

#         # request for creating a user with the email
#         request_1 = self.client.post("/api/v2/users/signup", data=json.dumps(dict(
#             email="abc@abc.com", username="abc", password="abcpassword"
#         )))

#         # try to create another user with same email
#         request_2 = self.client.post("/api/v2/users/signup", data=json.dumps(dict(
#             email="abc@abc.com", username="abc", password="abcpassword"
#         )))

#         UserModel.restructure_database()
#         self.assertEqual(request_1.status_code, 200)
#         self.assertEqual(request_2, 406)


