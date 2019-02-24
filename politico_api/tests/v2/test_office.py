from politico_api.tests.v2.config_test_v2 import BaseTest
import json


class TestPost(BaseTest):
    """
    tests for the POST method of the '/api/v2/office/' route of the API
    this will be from the data types to blank fields being used
    """
    def test_when_correct(self):
        # tests what response is gotten when all the mandatory fields are filled and they are in the correct format 
        token = self.get_token()

        response = self.client.post("/api/v2/office", 
            headers={"Authorization": "Bearer {}".format(token)},
            query_string={'db': 'test'}, data=json.dumps(dict(
                office_type="legislative", office_name="psoapsi"
            )), content_type="application/json")
        print(response.data)

        self.assertEqual(response.status_code, 201)
    
    def test_field_absent(self):
        # tests what happens when one of the mandatory fields is absent
        # in this case, the office_name will be absent
        token = self.get_token()

        response = self.client.post("/api/v2/office", 
                        headers={"Authorization": "Bearer {}".format(token)},
                        query_string={'db': 'test'}, data=json.dumps(dict(
                            office_type="legislative"
                        )),content_type="application/json")
        
        self.assertIn(b"office_name is a mandatory field", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_data_type(self):
        # tests for when the data type of one of the fields is wrong e.g getting a string when an integer was expected
        # here, the office_type which is expected to be a string will be sent as an integer(1)
        token = self.get_token()

        response = self.client.post("/api/v2/office",
                        headers={"Authorization": "Bearer {}".format(token)},
                        query_string={"db":"test"}, data=json.dumps(dict(
                            office_type=1, office_name="MP"
                        )), content_type="application/json")

        self.assertIn(b"office_type must be a <class 'str'>", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_blank_field(self):
        # tests what happens when one of the fields that have been sent is blank
        # that is, when the field sent is equal to "" or " ". office_name will be blank in this case
        token = self.get_token()

        response = self.client.post("/api/v2/office",
                        headers={"Authorization": "Bearer {}".format(token)},
                        query_string={"db": "test"}, data=json.dumps(dict(
                            office_type="legislative", office_name=" "
                        )), content_type="application/json")
        
        self.assertIn(b"office_name cannot be empty", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_beginning_with_blank(self):
        # tests when a string of one of the mandatory fields starts with a blank character
        # in this case, the office_name will be equal to " name" which starts with a blank
        token = self.get_token()

        response = self.client.post("/api/v2/office",
                        headers={"Authorization": "Bearer {}".format(token)},
                        query_string={"db": "test"}, data=json.dumps(dict(
                            office_type="legislative", office_name=" name"
                        )), content_type="application/json")
        
        self.assertIn(b"office_name cannot start or end with a blank character", response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_wrong_content_type(self):
        # tests when the content type is not correct
        # we will leave the content type to be blank when the expected value is "application/json"
        token = self.get_token()

        response = self.client.post("/api/v2/office",
                        headers={"Authorization":"Bearer {}".format(token)},
                        query_string={"db":"test"}, data=json.dumps(dict(
                            office_type="legislative", office_name="name"
                        )))
        
        self.assertIn(b"the content type used must be 'application/json'", response.data)
        self.assertEqual(response.status_code, 406)


class TestGet(BaseTest):
    
    def test_correct_request_before_adding(self):
        response = self.client.get("/api/v2/office")
        self.assertEqual(response.status_code, 404)