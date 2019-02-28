import psycopg2
import os 
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection

class OfficeConnection(BaseConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    
    def get_office_results(self, office_id):
        try:
            self.open_connection()

            find_office_sql = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)
            self.curr.execute(find_office_sql)
            find_offices = self.curr.fetchall()
            if len(find_offices) < 1:
                return None 
            
            count_votes_sql = """
            select users.username, count(candidate_id) as number_of_votes from votes INNER JOIN users ON users.id=votes.candidate_id WHERE votes.office_id={} GROUP BY users.username
            """.format(office_id)
            self.curr.execute(count_votes_sql)
            votes_count = self.curr.fetchall()

            self.close_connection()
            return votes_count
            
        except Exception as e:
            print("!!! UNABLE TO GET OFFICE RESULTS !!!")
            print(e)
            print("!!! UNABLE TO GET OFFICE RESULTS !!!")
    
