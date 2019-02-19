import unittest
from politico_api.v2 import create_app
from config import TestConfig, ProductionConfig
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
import os

class BaseTest(unittest.TestCase):

    def setUp(self):
        
        self.app = create_app(ProductionConfig)
        self.client = self.app.test_client()
        
        self.u = UserConnection(
            DB_NAME = self.app.config['DATABASE_NAME'], DB_PASSWORD= self.app.config['DATABASE_PASSWORD'],
            DB_USER = self.app.config['DATABASE_USER'], DB_HOST = self.app.config['DATABASE_HOST']
            )
        
        self.u.reset_database("schema.txt")
        
        self.create_user_data = dict(
            first_name = "random_first",
	        last_name =  "random_last",
	        other_name = "random_other",
	        email =  "random@random.com",
	        phone_number = "0712345678",
	        passport_url = "random_url",
            password = "random_password",
            is_admin = False,
            is_politician = False
        )

        self.change_password_data = dict(
            email = "random@random.com", old_password= "random_password", new_password = "new_random_password",
        )
        
        self.u.reset_database()
        

    def tearDown(self):
        self.u.reset_database()