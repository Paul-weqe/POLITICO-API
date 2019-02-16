import psycopg2
import os 
# from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection
from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection


class VoteConnection:

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
    
    def create_vote(self, voter_id, office_id, candidate_id):
        try:
            self.open_connection()

            # checks if the user has already voted for that office
            sql_check_if_voted_command = """
            select * from users inner join votes on votes.created_by=users.id WHERE users.id={} and votes.office={}
            """.format(voter_id, office_id)
            self.curr.execute(sql_check_if_voted_command)
            results = self.curr.fetchall()

            if len(results) != 0:
                return "already voted"
            
            # validate if the user exists
            u = UserConnection()
            
            ## TODO - ADD VALIDATION FOR THE office_id
            
            if u.find_user_by_id(voter_id) == None:
                return None
            elif u.find_user_by_id(candidate_id) == None:
                return None 

            sql_command = """
            INSERT INTO votes(created_by, office, voted_for) VALUES (
                {}, {}, {}
            )
            """.format(voter_id, office_id, candidate_id)

            self.curr.execute(sql_command)
            self.conn.commit()
            self.close_connection()

            return True
            

        except Exception as e:
            print("!!! UNABLE TO ADD A NEW VOTE !!!")
            print(e)
            print("!!! UNABLE TO ADD A NEW VOTE !!!")
            return False

