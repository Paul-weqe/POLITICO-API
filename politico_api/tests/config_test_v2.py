import unittest
from politico_api.v2 import create_app
from config import TestConfig

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        self.data = {
            "first_name": "Ruth",
	        "last_name": "Nekesa",
	        "other_name": "Waswa",
	        "email": "ruth@ruth.com",
	        "phone_number": "07107273",
	        "passport_url": "ruth passport URL",
            "is_admin": False, 
            "is_politician": False
        }

