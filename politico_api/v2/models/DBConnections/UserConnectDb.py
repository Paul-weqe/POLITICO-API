import hashlib
from lib2to3.pytree import Base
import logging
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConn

class UserConnection:
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def insert_user(self, **user_details_kwargs):

        with BaseConn(kwargs=self.kwargs) as base_conn:

            first_name = user_details_kwargs["first_name"]
            last_name = user_details_kwargs["last_name"]
            other_name = user_details_kwargs["other_name"]
            email = user_details_kwargs["email"]
            phone_number = user_details_kwargs["phone_number"]
            passport_url = user_details_kwargs["passport_url"]
            password = user_details_kwargs["password"]
            username = user_details_kwargs["username"]
            
            ## confirm if user with unique credentials already exists
            sql_command_if_exists = """
            SELECT * FROM users WHERE email='{}'
            """.format(email)
            
            base_conn.curr.execute(sql_command_if_exists)
            user_exists = base_conn.curr.fetchall()

            if len(user_exists) > 0: return None 

            sql_command = """
            INSERT INTO users
            (first_name, last_name, other_name, email, phone_number, passport_url, username, password)
            VALUES 
            ('{}', '{}', '{}', '{}', '{}', '{}', '{}', md5('{}'))
            """.format(first_name, last_name, other_name, email, phone_number, passport_url, username, password)
            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()
            logging.info("user {} {} created".format(first_name, last_name))

            return "user successfully created"


    def change_user_password(self, email, old_password, new_password):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            # confirm if the user is actually in the system
            sql_command = """
            SELECT * FROM users WHERE email='{}'
            """.format(email)
            base_conn.curr.execute(sql_command)
            
            # if email not in the system, the method returns None
            single_user = base_conn.curr.fetchone() 
            if single_user == None: return None 
            
            # if the old passwords do not match with the one entered
            print(single_user[5])
            if single_user[5] != hashlib.md5(old_password.encode()).hexdigest():
                return "the old password you entered is not correct"
            
            # if everything is fine so far
            sql_command = """
            UPDATE users SET password=md5('{}') WHERE email='{}'
            """.format(new_password, email)

            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()
            
            return True

    def find_by_email_password(self, email, password):
        with BaseConn(kwargs=self.kwargs) as base_conn:

            sql_command = """
            select * from users where email='{}' and password=md5('{}')
            """.format(email, password)
            base_conn.curr.execute(sql_command)
            user_info = base_conn.curr.fetchone()
            return user_info
        
    
    def make_user_admin(self, user_id):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            find_user_sql_command = """
            SELECT * FROM users WHERE id={}
            """.format(user_id)

            base_conn.curr.execute(find_user_sql_command)
            if base_conn.curr.fetchone() == None:
                return None
            
            sql_command = """
            UPDATE users SET is_admin=true WHERE id={}
            """.format(user_id)
            
            base_conn.curr.execute(sql_command)
            base_conn.conn.commit()

            return True

    def find_user_by_id(self, user_id):
        with BaseConn(kwargs=self.kwargs) as base_conn:
            sql_command = """
            SELECT exists(select 1 from users where id={})
            """.format(user_id)
            
            base_conn.curr.execute(sql_command)
            user_info = base_conn.curr.fetchone()

            return user_info
            

    
    