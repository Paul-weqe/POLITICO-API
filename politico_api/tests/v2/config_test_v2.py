import unittest
import json
from politico_api.v2 import create_app
from config import TestConfig, ProductionConfig
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection
import os
import ast

class BaseTest(unittest.TestCase):

    def setUp(self):
        print('set up')
        # self.app = create_app(TestConfig)
        # self.base = BaseConnection(
        #     DB_USER=os.getenv('TEST_DATABASE_USER'), DB_NAME=os.getenv('TEST_DATABASE_NAME'), DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), 
        #     DB_HOST=os.getenv('TEST_DATABASE_HOST')
        # )
        self.base.reset_database()

        self.client = self.app.test_client()
        
        self.query_data = {
            'db': 'test'
        }

        self.create_user_data = {
            "first_name": "Gideon", "last_name": "Koima", "other_name": "Kari", 
            "email": "kari@kari.com", 
            "phone_number": "0712345678",
            "passport_url": "http://paul.com",
            "password": "Kari@1234",
            "username": "kari"
        }

        self.change_password_data = {
            "email": "kari@kari.com",
            "old_password": "Kari@1234",
            "new_password": "Gideon@1234"
        }

        self.create_party_data = {
            "party_name": "democrats", 
            "party_hq": "New york",
            "party_logo": "http://democrats.com"
        }

    def tearDown(self):
        
        self.base = BaseConnection(
            DB_USER=os.getenv('TEST_DATABASE_USER'), DB_NAME=os.getenv('TEST_DATABASE_NAME'), DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), 
            DB_HOST=os.getenv('TEST_DATABASE_HOST')
        )
        self.base.reset_database()
    
    
    # gets a token for an admin
    def get_token(self):
        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(dict(
            email="paul@paul.com", password="Omwene11@"
        )), content_type="application/json")
        token = ast.literal_eval(login_response.data.decode("utf-8"))["token"]
        return token
    
    # gets a token for a normal user
    def get_normal_token(self):
        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(dict(
            email="kari@kari.com", password="Kari@1234"
        )), content_type="application/json")
        token = ast.literal_eval(login_response.data.decode("utf-8"))["token"]
        return token
        