"""
This file will be used to test the elements contained in users_blueprint
This will be mainly using the '/api/v2/auth' route in the system
"""
from politico_api.tests.v2.config_test_v2 import BaseTest
import json
import ast

class TestCreateUser(BaseTest):
    """
    Tests for when creating a user
    the fields that are required are named in the config_test_v2.py vairble called self.create_user_data
    """

    
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
        """
        tests when one of the mandatory fields is absent
        in this case, we will test when there is no email sent in the creation of a user
        """
        user_data = self.create_user_data
        del user_data["email"]
        token = self.get_token()

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"email is a mandatory field", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_datatype(self):
        """
        tests when the wrong data type is used to send in the JSON data
        for example, when expecting a string and a float is sent
        in this case, we will send username as an integer(1) when a string is expected
        """

        token = self.get_token()
        user_data = self.create_user_data
        user_data["username"] = 1

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"username has to be a <class 'str'>", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_email_format(self):
        """
        tests for the structure of the email address that is used
        emails are expected to be in the format 'email@email.com' otherwise response should show an error
        """
        token = self.get_token()
        user_data = self.create_user_data
        user_data["email"] = "this is an email"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"email is not in the valid email structure", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_blank_field(self):
        """
        none of the mandatory fields should be blank
        this tests when the username is blank
        """
        token = self.get_token()
        user_data = self.create_user_data
        user_data["username"] = " "

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"username cannot be empty", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_phone_number(self):
        """
        phone number should have ten integer string e.g 0712345678
        this will test when a shorter value is used
        """
        token = self.get_token()
        user_data = self.create_user_data
        user_data["phone_number"] = "07107"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"phone_number is not in the valid phone number structure", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_common_password(self):
        """
        tests for if the password is a commonly used password
        the commonly used passwords are stored in the common_passwords.txt file and if the password used in amongst those, it will be declined
        we use 'password' as the password which is one of the commonly used passwords
        """
        token = self.get_token()
        user_data = self.create_user_data
        user_data["password"] = "password"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"password should not be a commonly used password", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_weak_password(self):
        """
        For a strong password, we required a small letter,  a capital letter and a number 
        This will test with only small letters and see the response
        """
        token = self.get_token()
        user_data = self.create_user_data
        user_data["password"] = "thisismyweakpassword"

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"your password must have at least a special character, a small letter, a capital letter and a number", response.data)
        self.assertEqual(response.status_code, 400)
        
    def test_empty_value(self):
        """
        None of the required fields in the self.create_user_data should be left blank
        This method will test for when the email is blank
        """
        token = self.get_token()
        user_data = self.create_user_data
        user_data["email"] = " "

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        self.assertIn(b"email cannot be empty", response.data)
        self.assertEqual(response.status_code, 400)
    
class TestChangeUserPassword(BaseTest):
    """
    tests for when a user wants to change their password
    The fields required are 'email', 'old_password' and 'new_password'
    'old_password' needs to match their current password in the system
    """

    def test_with_correct_credentials(self):
        "Tests when all the required fields are present in the correct format"
        "first create the user"
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
    
    
    def test_when_old_password_is_wrong(self):
        """
        The 'old_password' needs to be the current password of the user as is saved in the system
        this tesrs when the 'old_password' does not match the current password in the system
        """

        # create the user with password "Kari@1234"
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(user_data))
        
        self.assertEqual(response.status_code, 201)
        
        
        # try to change password of created user
        # the 'old_password' is supposed to be 'Kari@1234' but instead we use '1234'
        change_password_data = self.change_password_data
        change_password_data["old_password"] = "1234"

        response = self.client.patch("/api/v2/auth/change-password", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(change_password_data))
        print(response.data)

        self.assertIn(b"the old password you entered is not correct", response.data)
        self.assertEqual(response.status_code, 404)

    def test_with_empty_email(self):
        "None of the fields used should be left blank"
        "Test for what happens when one of the fields is left blank. We will use the 'email' field in this test"

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
        "Tests with a password that is not strong enough"
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
        token = self.get_token()
        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"}, content_type="application/json",
                        data=json.dumps(self.create_user_data))
        

        # promote user to an admin
        response = self.client.put("/api/v2/auth/promote-user/2", query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        print(response.data)
        self.assertEqual(response.status_code, 200)

        