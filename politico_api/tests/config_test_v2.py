import unittest
from politico_api.v2 import create_app
from config import TestConfig
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.u = UserConnection()
        self.app = create_app(TestConfig)
        self.u.reset_database("reset.txt")
        self.client = self.app.test_client()
        
        self.create_user_data = dict(
            first_name = "random_first",
	        last_name =  "random_last",
	        other_name = "random_other",
	        email =  "random@random.com",
	        phone_number = "07107273",
	        passport_url = "random_url",
            password = "random_password",
            is_admin = False,
            is_politician = False
        )

        self.change_password_data = dict(
            email = "random@random.com", old_password= "random_password", new_password = "new_random_password",
        )
        
        # self.u.reset_database()
        

    def tearDown(self):
        self.u.reset_database()