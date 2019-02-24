from politico_api.tests.v2.config_test_v2 import BaseTest
import json

class TestCastVote(BaseTest):

    # def test_correct_data(self):

    #     # create the user
    #     response = self.client.post("/api/v2/auth/signup", content_type="application/json", data=json.dumps(self.create_user_data), 
    #                         query_string={"db":"test"})
        
    #     # create an office
    #     token = self.get_token()
    #     response = self.client.post("/api/v2/office", content_type="application/json",
    #                         data=json.dumps({"office_name": "DC", "office_type": "federal"}), 
    #                         headers={"Authorization": "Bearer {}".format(token)}, query_string={"db": "test"})
    #     print("OFFICE")
    #     print(response.data)
        
    #     # create a party
    #     party_data = self.create_party_data
    #     response = self.client.post("/api/v2/party", content_type="application/json", 
    #                         data=json.dumps(party_data), query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})
        
        
    #     # create a candidate
    #     response = self.client.post("/api/v2/office/1/register", content_type="application/json", data=json.dumps({
    #         "candidate_username": "kari", "party_name": "democrats"
    #     }), query_string={"db": "test"}, headers={"Authorization": "Bearer {}".format(token)})

    #     # vote for the candidate
    #     response = self.client.post("/api/v2/votes", content_type="application/json", data=json.dumps({"candidate_id": 2}), 
    #                         headers={"Authorization": "Bearer {}".format(token)})

    #     print("CANDIDATE VOTE")
    #     print(response.data)
    #     self.assertEqual(response.status_code, 201)
    
    def test_with_wrong_datatype(self):
        # create the user
        response = self.client.post("/api/v2/auth/signup", content_type="application/json", data=json.dumps(self.create_user_data), 
                            query_string={"db":"test"})
        
        # create an office
        token = self.get_token()
        response = self.client.post("/api/v2/office", content_type="application/json",
                            data=json.dumps({"office_name": "DC", "office_type": "federal"}), headers={"Authorization": "Bearer {}".format(token)})
        
        # create a party
        party_data = self.create_party_data
        response = self.client.post("/api/v2/party", content_type="application/json", 
                            data=json.dumps(party_data), query_string={"db": "test"})
        
        # create a candidate
        response = self.client.post("/api/v2/office/1/register", content_type="application/json", data=json.dumps({
            "candidate_username": "kari", "party_name": "democrats"
        }), query_string={"db": "test"})

        # vote for the candidate
        response = self.client.post("/api/v2/votes", content_type="application/json", data=json.dumps({"candidate_id": ""}), 
                            headers={"Authorization": "Bearer {}".format(token)})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"candidate_id must be a <class 'int'>", response.data)
    
    def test_without_candidate(self):
        # create the user
        response = self.client.post("/api/v2/auth/signup", content_type="application/json", data=json.dumps(self.create_user_data), 
                            query_string={"db":"test"})
        
        # create an office
        token = self.get_token()
        response = self.client.post("/api/v2/office", content_type="application/json",
                            data=json.dumps({"office_name": "DC", "office_type": "federal"}), headers={"Authorization": "Bearer {}".format(token)})
        
        # create a party
        party_data = self.create_party_data
        response = self.client.post("/api/v2/party", content_type="application/json", 
                            data=json.dumps(party_data), query_string={"db": "test"})
        
        # create a candidate
        response = self.client.post("/api/v2/office/1/register", content_type="application/json", data=json.dumps({
            "candidate_username": "kari", "party_name": "democrats"
        }), query_string={"db": "test"})

        # vote for the candidate
        response = self.client.post("/api/v2/votes", content_type="application/json", data=json.dumps({}), 
                            headers={"Authorization": "Bearer {}".format(token)})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"candidate_id is a mandatory field", response.data)
    
    def test_with_invalid_candidate(self):
        # create the user
        response = self.client.post("/api/v2/auth/signup", content_type="application/json", data=json.dumps(self.create_user_data), 
                            query_string={"db":"test"})
        
        # create an office
        token = self.get_token()
        response = self.client.post("/api/v2/office", content_type="application/json",
                            data=json.dumps({"office_name": "DC", "office_type": "federal"}), headers={"Authorization": "Bearer {}".format(token)})
        
        # create a party
        party_data = self.create_party_data
        response = self.client.post("/api/v2/party", content_type="application/json", 
                            data=json.dumps(party_data), query_string={"db": "test"})
        
        # create a candidate
        response = self.client.post("/api/v2/office/1/register", content_type="application/json", data=json.dumps({
            "candidate_username": "kari", "party_name": "democrats"
        }), query_string={"db": "test"})

        # vote for the candidate
        response = self.client.post("/api/v2/votes", content_type="application/json", data=json.dumps({"candidate_id": 10}), 
                            headers={"Authorization": "Bearer {}".format(token)})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"candidate could not be found", response.data)


