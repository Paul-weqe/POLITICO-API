from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConn

class PetitionConnection:
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs


    def create_petition(self, created_by, office, body):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            
            ### command to make sure one does not create petition for the same office twice
            sql_if_has_filed_command = """
            SELECT * FROM petitions WHERE create_by={} and office={}
            """.format(created_by, office)
            base_conn.curr.execute(sql_if_has_filed_command)

            entries = base_conn.curr.fetchall()
            if len(entries) > 1: return None

            ### creates the petition
            sql_command = """
            INSERT INTO petitions(create_by, office, body) VALUES ({}, {}, '{}')
            """.format(created_by, office, body)
            
            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()

            return True
