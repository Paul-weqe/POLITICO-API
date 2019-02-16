import psycopg2
import os

class UserConnection:

    def __init__(self, **kwargs):
        self.conn = None 
        self.curr = None 
        self.kwargs = None
        if len(kwargs) != 0:
            self.kwargs = kwargs

    def open_connection(self):
        try:
            if self.kwargs==None:
                self.conn = psycopg2.connect(
                    user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host="localhost", database=os.getenv("DATABASE_NAME")
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
            is_politician = 'false'
            is_admin = 'false'

            if "is_politician" in user_details_kwargs:
                is_politician = 'true' if user_details_kwargs["is_politician"] else 'false'
            

            if "is_admin" in user_details_kwargs:
                is_admin = 'true' if user_details_kwargs["is_admin"] else 'false'
            
            sql_command = """
            INSERT INTO users
            (first_name, last_name, other_name, email, phone_number, passport_url, is_politician, is_admin, password)
            VALUES 
            ('{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}')
            """.format(
                first_name, last_name, other_name, email, phone_number, passport_url, is_politician, is_admin, password
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
            if single_user[5] != old_password:
                return "the old password you entered is not correct"
            
            # if everything is fine so far
            sql_command = """
            UPDATE users SET password='{}' WHERE email='{}'
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

        
    def find_user_by_email_and_password(self, email, password):
        try:
            self.open_connection()

            sql_command = """
            SELECT * FROM users WHERE email='{}' and password='{}'
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
    
    def find_user_by_id(self, user_id):
        try:
            self.open_connection()

            sql_command = """
            SELECT * FROM users WHERE id={}
            """.format(user_id)
            
            self.curr.execute(sql_command)
            user_info = self.curr.fetchone()

            self.close_connection()
            return user_info
            
        except Exception as e:
            print("!!! UNABLE TO FIND USER BY ID !!!")
            print(e)
            print("!!! UNABLE TO FIND USER BY ID !!!")

    ## WARNING: TO BE USED FOR TESTING DATABASE ONLY ##
    def reset_database(self, schema_file=None):
        try:
            self.open_connection()
            if schema_file == None:
                self.curr.execute(open("schema.txt", "r").read())
            else:
                self.curr.execute(open(schema_file, "r").read())
            self.conn.commit()
            self.close_connection()
            return True
        except Exception as e:
            print("!!! ERROR RESETTING DATABASE USER PASSWORD !!!")
            print(e)
            print("!!! ERROR RESETING DATABASE !!!")
            return False

u = UserConnection()
u.insert_user(**{"username": "weqe", "email": "weqe@weqe.com", "password": "popopo"})
