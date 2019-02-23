import unittest
from politico_api.v2 import create_app
from config import TestConfig, ProductionConfig
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
import os

class BaseTest(unittest.TestCase):

    def setUp(self):
        
        self.app = create_app(ProductionConfig)
        self.app = create_app()
        self.client = self.app.test_client()

        self.change_password_data = dict(
            email = "random@random.com", old_password= "random_password", new_password = "new_random_password",
        )
        