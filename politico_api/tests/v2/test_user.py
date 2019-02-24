"""
This file will be used to test the elements contained in users_blueprint
Each class will be named Test<methodname> e.g if testing for POST, we will be naming the class TestPost
"""
from politico_api.tests.v2.config_test_v2 import BaseTest
import json
import ast

class TestCreateUser(BaseTest):
    # tests for when creating a user
    # the fields that are required are named in the config_test_v2.py vairble called self.create_user_data

    
    def test_with_correct_fields(self):
        # tests when every field is okay 
        user_data = self.create_user_data
        token = self.get_token()

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"}, 
                    content_type="application/json", data=json.dumps(user_data), 
                    headers={"Authorization": "Bearer {}".format(token)})
        
        print(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_missing_field(self):
        # tests when one of the mandatory fields is absent
        # in this case, we will test when there is no email and see the response gotten
        user_data = self.create_user_data
        del user_data["email"]
        token = self.get_token()

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"email is a mandatory field", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_datatype(self):
        # tests when the wrong data type is used to send in the JSON data
        # for example, when expecting a string and a float is sent
        # in this case, we will send username as an integer(1) when a string is expected
        token = self.get_token()
        user_data = self.create_user_data
        user_data["username"] = 1

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"username has to be a <class 'str'>", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_email_format(self):
        # tests for the structure of the email address that is used
        # emails are expected to be in the format 'email@email.com' otherwise response should show an error
        token = self.get_token()
        user_data = self.create_user_data
        user_data["email"] = "this is an email"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"email is not in the valid email structure", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_blank_field(self):
        # none of the mandatory fields should be blank
        # this tests when the username is blank
        token = self.get_token()
        user_data = self.create_user_data
        user_data["username"] = " "

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"username cannot be empty", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_phone_number(self):
        token = self.get_token()
        user_data = self.create_user_data
        user_data["phone_number"] = "07107"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"phone_number is not in the valid phone number structure", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_common_password(self):
        token = self.get_token()
        user_data = self.create_user_data
        user_data["password"] = "password"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        # self.assertIn(b"your password must have at least a special character, a small letter, a capital letter and a number", response.data)
        self.assertIn(b"password should not be a commonly used password", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_weak_password(self):
        token = self.get_token()
        user_data = self.create_user_data
        user_data["password"] = "thisismyweakpassword"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"your password must have at least a special character, a small letter, a capital letter and a number", response.data)
        # self.assertIn(b"password should not be a commonly used password", response.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_value(self):
        token = self.get_token()
        user_data = self.create_user_data
        user_data["email"] = " "

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        # self.assertIn(b"your password must have at least a special character, a small letter, a capital letter and a number", response.data)
        # self.assertIn(b"password should not be a commonly used password", response.data)
        self.assertIn(b"email cannot be empty", response.data)
        self.assertEqual(response.status_code, 400)
    
class TestChangeUserPassword(BaseTest):
    # tests for when a user wants to change their password
    # we will be creating a new user and trying to change their passwords
    def test_with_correct_credentials(self):

        # first create the user
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)

        # change password of created user
        change_password_data = self.change_password_data

        response = self.client.patch("/api/v2/auth/change-password", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(change_password_data))
        print(response.data)
        self.assertEqual(response.status_code, 200)
    
    # tests when the user does not keep the correct old password
    def test_when_old_password_is_wrong(self):
        # first create the user
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)

        # change password of created user
        change_password_data = self.change_password_data
        change_password_data["old_password"] = "1234"

        response = self.client.patch("/api/v2/auth/change-password", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(change_password_data))
        print(response.data)

        self.assertIn(b"the old password you entered is not correct", response.data)
        self.assertEqual(response.status_code, 404)
    

    # tests when one of the mandatory fields is left blank
    def test_with_empty_email(self):
        # first create the user
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)

        # change password of created user
        change_password_data = self.change_password_data
        change_password_data["email"] = " "

        response = self.client.patch("/api/v2/auth/change-password", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(change_password_data))
        print(response.data)

        self.assertIn(b"email cannot be empty", response.data)
        self.assertEqual(response.status_code, 400)

    
    def test_with_invalid_password(self):
        # first create the user
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)

        # change password of created user
        change_password_data = self.change_password_data
        change_password_data["new_password"] = "thisiskenya"

        response = self.client.patch("/api/v2/auth/change-password", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(change_password_data))
        print(response.data)

        self.assertIn(b"your password must have at least a special character, a small letter, a capital letter and a number", response.data)
        self.assertEqual(response.status_code, 400)

    def test_with_invalid_email(self):
        # create the user
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)

        # change password of created user
        change_password_data = self.change_password_data
        change_password_data["email"] = "not valid email"

        response = self.client.patch("/api/v2/auth/change-password", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(change_password_data))
        print(response.data)

        self.assertIn(b"email is not in the correct email structure(e.g abc@abc.com)", response.data)
        self.assertEqual(response.status_code, 400)
        

class TestMakeAdmin(BaseTest):
    """
    This class tests for when a user wants to become an admin
    one can only become an admin by promotion by another admin
    The admin that will be used will be "paul@paul.com" who will try and promote a newly created user Kari to an admin
    """

    def test_with_valid_cridentials(self):
        # login admin
        admin_data = { "email": "paul@paul.com", "password": "Omwene11@" }
        response = self.client.post("/api/v2/auth/login", query_string={"db": "test"}, content_type="application/json",
                        data=json.dumps(admin_data))
        
        self.assertEqual(response.status_code, 200)
        token = ast.literal_eval(response.data.decode("utf-8"))["token"]
        
        # create another user
        user_data = self.create_user_data
        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"}, content_type="application/json",
                        data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)

        # promote user to an admin
        response = self.client.put("/api/v2/auth/make-admin/2", query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        print(response.data)
        self.assertEqual(response.status_code, 200)

        