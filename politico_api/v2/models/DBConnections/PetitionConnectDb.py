import psycopg2
import os

class PetitionConnection:
    """
    This class is used to connect a cursor to the politico database
    This will contain methods that carry out SQL queries and commands on the database specifically for the petitions table
    """

    def __init__(self, **kwargs):
        self.conn = None 
        self.curr = None 
        self.kwargs = None
        if len(kwargs) != 0:
            self.kwargs = kwargs

    def open_connection(self):
        # this function should be carried out before every function to carry out SQL queries begins
        try:
            if self.kwargs==None:
                self.conn = psycopg2.connect(
                    user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host="localhost", database=os.getenv("DATABASE_NAME")
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
        # this function should be carried out after evey function that is carrying out SQL queries

        try:
            if (self.conn):
                self.curr.close()
    
        except Exception as e:
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
            print(e)
            print("!!! UNABLE TO CONNECT TO THE DATABASE !!!")
    
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



