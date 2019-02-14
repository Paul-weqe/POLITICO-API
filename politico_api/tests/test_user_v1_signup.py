import unittest
import json
from politico_api.tests.config_test import BaseTest

class TestMandatoryFields(BaseTest):

    def test_when_email_is_absent(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            username="paul", password="paulpassword"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
    
    def test_when_username_is_absent(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="paul@gmail.com", password="paulpassword"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
    
    def test_when_password_is_absent(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="paul@gmail.com", password="paulpassword"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_when_all_fields_are_present(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="paul@gmail.com", password="paulpassword", username="paul"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 200)


class TestDuplicate(BaseTest):

    def test_when_email_duplicates_are_used(self):
        # trying to create an account that was created above
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="paul@gmail.com", password="paulpassword", username="paul" 
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)

class TestDataTypes(BaseTest):

    def test_when_email_is_1(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email=1, password="paulpassword", username="paul"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
    
    def test_when_username_is_1(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="email1@email1.com", password="paulpassword", username=1
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)
    
    def test_when_password_is_integer(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="abc@abc.com", password=500, username="paul"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_when_all_data_types_are_correct(self):
        response = self.client.post("/api/v1/users/signup", data=json.dumps(dict(
            email="abc@abc.com", password="abcpassword", username="abc"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 200)

        
    

