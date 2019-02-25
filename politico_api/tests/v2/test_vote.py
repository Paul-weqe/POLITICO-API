from politico_api.tests.v2.config_test_v2 import BaseTest
import json

class TestCastVote(BaseTest):

    def test_with_relevant_parameters(self):
        "Tests for when all the necessary valid parameters are kept"
        # create a user
        self.client.post("/api/v2/auth/signup", data=json.dumps(self.create_user_data), content_type="application/json",
                    query_string={"db": "test"})

        # create an office
        token = self.get_token()
        self.client.post("/api/v2/office", data=json.dumps({"office_name": "president", "office_type": "legislative"}), 
                    query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")

        # create a party
        self.client.post("/api/v2/party", data=json.dumps(self.create_party_data), query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)},
                    content_type="application/json")

        # create a candidate
        self.client.post("/api/v2/office/1/register", data=json.dumps({"candidate_username": "kari", "party_name": "democrats"}), 
                    headers={"Authorization": "Bearer {}".format(token)}, query_string={"db": "test"}, content_type="application/json")
        
        # vote for the candidate
        response = self.client.post("/api/v2/votes", data=json.dumps({"candidate_id": 2, "office_id": 1}), query_string={"db": "test"},
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        # carry out the tests
        self.assertIn(b"successfully casted your vote...", response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_with_non_existing_user(self):
        "Tests for when all the necessary valid parameters are kept"
        # create a user
        self.client.post("/api/v2/auth/signup", data=json.dumps(self.create_user_data), content_type="application/json",
                    query_string={"db": "test"})

        # create an office
        token = self.get_token()
        self.client.post("/api/v2/office", data=json.dumps({"office_name": "president", "office_type": "legislative"}), 
                    query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")

        # create a party
        self.client.post("/api/v2/party", data=json.dumps(self.create_party_data), query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)},
                    content_type="application/json")
        
        # vote for the candidate
        response = self.client.post("/api/v2/votes", data=json.dumps({"candidate_id": 2, "office_id": 1}), query_string={"db": "test"},
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        # carry out the tests
        self.assertIn(b"candidate could not be found", response.data)
        self.assertEqual(response.status_code, 404)
    
    def test_vote_twice(self):
        "Tests for the response when we vote twice for the same office"
        # create a user
        self.client.post("/api/v2/auth/signup", data=json.dumps(self.create_user_data), content_type="application/json",
                    query_string={"db": "test"})

        # create an office
        token = self.get_token()
        self.client.post("/api/v2/office", data=json.dumps({"office_name": "president", "office_type": "legislative"}), 
                    query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")

        # create a party
        self.client.post("/api/v2/party", data=json.dumps(self.create_party_data), query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)},
                    content_type="application/json")

        # create a candidate
        self.client.post("/api/v2/office/1/register", data=json.dumps({"candidate_username": "kari", "party_name": "democrats"}), 
                    headers={"Authorization": "Bearer {}".format(token)}, query_string={"db": "test"}, content_type="application/json")
        
        # vote for the candidate
        self.client.post("/api/v2/votes", data=json.dumps({"candidate_id": 2, "office_id": 1}), query_string={"db": "test"},
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        response = self.client.post("/api/v2/votes", data=json.dumps({"candidate_id": 2, "office_id": 1}), query_string={"db": "test"},
                    headers={"Authorization": "Bearer {}".format(token)}, content_type="application/json")
        
        # carry out the tests
        self.assertIn(b"user 1 has already voted for that office", response.data)
        self.assertEqual(response.status_code, 400)