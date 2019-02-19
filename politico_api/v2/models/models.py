from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
from politico_api.v2.models.DBConnections.VoteConnectDb import VoteConnection
from politico_api.v2.models.DBConnections.OfficeConnectDb import OfficeConnection
from politico_api.v2.models.DBConnections.PetitionConnectDb import PetitionConnection

class User:

    
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def create_user(self):
        new_user = UserConnection()
        user_created = new_user.insert_user(**self.kwargs)
        return user_created
    
    def change_password(self, email, old_password, new_password):
        user = UserConnection()
        return  user.change_user_password(email, old_password, new_password)
        
    def get_user_by_email_and_password(self, email, password):
        user = UserConnection()
        # return user.find_user_by_email_and_password(email, password)
        return user.find_by_email_password(email, password)

class Vote:

    def __init__(self, voter_id=None, office_id=None, candidate_id=None):
        self.voter_id = voter_id
        self.office_id = office_id
        self.candidate_id = candidate_id

    def create_vote(self):
        new_vote =VoteConnection()
        return new_vote.create_vote(self.voter_id, self.office_id, self.candidate_id)

class Office:

    def __init__(self, office_name=None, office_type=None):
        self.office_name = office_name
        self.office_type = office_type
        
    def count_office_votes(self, office_id):
        office_conn = OfficeConnection()
        results = office_conn.get_office_results(office_id)
        return results

    def create_office(self):
        office_conn = OfficeConnection()
        return office_conn.create_office(self.office_name, self.office_type)
    
    def get_all_offices(self):
        office_conn = OfficeConnection()
        return office_conn.get_all_offices()

class Petition:

    def __init__(self, created_by=None, office=None, body=None):
        self.created_by = created_by
        self.office = office
        self.body = body 
    
    def create_petition(self):
        petition_conn = PetitionConnection()
        return petition_conn.create_petition(self.created_by, self.office, self.body)
