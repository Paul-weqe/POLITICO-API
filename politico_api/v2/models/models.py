from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
from politico_api.v2.models.DBConnections.VoteConnectDb import VoteConnection
from politico_api.v2.models.DBConnections.OfficeConnectDb import OfficeConnection
from politico_api.v2.models.DBConnections.PetitionConnectDb import PetitionConnection
from politico_api.v2.models.DBConnections.CandidateConnectDb import CandidateConnection
from politico_api.v2.models.DBConnections.PartyConnectDb import PartyConnection
import os

class Candidate:

    def __init__(self, candidate_id=None, party_id=None, office_id=None, db=None):
        self.candidate_id = candidate_id
        self.party_id = party_id
        self.office_id = office_id
        self.office_conn = None
        self.db = db
        if self.db == None:
            self.candidate_conn = CandidateConnection()
        else:
            self.candidate_conn = CandidateConnection(DB_NAME=os.getenv('TEST_DATABASE_NAME'),
                                DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), DB_USER=os.getenv('TEST_DATABASE_USER'),
                                DB_HOST=os.getenv('TEST_DATABASE_HOST'))
    
    def create_candidate(self):
        return self.candidate_conn.create_candidate(self.candidate_id, self.party_id, self.office_id)
    

    def create_candidate_by_name(self, user_name, party_name, office_id):
        return self.candidate_conn.create_candidate_by_names(user_name, party_name, office_id)

class User:

    def __init__(self, db=None, **kwargs):
        self.kwargs = kwargs
        self.db = db
        if self.db == None:
            self.user_conn = UserConnection()
        else:
            self.user_conn = UserConnection(DB_NAME=os.getenv('TEST_DATABASE_NAME'),
                                DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), DB_USER=os.getenv('TEST_DATABASE_USER'),
                                DB_HOST=os.getenv('TEST_DATABASE_HOST'))

    def create_user(self):
        user_created = self.user_conn.insert_user(**self.kwargs)
        return user_created
    
    def change_password(self, email, old_password, new_password):
        return  self.user_conn.change_user_password(email, old_password, new_password)
        
    def get_user_by_email_and_password(self, email, password):
        return self.user_conn.find_by_email_password(email, password)
    
    def make_user_admin(self, user_id):
        return self.user_conn.make_user_admin(user_id)

class Vote:

    def __init__(self, voter_id=None, candidate_id=None, office_id=None, db=None):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.office_id = office_id
        self.db = db

        if self.db == None:
            self.vote_conn = VoteConnection()
        else:
            self.vote_conn = VoteConnection (DB_NAME=os.getenv('TEST_DATABASE_NAME'),
                                DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), DB_USER=os.getenv('TEST_DATABASE_USER'),
                                DB_HOST=os.getenv('TEST_DATABASE_HOST'))


    def create_vote(self):
        return self.vote_conn.cast_vote(self.voter_id, self.candidate_id, self.office_id)

class Office:

    def __init__(self, office_name=None, office_type=None, db=None):
        self.office_name = office_name
        self.office_type = office_type
        self.db = db
        if self.db == None:
            self.office_conn = OfficeConnection()
        else:
            self.office_conn = OfficeConnection(DB_NAME=os.getenv('TEST_DATABASE_NAME'),
                                DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), DB_USER=os.getenv('TEST_DATABASE_USER'),
                                DB_HOST=os.getenv('TEST_DATABASE_HOST'))
        
        
    def count_office_votes(self, office_id):
        results = self.office_conn.get_office_results(office_id)
        return results

    def create_office(self):
        return self.office_conn.create_office(self.office_name, self.office_type)
    
    def get_all_offices(self):
        return self.office_conn.get_all_offices()
    
    def get_office_by_id(self, office_id):
        return self.office_conn.get_office_by_id(office_id)

    def get_office_by_name(self, office_name):
        return self.office_conn.get_office_by_name(office_name)

class Petition:

    def __init__(self, created_by=None, office=None, body=None, db=None):
        self.created_by = created_by
        self.office = office
        self.body = body 
        self.db = db
        
        if self.db == None:
            self.petition_conn = PetitionConnection()
        else:
            self.petition_conn = PetitionConnection(DB_NAME=os.getenv('TEST_DATABASE_NAME'),
                                DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), DB_USER=os.getenv('TEST_DATABASE_USER'),
                                DB_HOST=os.getenv('TEST_DATABASE_HOST'))

    def create_petition(self):
        return self.petition_conn.create_petition(self.created_by, self.office, self.body)


class Party:
    def __init__(self, party_name=None, party_hq=None, party_logo=None, db=None):
        self.party_name = party_name 
        self.party_hq = party_hq
        self.party_logo = party_logo
        self.db = db
        
        if self.db == None:
            self.party_conn = PartyConnection()
        else:
            self.party_conn = PartyConnection(DB_NAME=os.getenv('TEST_DATABASE_NAME'),
                                DB_PASSWORD=os.getenv('TEST_DATABASE_PASSWORD'), DB_USER=os.getenv('TEST_DATABASE_USER'),
                                DB_HOST=os.getenv('TEST_DATABASE_HOST'))

    def create_party(self):
        return self.party_conn.create_party(self.party_name, self.party_hq, self.party_logo)
    
    def get_all_parties(self):
        return self.party_conn.get_all_parties()

