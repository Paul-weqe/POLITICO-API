import psycopg2
import os 
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection


class OfficeConnection(BaseConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    # this returns the result of the office with ID officeID
    def get_office_results(self, office_id):
        try:
            self.open_connection()
            sql_find_office_command = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)

            self.curr.execute(sql_find_office_command)
            office = self.curr.fetchone()
            if office == None:
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

            # t his SQL query looks if the parameters aimed to be used to create this party already exist
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
    
    def get_all_offices(self):
        try:
            self.open_connection()

            sql_command = "SELECT * FROM offices"

            self.curr.execute(sql_command)
            all_offices = self.curr.fetchall()

            self.close_connection()
            return all_offices

        except Exception as e:
            print("!!! UNABLE TO GET ALL OFFICES !!!")
            print(e)
            print("!!! UNABLE TO GET ALL OFFICES !!!")
            return False
    

    def get_office_by_id(self, office_id):

        try:
            self.open_connection()

            sql_command = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)
            self.curr.execute(sql_command)
            office = self.curr.fetchone()

            self.close_connection()
            return office

        except Exception as e:
            print("!!! UNABLE TO GET A SINGLE OFFICE!!!")
            print(e)
            print("!!! UNABLE TO GET A SINGLE OFFICE!!!")

    def get_office_by_name(self, office_name):
        try:
            self.open_connection()
            
            sql_command = """
            SELECT * FROM offices WHERE office_name='{}'
            """.format(office_name)
            self.curr.execute(sql_command)
            office = self.curr.fetchone()

            self.close_connection()
            return office

        except Exception as e:
            print("!!! UNABLE TO GET A SINGLE OFFICE BY ID !!!")
            print(e)
            print("!!! UNABLE TO GET A SINGLE OFFICE BY ID !!!")
    
    