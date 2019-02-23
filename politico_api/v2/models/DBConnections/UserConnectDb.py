import psycopg2
import hashlib
import os
from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection

class UserConnection(BaseConnection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def insert_user(self, **user_details_kwargs):
        try:

            self.open_connection()

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
            
            self.curr.execute(sql_command_if_exists)
            user_exists = self.curr.fetchall()

            if len(user_exists) > 0: return None 

            sql_command = """
            INSERT INTO users
            (first_name, last_name, other_name, email, phone_number, passport_url, username, password)
            VALUES 
            ('{}', '{}', '{}', '{}', '{}', '{}', '{}', md5('{}'))
            """.format(
                first_name, last_name, other_name, email, phone_number, passport_url, username, password
            )
            self.curr.execute(sql_command)
            self.conn.commit()
            print("user {} {} created".format(first_name, last_name))

            self.close_connection()

            return "user successfully created"

        except Exception as e:
            print("!!! UNABLE TO CREATE NEW USER !!!")
            print(e)
            print("!!! UNABLE TO CREATE NEW USER !!!")
            return False

    def change_user_password(self, email, old_password, new_password):

        try:
            self.open_connection()
            
            # confirm if the user is actually in the system

            sql_command = """
            SELECT * FROM users WHERE email='{}'
            """.format(email)
            self.curr.execute(sql_command)
            
            # if email not in the system, the method returns None
            single_user = self.curr.fetchone() 
            if single_user == None: return None 
            
            # if the old passwords do not match with the one entered
            print(single_user[5])
            if single_user[5] != hashlib.md5(old_password.encode()).hexdigest():
                return "the old password you entered is not correct"
            
            # if everything is fine so far
            sql_command = """
            UPDATE users SET password=md5('{}') WHERE email='{}'
            """.format(new_password, email)

            self.curr.execute(sql_command)
            self.conn.commit()
            
            self.close_connection()
            return True
        
        except Exception as e:
            print("!!! ERROR CHANGING USER PASSWORD !!!")
            print(e)
            print("!!! ERROR CHANGING USER PASSWORD !!!")
            return False

    def find_by_email_password(self, email, password):
        try:
            self.open_connection()

            sql_command = """
            select * from users where email='{}' and password=md5('{}')
            """.format(email, password)
            self.curr.execute(sql_command)
            
            user_info = self.curr.fetchone()

            self.close_connection()
            return user_info

        except Exception as e:
            print("!!! ERROR FINDING USER !!!")
            print(e)
            print("!!! ERROR FINDING USER !!!")
            return False 
    
    def make_user_admin(self, user_id):
        try:
            
            self.open_connection()

            find_user_sql_command = """
            SELECT * FROM users WHERE id={}
            """.format(user_id)

            self.curr.execute(find_user_sql_command)
            if self.curr.fetchone() == None:
                return None
            
            sql_command = """
            UPDATE users SET is_admin=true WHERE id={}
            """.format(user_id)
            
            self.curr.execute(sql_command)
            self.conn.commit()
            
            self.close_connection()
            return True

        except Exception as e:
            print("!!! ERROR MAKING USER ADMIN !!!")
            print(e)
            print("!!! ERROR MAKING USER ADMIN !!!")
            
        return True

    def find_user_by_id(self, user_id):
        try:
            self.open_connection()
            
            sql_command = """
            SELECT exists(select 1 from users where id={})
            """.format(user_id)
            
            self.curr.execute(sql_command)
            user_info = self.curr.fetchone()

            self.close_connection()
            return user_info
            
        except Exception as e:
            print("!!! UNABLE TO FIND USER BY ID !!!")
            print(e)
            print("!!! UNABLE TO FIND USER BY ID !!!")
