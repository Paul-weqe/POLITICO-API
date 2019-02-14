import psycopg2
import os

class UserConnection:

    def __init__(self):
        self.conn = None 
        self.curr = None 

    def open_connection(self):
        try:
            self.conn = psycopg2.connect(
                user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host="localhost", database=os.getenv("DATABASE_NAME")
            )
            self.curr = self.conn.cursor()
            print("connection established")

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
    
    
    def insert_user(self, **user_details_kwargs):
        try:

            self.open_connection()
            first_name = user_details_kwargs["first_name"]
            last_name = user_details_kwargs["last_name"]
            other_name = user_details_kwargs["other_name"]
            email = user_details_kwargs["email"]
            phone_number = user_details_kwargs["phone_number"]
            passport_url = user_details_kwargs["passport_url"]
            is_politician = 'false'
            is_admin = 'false'

            if "is_politician" in user_details_kwargs:
                is_politician = 'true' if user_details_kwargs["is_politician"] else 'false'
            

            if "is_admin" in user_details_kwargs:
                is_admin = 'true' if user_details_kwargs["is_admin"] else 'false'
            
            sql_command = """
            INSERT INTO users
            (first_name, last_name, other_name, email, phone_number, passport_url, is_politician, is_admin)
            VALUES 
            ('{}', '{}', '{}', '{}', '{}', '{}', {}, {})
            """.format(
                first_name, last_name, other_name, email, phone_number, passport_url, is_politician, is_admin
            )
            self.curr.execute(sql_command)
            self.conn.commit()
            print("user {} {} created".format(first_name, last_name))

            self.close_connection()

            return [{"first_name": first_name, "last_name": last_name}]

        except Exception as e:
            print("!!! UNABLE TO CREATE NEW USER !!!")
            print(e)
            print("!!! UNABLE TO CREATE NEW USER !!!")
            return False
