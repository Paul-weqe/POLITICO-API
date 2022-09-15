from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConn


class PartyConnection:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def create_party(self, party_name, party_hq, party_logo):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            sql_command = """
            SELECT FROM PARTIES WHERE party_name='{}'
            """.format(party_name)
            base_conn.curr.execute(sql_command)
            party_exists = base_conn.curr.fetchone()
            if party_exists is not None:
                return "Party with name {} already exists".format(party_name)
            
            sql_command = """
            INSERT INTO parties(party_name, party_hq_address, party_logo_url) VALUES ('{}', '{}', '{}')
            """.format(party_name, party_hq, party_logo)
            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()
            return True
    

    def get_all_parties(self):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            sql_command = """
            SELECT * FROM parties
            """
            base_conn.curr.execute(sql_command)
            all_parties = base_conn.curr.fetchall()
            return all_parties