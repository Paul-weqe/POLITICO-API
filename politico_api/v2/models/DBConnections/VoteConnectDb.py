import psycopg2
import os 
# from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection


class VoteConnection:
    """
    this class creates a connection to the politico database
    SQL queries can be carried through methods in this class
    """
    def __init__(self, **kwargs):
        self.conn = None 
        self.curr = None 
        self.kwargs = None 
        if len(kwargs) > 0:
            self.kwargs = kwargs
        

    def open_connection(self):
        try:
            print(self.kwargs)
            if self.kwargs==None:
                self.conn = psycopg2.connect(
                    user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host=os.getenv("DATABASE_HOST"), database=os.getenv("DATABASE_NAME")
                )
                self.curr = self.conn.cursor()
                print("connection established")
            else:
                self.conn = psycopg2.connect(
                    user=self.kwargs["DB_USER"], password=self.kwargs["DB_PASSWORD"], host="localhost", database=self.kwargs["DB_NAME"]
                )
                self.curr = self.conn.cursor()
                print("Connection  established test")

        except Exception as e:
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
            print(e)
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
    
    def close_connection(self):
        try:
            if (self.conn):
                self.curr.close()
    
        except Exception as e:
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
            print(e)
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
    
    def create_vote(self, voter_id, candidate_id):
        try:
            self.open_connection()

            sql_command = """
            SELECT user_id from candidates where user_id={}
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
            
            sql_command = """
            INSERT INTO votes(voter_id, candidate_id) VALUES ({}, {})
            """.format(voter_id, candidate_id)
            self.curr.execute(sql_command)
            self.conn.commit()

            # checks if the user has already voted for that office
            self.close_connection()
            return True

        except Exception as e:
            print("!!! UNABLE TO ADD A NEW VOTE !!!")
            print(e)
            print("!!! UNABLE TO ADD A NEW VOTE !!!")
            return False
    
    # def create_vote_by_names(self, voter_id, office_name, candidate_name):
    #     try:

    #         self.open_connection()

    #         sql_find_office = """
    #         SELECT id FROM offices WHERE office_name='{}'
    #         """.format(office_name)
    #         self.curr.execute(sql_find_office)
    #         single_office = self.curr.fetchone()
    #         if single_office == None:
    #             return "Office with name {} could not be found".format(office_name)
    #         office_id = single_office[0]


    #         self.close_connection()

    #     except Exception as e:
    #         print("!!! UNABLE TO CREATE A NEW VOTE BY NAME !!!")
    #         print(e)
    #         print("!!! UNABLE TO CREATE A NEW VOTE BY NAME !!!")
    