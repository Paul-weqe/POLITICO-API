import psycopg2
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection
import os

class PetitionConnection(BaseConnection):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def create_petition(self, created_by, office, body):
        try:

            self.open_connection()
            
            ### command to make sure one does not create petition for the same office twice
            sql_if_has_filed_command = """
            SELECT * FROM petitions WHERE create_by={} and office={}
            """.format(created_by, office)
            self.curr.execute(sql_if_has_filed_command)

            entries = self.curr.fetchall()
            if len(entries) > 1: return None

            ### creates the petition
            sql_command = """
            INSERT INTO petitions(create_by, office, body) VALUES ({}, {}, '{}')
            """.format(created_by, office, body)
            
            self.curr.execute(sql_command)
            self.conn.commit()

            self.close_connection()
            return True

        except Exception as e:
            if type(e) == psycopg2.IntegrityError:
                return "Office could not be found"
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
            print(e)
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
            return False



