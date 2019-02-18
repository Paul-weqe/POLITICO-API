from politico_api.tests.config_test_v2 import BaseTest
from politico_api.v2.views.office.office_blueprint import office_blueprint_v2
import json
import ast

# def bytes_to_dict(string_input):
#     return ast.literal_eval(string_input)

# class TestDataTypes(BaseTest):

#     def test_when_office_name_is_absent(self):
#         # response = self.client.post("/api/v2/users/login", data=json.dumps(dict(
#         #     email="voter1@voter1.com", password="voter1_password"
#         # )), content_type="application/json")

#         response = self.client.post("/api/v2/offices/", data=json.dumps(dict(
#             office_type="popopo"
#         )), content_type="application/json")

#         self.assertEqual(response.status_code, 403)
#         self.assertIn("office_name is a mandatory field", response.data.decode("utf-8"))
    