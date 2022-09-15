from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConn

class VoteConnection:
    """
    this class creates a connection to the politico database
    SQL queries can be carried through methods in this class
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs_1 = kwargs
    
    def cast_vote(self, voter_id, candidate_id, office_id):
        with BaseConn(kwargs=self.kwargs_1) as base_conn:
            sql_command = """
            SELECT * from candidates where user_id={}
            """.format(candidate_id)
            base_conn.curr.execute(sql_command)
            candidates = base_conn.curr.fetchone()
            if candidates == None:
                return "Unable to find the candidate"
            
            sql_find_conflict = """
            select candidates.office_id from votes inner join candidates on candidates.user_id=votes.candidate_id and votes.voter_id={}
            """.format(voter_id)
            base_conn.curr.execute(sql_find_conflict)
            already_voted = base_conn.curr.fetchone()

            if already_voted != None:
                return "already voted"
            
            sql_insert = """
            INSERT INTO votes(voter_id, office_id, candidate_id) VALUES ({}, {}, {})
            """.format(voter_id, office_id, candidate_id)

            base_conn.curr.execute(sql_insert)
            base_conn.conn.commit()

            base_conn.close_connection()
            return True
    