from politico_api.tests.config_test_v2 import BaseTest
import json
import ast

class TestDataType(BaseTest):

    
    def test_when_all_fields_are_correct_type(self):
        test_data = self.create_user_data
        test_data["email"] = "correct_typ@correct.com"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 200)
        
    # first_name is supposed to be string, so we will test it with integer
    def test_when_first_name_is_integer(self):
        test_data = self.create_user_data
        test_data["first_name"] = 1
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)

    # last_name is supposed to be string, so we will test it with integer
    def test_when_last_name_is_integer(self):
        test_data = self.create_user_data
        test_data["last_name"] = 1
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
        # first_name is supposed to be string, so we will test it with integer
    
    
    def test_when_other_name_is_string(self):
        test_data = self.create_user_data
        test_data["other_name"] = ['this', 'is', 'it']
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    
    
    def test_when_email_is_decimal(self):
        test_data = self.create_user_data
        test_data["email"] = 1.0
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    
    def test_when_phone_number_is_tuple(self):
        test_data = self.create_user_data
        test_data["phone_number"] = (1, 2, 3)
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    
    def test_when_passport_url_is_integer(self):
        test_data = self.create_user_data
        test_data["passport_url"] = 20
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    
    def test_when_is_admin_is_string(self):
        test_data = self.create_user_data
        test_data["is_admin"] = "this"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    
    def test_when_is_politician_is_string(self):
        test_data = self.create_user_data
        test_data["is_politician"] = "is a politician"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    
    
    

class TestMandatoryFields(BaseTest):

    def test_when_first_name_is_absent(self):
        test_data = self.create_user_data
        del test_data["first_name"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    def test_when_last_name_is_absent(self):
        test_data = self.create_user_data
        del test_data["last_name"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    def test_when_other_name_is_absent(self):
        test_data = self.create_user_data
        del test_data["other_name"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    def test_when_email_is_absent(self):
        test_data = self.create_user_data
        del test_data["email"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))
        
        self.assertEqual(response.status_code, 406)
    
    def test_when_phone_number_is_absent(self):
        test_data = self.create_user_data
        del test_data["phone_number"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    def test_when_passport_url_is_absent(self):
        test_data = self.create_user_data
        del test_data["passport_url"]
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 406)
    
    def test_when_is_admin_is_absent(self):
        test_data = self.create_user_data
        del test_data["is_admin"]
        test_data["email"] = "adminabsent@adminabsent.com"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 200)
    
    def test_when_is_politician_is_absent(self):
        test_data = self.create_user_data
        del test_data["is_politician"]
        test_data["email"] = "polititicanabsent@politician.com"
        response = self.client.post("/api/v2/users/signup", data=json.dumps(test_data))

        self.assertEqual(response.status_code, 200)
    
    
    