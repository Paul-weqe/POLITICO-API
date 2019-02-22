from politico_api.tests.config_test_v2 import BaseTest
import json
import ast

class TestDataType(BaseTest):

    
        
    # first_name is supposed to be string, so we will test it with integer
    def test_when_first_name_is_integer(self):
        test_data = self.create_user_data
        test_data["first_name"] = 1
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name is supposed to be a <class 'str'>", response.data.decode('utf-8'))

    # last_name is supposed to be string, so we will test it with integer
    def test_when_last_name_is_integer(self):
        test_data = self.create_user_data
        test_data["last_name"] = 1
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
        self.assertIn("last_name is supposed to be a <class 'str'>", response.data.decode('utf-8'))
    
    
    def test_when_other_name_is_string(self):
        test_data = self.create_user_data
        test_data["other_name"] = ['this', 'is', 'it']
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))
        self.assertIn("other_name is supposed to be a <class 'str'>", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
    
    def test_when_email_is_decimal(self):
        test_data = self.create_user_data
        test_data["email"] = 1.0
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))
        self.assertIn("email is supposed to be a <class 'str'>", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
    
    
    def test_when_phone_number_is_tuple(self):
        test_data = self.create_user_data
        test_data["phone_number"] = (1, 2, 3)
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))
        self.assertIn("phone_number is supposed to be a <class 'str'>", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
    
    
    def test_when_passport_url_is_integer(self):
        test_data = self.create_user_data
        test_data["passport_url"] = 20
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertIn("passport_url is supposed to be a <class 'str'>", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
    
    
    def test_when_is_admin_is_string(self):
        test_data = self.create_user_data
        test_data["is_admin"] = "this"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
    
    
    def test_when_is_politician_is_string(self):
        test_data = self.create_user_data
        test_data["is_politician"] = "is a politician"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
    
    
    
    

class TestMandatoryFields(BaseTest):

    def test_when_first_name_is_absent(self):
        test_data = self.create_user_data
        del test_data["first_name"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
    
    def test_when_last_name_is_absent(self):
        test_data = self.create_user_data
        del test_data["last_name"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))
        
        self.assertEqual(response.status_code, 400)
    
    def test_when_other_name_is_absent(self):
        test_data = self.create_user_data
        del test_data["other_name"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
    
    def test_when_email_is_absent(self):
        test_data = self.create_user_data
        del test_data["email"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))
        
        self.assertEqual(response.status_code, 400)
    
    def test_when_phone_number_is_absent(self):
        test_data = self.create_user_data
        del test_data["phone_number"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
    
    def test_when_passport_url_is_absent(self):
        test_data = self.create_user_data
        del test_data["passport_url"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 400)
    
class TestValidation(BaseTest):
    """
    TESTS FOR VALIDATION OF THE FIELDS e.g email is something@something.com or phone number is 0712345678
    """

    # email should be in format abc@abc.com
    def test_when_email_is_wrong_format(self):
        test_data = self.create_user_data
        test_data["email"] = "not_valid_email"
        
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data), content_type="application/json")
        self.assertTrue(response.status_code, 400)

    # phone_number should be a 10 digit number 
    def test_when_phone_number_is_wrong_format(self):
        test_data = self.create_user_data
        test_data["phone_number"] = "07748949"
        
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data), content_type="application/json")
        self.assertTrue(response.status_code, 400)
    
    # url is supposed to be in the format: http://some_url.com
    def test_when_passport_url_is_wrong_format(self):
        test_data = self.create_user_data
        test_data["passport_url"] = "not_a_valid_url"

        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data), content_type="application/json")
        return self.assertEqual(response.status_code, 400)
        

   