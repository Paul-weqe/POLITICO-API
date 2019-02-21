import psycopg2
import os 
# from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection


class PartyConnection:
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