import psycopg2
import os 

from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection


class PartyConnection(BaseConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def create_party(self, party_name, party_hq, party_logo):
        try:
            self.open_connection()

            sql_command = """
            SELECT FROM PARTIES WHERE party_name='{}'
            """.format(party_name)
            self.curr.execute(sql_command)
            party_exists = self.curr.fetchone()
            if party_exists is not None:
                return "Party with name {} already exists".format(party_name)
            
            sql_command = """
            INSERT INTO parties(party_name, party_hq_address, party_logo_url) VALUES ('{}', '{}', '{}')
            """.format(party_name, party_hq, party_logo)
            self.curr.execute(sql_command)
            self.conn.commit()

            self.close_connection()
            return True

        except Exception as e:
            print("!!! UNABLE TO CREATE A PARTY !!!")
            print(e)
            print("!!! UNABLE TO CREATE A PARTY !!!")
    

    def get_all_parties(self):
        try:
            self.open_connection()

            sql_command = """
            SELECT * FROM parties
            """
            self.curr.execute(sql_command)
            all_parties = self.curr.fetchall()

            self.close_connection()
            return all_parties
        except Exception as e:
            print("!!! UNABLE TO LIST PARTIES !!!")
            print(e)
            print("!!! UNABLE TO LIST PARTIES !!!")
