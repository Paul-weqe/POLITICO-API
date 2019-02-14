from politico_api.tests.config_test_v2 import BaseTest
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
import json



class TestDataTypes(BaseTest):

    """
    for each function, we will create an acoount then try t change the password and eventually delete the account
    """

    
    def test_when_all_fields_present(self):
        test_data = self.change_password_data
        response = self.client.patch("/api/v2/users/change-password", data=json.dumps(test_data), content_type="application/json")
        
        self.assertEqual(response.status_code, 406)
    
    
    def test_when_old_password_is_integer(self):

        test_data = self.change_password_data
        test_data["old_password"] = 1000
        response = self.client.patch("/api/v2/users/change-password", data=json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, 406)

        
    def test_when_email_is_integer(self):

        test_data = self.change_password_data
        test_data["email"] = 1000
        response = self.client.patch("/api/v2/users/change-password", data=json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, 406)
    
    def test_when_new_password_is_integer(self):

        test_data = self.change_password_data
        test_data["new_password"] = 5000
        response = self.client.patch("/api/v2/users/change-password", data=json.dumps(test_data), content_type="application/json")

        self.assertEqual(response.status_code, 406)
    
