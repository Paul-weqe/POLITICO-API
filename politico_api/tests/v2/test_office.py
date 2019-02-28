"""
Tests for the '/api/v2/office' route
BaseTest contains the main test elements that will be used
"""
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
    
    # tests for getting a list of all the offices
    # this should not bring any errors
    def test_correct_request_before_adding(self):
        response = self.client.get("/api/v2/office")
        self.assertEqual(response.status_code, 200)


class TestCreateCandidate(BaseTest):
    """
    tests for registering a candidate for a particular office
    '/api/office/<officeId>/register'
    takes the JSON fields "party_name" and "candidate_username" both of which should have already been registered
    """
    def test_when_correct(self):

        # create a user that will run for an office
        user_data = self.create_user_data

        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"}, 
                    content_type="application/json", data=json.dumps(user_data))
        
        # create a party that the user will vie with
        party_data = self.create_party_data
        token = self.get_token()

        response = self.client.post("/api/v2/party", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(party_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        # create the office to be run for 
        token = self.get_token()
        office_data = {"office_name": "MP", "office_type": "legislative"}
        response = self.client.post("/api/v2/office", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(office_data),
                    headers={"Authorization": "Bearer {}".format(token)})
            
        get_offices = self.client.get("/api/v2/office")
        print(get_offices.data)
        
        # run for the office :)
        token = self.get_token()
        candidate_data = {"party_name": "democrats", "candidate_username": "kari"}

        response = self.client.post("/api/v2/office/1/register", data=json.dumps(candidate_data),
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json",
                    query_string={"db": "test"})
        
        self.assertEqual(response.status_code, 201)

    def test_without_user(self):
        """
        to register as a candidate for a particular office, we require "candidate_username" and "party_name"
        in this test, we will run the program with a "candidate_username" that does not exist
        """

        party_data = self.create_party_data
        token = self.get_token()

        # create party "democrats" that will be used to run for the office
        response = self.client.post("/api/v2/party", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(party_data),
                    headers={"Authorization": "Bearer {}".format(token)})
        
        # create the office to be run for 
        token = self.get_token()
        office_data = {"office_name": "MP", "office_type": "legislative"}
        response = self.client.post("/api/v2/office", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(office_data),
                    headers={"Authorization": "Bearer {}".format(token)})

        # run for the office without a valid candidate "kari" that has not been created
        token = self.get_token()
        candidate_data = {"party_name": "democrats", "candidate_username": "kari"}

        response = self.client.post("/api/v2/office/1/register", data=json.dumps(candidate_data),
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json",
                    query_string={"db": "test"})
        
        self.assertIn(b"User with name kari not found", response.data)
        self.assertEqual(response.status_code, 400)

    def test_without_party(self):
        """
        Try and run for an office with a party that has not been created
        Th party to be run using is specified using the "party_name" in the JSON fields
        """

        # create a user that will run for an office
        user_data = self.create_user_data
        
        # create the user
        response = self.client.post("/api/v2/auth/signup", query_string={"db": "test"}, 
                    content_type="application/json", data=json.dumps(user_data))
        
        # create an office
        token = self.get_token()
        office_data = {"office_name": "MP", "office_type": "legislative"}
        response = self.client.post("/api/v2/office", query_string={"db": "test"},
                    content_type="application/json", data=json.dumps(office_data),
                    headers={"Authorization": "Bearer {}".format(token)})

        get_offices = self.client.get("/api/v2/office")
        print(get_offices.data)

        # run for the office with an invalid party
        token = self.get_token()
        candidate_data = {"party_name": "democrats", "candidate_username": "kari"}

        response = self.client.post("/api/v2/office/1/register", data=json.dumps(candidate_data),
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json",
                    query_string={"db": "test"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Party with name democrats not found", response.data)

class TestGetById(BaseTest):
    """
    Tests for getting a specific office using the ID of the office
    use the '/api/v2/office/<officeID>' route where officeID is the identifier of the office which information we want
    """

    def test_with_valid_id(self):
        """
        Create an office, since they are identified by a serial, its ID will be 1
        Then get the office information, a request that is supposed to be successful
        """

        # create the office
        token = self.get_token()
        office_data = {"office_name": "president", "office_type": "legislative"}
        response = self.client.post("/api/v2/office", data=json.dumps(office_data), 
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json", 
                    query_string={"db": "test"})
        

        # get the information of the office with ID 1 using '/api/v2/office/<officeId>' where officeId is 1    
        response = self.client.get("/api/v2/office/1", query_string={"db": "test"})
        print(response.data)
        
        self.assertEqual(response.status_code, 200)
    

    def test_with_invalid_id(self):
        """
        Get an office whose ID does not exist
        notice there is no office created but the information about the specific office is being requested
        """
        # try to get an office that has not yet been created
        response = self.client.get("/api/v2/office/1", query_string={"db": "test"})

        print(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Office with ID 1 could not be found", response.data)

class TestGetResults(BaseTest):
    """
    Tests for getting results for a specific office 'ThIs Is GoIng tO bE a LoNg OnE'
    tests mainly using the route '/api/v2/office/<officeID>/result'
    You have to create a candidate with all valid credentials, create a user to vote for them and finally vote for the candidate
    all steps illustrated below the respective comments below
    TODO: write more tests on the results
    """
    def test_when_valid(self):
        # create a user
        self.client.post("/api/v2/auth/signup", query_string={"db":"test"}, content_type="application/json",
            data=json.dumps(self.create_user_data))

        # create an office
        token = self.get_token()
        self.client.post("/api/v2/office", query_string={"db":"test"}, content_type="application/json", data=json.dumps({
            "office_name": "president", "office_type":"legislative"
        }), headers={"Authorization": "Bearer {}".format(token)})

        # create a party
        self.client.post("/api/v2/party", query_string={"db":"test"}, content_type="application/json", data=json.dumps(self.create_party_data),
            headers={"Authorization": "Bearer {}".format(token)})

        # create a candidate for an office
        self.client.post("/api/v2/office/1/register", query_string={"db":"test"}, content_type="application/json", data=json.dumps({
            "candidate_username":"koima", "party_name": "democrats"
        }), headers={"Authorization": "Bearer {}".format(token)})

        # vote for a candidate
        self.client.post("/api/v2/votes", query_string={"db":"test"}, content_type="application/json", data=json.dumps({
            "candidate_id": 2, "office_id": 1
        }), headers={"Authorization": "Bearer {}".format(token)})

        # get results after the vote
        results = self.client.get("/api/v2/office/1/result", query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        print(results.data)
        self.assertEqual(results.status_code, 200)