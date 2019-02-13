# allow for import from the politico_app folder 
import unittest
import sys
import json
from politico_api.v1 import create_app

app = create_app()

class TestJsonDataTypes(unittest.TestCase):
    """
    This class is meant for testing the data types of the JSON data being POSTed to the '/offices' route
    for instance some fields require only a string
    """
    def setUp(self):
        self.client = app.test_client()
    
    # tests for when the wrong data type is used for office_type
    # this method uses office_type=2 which is an integer. A string is the required data type. 
    # A 404 status code is expected
    def test_when_office_type_is_integer(self):
        response = self.client.post("/api/v1/offices", data = json.dumps(dict(
            office_type=2, office_name="Prime minister"
        )), content_type="application/json")
        
        self.assertEqual(response.status_code, 406)
        
    # tests for when the wrong data type us used for office_name
    # this method uses office_name=2 which is an integer. A string is the required data type. 
    # A 404 status code is expected
    def test_when_office_name_is_integer(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(dict(
            office_type="legislative", office_name=2
        )), content_type="application/json")
        self.assertEqual(response.status_code, 406)

    # tests when both requierd fields, 'office_name' and 'office_type' use the correct data types
    # both are strings. A 200 status code is expected
    def test_when_all_json_inputs_correct(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(dict(
            office_type="legislative", office_name="President"
        )), content_type="application/json")
        self.assertEqual(response.status_code, 200)

class TestMandatoryFields(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # tests for when a POST request is sent to the '/offices' route without the office_name being part of the data that is sent
    # a 406 error is sent since this is a mandatory field
    def test_response_without_office_name(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(dict(
            office_type="legislative"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 406)

    # tests for when a POST request is sent to the '/offices' route without the office_type being part of the data that is sent
    # a 406 error is expected since this is a mandatory field
    def test_response_without_office_type(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(dict(
            office_name="President"
        )), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        
    # tests for when all the mandatory fields are sent in the JSON with the POST request to the '/offices' route
    # a 200 status code is expected
    def test_when_all_fields_present(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(dict(
            office_name="President", office_type="legislative"
        )), content_type="application/json")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
