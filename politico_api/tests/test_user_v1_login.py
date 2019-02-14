import json
import unittest
from politico_api.tests.config_test import BaseTest

class TestDataTypes(BaseTest):

    def test_when_email_is_integer(self):
        
        response = self.client.post("/api/v1/users/login", data=json.dumps(dict(
            email=1, password="password"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
    
    def test_when_password_is_integer(self):

        response = self.client.post("/api/v1/users/login", data=json.dumps(dict(
            email="paul@paul.com", password="password"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
    

class TestMandatoryFields(BaseTest):
    
    def test_when_email_is_absent(self):
        # create an account that will be used to login
        self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="paul@paul.com", password="password", username="paul"
        )), content_type="application/json")

        # the created account is used to login
        response = self.client.post("/api/v1/users/login", data=json.dumps(dict(
            password="password"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)

    
    def test_when_password_is_absent(self):
        response = self.client.post("/api/v1/users/login", data=json.dumps(dict(
            email="paul@paul.com"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)