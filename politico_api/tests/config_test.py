import unittest 
from politico_api.v1 import create_app

class BaseTest(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client()

        