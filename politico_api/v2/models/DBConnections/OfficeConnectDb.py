import psycopg2
import os 
# from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection


class OfficeConnection:
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
    

    # this returns the result of the office with ID officeID
    def get_office_results(self, office_id):
        try:
            self.open_connection()
            sql_find_office_command = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)

            self.curr.execute(sql_find_office_command)
            office = self.curr.fetchall()
            if len(office) == 0:
                return None

            sql_command = """
            SELECT users.id, users.first_name, count(votes.voted_for) as number_of_votes from users LEFT JOIN votes 
            ON (votes.voted_for=users.id) WHERE (users.is_politician=true) AND (users.office_interested={}) group by users.id
            """.format(office_id)

            self.curr.execute(sql_command)
            votes_results = self.curr.fetchall()
            self.close_connection()

            return votes_results

        except Exception as e:
            print("!!! UNABLE TO FIND OFFICE RESULTS !!!")
            print(e)
            print("!!! UNABLE TO FIND OFFICE RESULTS !!!")
            return False 
    
    # creates a new office with the valid parameters
    def create_office(self, office_name, office_type):
        try:
            self.open_connection()

            # this SQL query looks if the parameters aimed to be used to create this party already exist
            sql_if_office_exists_command = """
            SELECT * FROM offices WHERE office_name='{}' and office_type='{}'
            """.format(office_name, office_type)
            
            self.curr.execute(sql_if_office_exists_command)
            office_exists = self.curr.fetchall()

            if len(office_exists) > 0:
                return None
            
            # if the office does not already exist, it is then created
            # this way:
            sql_command = """
            INSERT INTO offices(office_name, office_type) VALUES ('{}', '{}')
            """.format(office_name, office_type)

            self.curr.execute(sql_command)
            self.conn.commit()
            self.close_connection()

            return True
        except Exception as e:
            print("!!! UNABLE TO CREATE NEW OFFICE !!!")
            print(e)
            print("!!! UNABLE TO CREATE NEW OFFICE !!!")
            return False
