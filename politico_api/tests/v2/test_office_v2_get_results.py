from politico_api.tests.config_test_v2 import BaseTest
from politico_api.v2.views.office.office_blueprint import office_blueprint_v2


class TestDataTypes(BaseTest):
    
    # test when the office_id is not an integer
    def test_when_office_id_is_string(self):
        response = self.client.get("/api/v2/offices/get-office-results/string")
        print(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("office_id must be an integer", response.data.decode("utf-8"))
    
    def test_with_correct_data(self):
        response = self.client.get("/api/v2/offices/get-office-results/1")
        print(response.data)

        self.assertEqual(response.status_code, 200)
