import psycopg2
import os 
# from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection


class CandidateConnection:
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
    
    def create_candidate(self, user_id, party_id, office_id):
        try:
            self.open_connection()

            check_if_user_exists_command = """
            SELECT * FROM users WHERE id={}
            """.format(user_id)

            check_if_party_exists_command = """
            SELECT * FROM parties WHERE id={}
            """.format(party_id)

            check_if_office_exists_command = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)

            self.curr.execute(check_if_user_exists_command)
            user_found = self.curr.fetchone()

            self.curr.execute(check_if_party_exists_command)
            party_found = self.curr.fetchone()

            self.curr.execute(check_if_office_exists_command)
            office_found = self.curr.fetchone()

            if user_found == None:
                return "The user does not exist"
            
            elif party_found == None:
                return "The party does not exist in our system"
            
            elif office_found == None:
                return "The office does not exist in our system"

            sql_command = """
            INSERT INTO candidates(user_id, party_id, office_id) VALUES 
            ({}, {}, {})
            """.format(user_id, party_id, office_id)

            self.curr.execute(sql_command)
            self.conn.commit()

            self.close_connection()
            return "Candidate successfully created"

        except Exception as e:
            # if type(e) == psycopg2.IntegrityError:
            #     return "The user has already been registered as a candidate"
            print("!!! UNABLE TO CREATE A CANDIDATE !!!")
            print(e)
            print("!!! UNABLE TO CREATE A CANDIDATE !!!")
    
    def create_candidate_by_names(self, user_name, party_name, office_id):
        try:
            self.open_connection()
            ## FIND THE USER ID
            sql_find_user = """
            SELECT id FROM users WHERE username='{}'
            """.format(user_name)
            self.curr.execute(sql_find_user)
            user_found = self.curr.fetchone()
            if user_found is None:
                return "User with name {} not found".format(user_name)
            user_id = user_found[0]

            ## FIND THE PARTY ID
            sql_find_party = """
            SELECT id FROM parties WHERE party_name='{}'
            """.format(party_name)
            self.curr.execute(sql_find_party)
            party_found = self.curr.fetchone()
            if party_found is None:
                return "Party with name {} not found".format(party_name)
            party_id = party_found[0]

            ## FIND THE OFFICE ID
            sql_find_office = """
            SELECT id from offices WHERE id={}
            """.format(office_id)
            self.curr.execute(sql_find_office)
            office_found = self.curr.fetchone()
            if office_found is None:
                return "Office with id {} not found".format(office_id)
            office_id = office_found[0]
            
            ## ADD THE CANDIDATE
            sql_command = """
            INSERT INTO candidates(user_id, office_id, party_id) VALUES ({}, {}, {})
            """.format(user_id, office_id, party_id)
            self.curr.execute(sql_command)
            self.conn.commit()
            self.close_connection()

            return True
            
        except Exception as e:
            if type(e) == psycopg2.IntegrityError:
                print(e)
                return "Candidate already exists"
            print("!!! UNABLE TO CREATE A CANDIDATE USING NAME !!!")
            print(e)
            print("!!! UNABLE TO CREATE A CANDIDATE USING NAME !!!")
            return False
            
