import unittest 
from politico_api.tests.config_test import BaseTest

class TestDataType(BaseTest):

    def test_when_id_is_string(self):
        response = self.client.delete("/api/v1/users/mine")
        self.assertEqual(response.status_code, 400)


class TestNonExistentId(BaseTest):

    def test_when_id_not_in_system(self):
        response = self.client.delete("/api/v1/users/1000")
        self.assertEqual(response.status_code, 400)
    
    def test_when_id_is_negative(self):
        response = self.client.delete("/api/v1/users/-1")
        self.assertEqual(response.status_code, 400)


