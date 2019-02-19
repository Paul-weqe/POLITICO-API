from politico_api.tests.config_test_v2 import BaseTest
from politico_api.v2.views.petition.petition_blueprint import peition_blueprint_v2
import json

class TestMandatoryFields(BaseTest):

    def test_when_created_by_is_absent(self):
        response = self.client.post("/api/v2/petitions", data=json.dumps(dict(
            office=1, body="not fair"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)
    
    def test_when_office_is_absent(self):
        response = self.client.post("/api/v2/petitions", data=json.dumps(dict(
            created_by=1, body="not fair"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)

class TestDataTypes(BaseTest):

    def test_when_created_by_is_string(self):
        response = self.client.post("/api/v2/petitions", data=json.dumps(dict(
            created_by="not_integer", office=1, body="This is the body"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 403)


class TestAlreadyAdded(BaseTest):

    def test_when_petition_is_already_added(self):
        response = self.client.post("/api/v2/petitions", data=json.dumps(dict(
            created_by=1, office=1, body="This is the body"
        )), content_type="application/json")

        response = self.client.post("/api/v2/petitions", data=json.dumps(dict(
            created_by=1, office=1, body="This is the body"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 403)