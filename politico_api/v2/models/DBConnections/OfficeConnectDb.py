from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConn

class OfficeConnection:
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    # creates a new office with the valid parameters
    def create_office(self, office_name, office_type):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            # this SQL query looks if the parameters aimed to be used to create this party already exist
            sql_if_office_exists_command = """
            SELECT * FROM offices WHERE office_name='{}' and office_type='{}'
            """.format(office_name, office_type)
            
            base_conn.curr.execute(sql_if_office_exists_command)
            office_exists = base_conn.curr.fetchall()

            if len(office_exists) > 0:
                return None
            
            # if the office does not already exist, it is then created
            # this way:
            sql_command = """
            INSERT INTO offices(office_name, office_type) VALUES ('{}', '{}')
            """.format(office_name, office_type)

            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()

            return True
    
    def get_all_offices(self):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            sql_command = "SELECT * FROM offices"
            base_conn.curr.execute(sql_command)
            all_offices = base_conn.curr.fetchall()
            return all_offices
    

    def get_office_by_id(self, office_id):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            sql_command = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)
            base_conn.curr.execute(sql_command)
            office = base_conn.curr.fetchone()
            return office

    def get_office_by_name(self, office_name):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            sql_command = """
            SELECT * FROM offices WHERE office_name='{}'
            """.format(office_name)
            base_conn.curr.execute(sql_command)
            office = base_conn.curr.fetchone()
            return office
    
    def get_office_results(self, office_id):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            find_office_sql = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)
            base_conn.curr.execute(find_office_sql)
            find_offices = base_conn.curr.fetchall()
            if len(find_offices) < 1:
                return None 
            
            count_votes_sql = """
            select users.username, count(candidate_id) as number_of_votes from votes INNER JOIN users ON users.id=votes.candidate_id WHERE votes.office_id={} GROUP BY users.username
            """.format(office_id)
            base_conn.curr.execute(count_votes_sql)
            votes_count = base_conn.curr.fetchall()

            self.close_connection()
            return votes_count
    
