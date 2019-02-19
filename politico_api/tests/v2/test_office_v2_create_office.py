from politico_api.tests.config_test_v2 import BaseTest
from politico_api.v2.views.office.office_blueprint import office_blueprint_v2
import json
import ast

# def bytes_to_dict(string_input):
#     return ast.literal_eval(string_input)

class TestMandatoryFields(BaseTest):

    def test_when_office_name_is_absent(self):

        response = self.client.post("/api/v2/offices/", data=json.dumps(dict(
            office_type="popopo"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)
    
    def test_when_office_type_is_absent(self):
        response = self.client.post("/api/v2/offices/", data=json.dumps(dict(
            office_name="office-name"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)
    
    

class TestDataTypes(BaseTest):
    def test_when_office_name_is_integer(self):
        response = self.client.post("/api/v2/offices", data=json.dumps(dict(
            office_name=1, office_type="this office name"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)

    
    def test_when_office_type_is_integer(self):
        response = self.client.post("/api/v2/offices", data=json.dumps(dict(
            office_name="this office name", office_type=1
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)
    3
    