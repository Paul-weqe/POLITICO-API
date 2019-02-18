from politico_api.v2.views.users.users_blueprint import users_blueprint_v2
from politico_api.tests.config_test_v2 import BaseTest
from politico_api.tests.functions_for_tests import bytes_to_dict
import json

class TestMandatoryParameters(BaseTest):
    
    def test_when_email_is_missing(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            password="voter1_password"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("email is a mandatory field", response.data.decode("utf-8"))
    

    def test_when_password_is_missing(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email="voter1@voter1.com"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("password is a mandatory field", response.data.decode("utf-8"))
    
    def test_when_both_fields_are_present(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email="voter1@voter1.com", password="voter1_password"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 200)


class TestDataTypes(BaseTest):

    # email is supposed to be string
    def test_when_email_is_integer(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email=1, password="voter1_password@gmail.com"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("email must be a <class 'str'>", response.data.decode('utf-8'))

    
    def test_when_password_is_integer(self):
        response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
            email="voter1@voter1.com", password=1
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("password must be a <class 'str'>", response.data.decode('utf-8'))
