from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConn

class CandidateConnection:

    def __init__(self, **kwargs):
        self.kwargs_1 = kwargs

    def create_candidate(self, user_id, party_id, office_id):
        """
        Creates a new candidate in the system
        the user_id is used to reference the candidate to a specific user. 
        """

        with BaseConn(kwargs = self.kwargs_1) as base_conn:
            # the following are checks to see if the users, party and offices refered to actually exist
            check_if_user_exists_command = """
            SELECT * FROM users WHERE id={}
            """.format(user_id)

            check_if_party_exists_command = """
            SELECT * FROM parties WHERE id={}
            """.format(party_id)

            check_if_office_exists_command = """
            SELECT * FROM offices WHERE id={}
            """.format(office_id)

            base_conn.curr.execute(check_if_user_exists_command)
            user_found = self.curr.fetchone()

            base_conn.curr.execute(check_if_party_exists_command)
            party_found = self.curr.fetchone()

            base_conn.curr.execute(check_if_office_exists_command)
            office_found = self.curr.fetchone()

            if user_found == None:
                return "The user does not exist"
            
            elif party_found == None:
                return "The party does not exist in our system"
            
            elif office_found == None:
                return "The office does not exist in our system"
            
            # add the candidate to the candidates' list
            sql_command = """
            INSERT INTO candidates(user_id, party_id, office_id) VALUES 
            ({}, {}, {})
            """.format(user_id, party_id, office_id)

            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()

            base_conn.close_connection()
            return "Candidate successfully created"

        # except Exception as e:
        #     print("!!! UNABLE TO CREATE A CANDIDATE !!!")
        #     print(e)
        #     print("!!! UNABLE TO CREATE A CANDIDATE !!!")
    
    def create_candidate_by_names(self, user_name, party_name, office_id):
        with BaseConn(kwargs = self.kwargs_1) as base_conn:
            ## FIND IF THE USER ID EXISTS
            sql_find_user = """
            SELECT id FROM users WHERE username='{}'
            """.format(user_name)
            base_conn.curr.execute(sql_find_user)
            user_found = base_conn.curr.fetchone()
            if user_found is None:
                return "User with name {} not found".format(user_name)
            user_id = user_found[0]

            ## FIND IF THE PARTY ID EXISTS
            sql_find_party = """
            SELECT id FROM parties WHERE party_name='{}'
            """.format(party_name)
            base_conn.curr.execute(sql_find_party)
            party_found = base_conn.curr.fetchone()
            if party_found is None:
                return "Party with name {} not found".format(party_name)
            party_id = party_found[0]

            ## FIND IF THE OFFICE ID EXISTS
            sql_find_office = """
            SELECT id from offices WHERE id={}
            """.format(office_id)
            base_conn.curr.execute(sql_find_office)
            office_found = base_conn.curr.fetchone()
            if office_found is None:
                return "Office with id {} not found".format(office_id)
            office_id = office_found[0]

            ## look for if the user has already registered for that specific office
            sql_has_registered = """
            SELECT * FROM candidates WHERE user_id={} and office_id={}
            """.format(user_id, office_id)
            base_conn.curr.execute(sql_has_registered)
            user_already_registered = base_conn.curr.fetchone()
            if user_already_registered != None:
                return "User has already registered for that office"

            ## ADD THE CANDIDATE
            sql_command = """
            INSERT INTO candidates(user_id, office_id, party_id) VALUES ({}, {}, {})
            """.format(user_id, office_id, party_id)
            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()

            return True
    