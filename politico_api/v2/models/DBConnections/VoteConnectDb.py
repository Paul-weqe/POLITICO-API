import psycopg2
import os 
# from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection

class VoteConnection(BaseConnection):
    """
    this class creates a connection to the politico database
    SQL queries can be carried through methods in this class
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def cast_vote(self, voter_id, candidate_id, office_id):
        try:
            self.open_connection()
            print(candidate_id)

            sql_command = """
            SELECT * from candidates where user_id={}
            """.format(candidate_id)
            self.curr.execute(sql_command)
            candidates = self.curr.fetchone()
            if candidates == None:
                return "Unable to find the candidate"
            
            sql_find_conflict = """
            select candidates.office_id from votes inner join candidates on candidates.user_id=votes.candidate_id and votes.voter_id={}
            """.format(voter_id)
            self.curr.execute(sql_find_conflict)
            already_voted = self.curr.fetchone()

            if already_voted != None:
                return "already voted"
            
            sql_insert = """
            INSERT INTO votes(voter_id, office_id, candidate_id) VALUES ({}, {}, {})
            """.format(voter_id, office_id, candidate_id)

            self.curr.execute(sql_insert)
            self.conn.commit()

            self.close_connection()
            return True

        except Exception as e:
            print("!!! UNABLE TO CAST A VOTE !!!")
            print(e)
            print("!!! UNABLE TO CAST A VOTE !!!")
    
    