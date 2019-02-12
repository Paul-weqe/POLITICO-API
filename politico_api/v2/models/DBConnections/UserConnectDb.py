import psycopg2

class UserConnection:
    
    def __init__(self):
        self.conn = None 
        self.curr = None 
    
    # opens a connection between the database and the python code
    # will be called everytime before we do any database related function
    def create_connection(self):

        try:
            self.conn = psycopg2.connect(
                database='politico_test', user='weqe', password='4ndel4', host='localhost', port="5432"
                )
            self.curr = self.conn.cursor()
            return True
        
        except Exception as e:
            print("!!!ERROR CREATING DATABASE!!!")
            print(e)
            return False
    
    # closes a database connection between the politico database and the python code
    # will be called everytime when a specific database related function is done
    def close_connection(self):
        
        if self.curr != None:
            self.curr.close()
        if self.conn != None:
            self.conn.close()
        
    def check_if_email_exists(self, email):
        try:
            self.create_connection()

            sql_command = "SELECT * FROM users where email='{}'".format(email)
            self.curr.execute(sql_command)

            user_exists = self.curr.fetchall()
            if len(user_exists) > 0:
                return True
            return False

        except Exception as e:
            print("!!! ERROR FINDING USER USING EMAIL !!!")
            print(e)
            print("!!! ERROR FINDING USER USING EMAIL !!!")
            return False
    
    # creates a new user with the valid cridentials
    def create_new_user(self, username, email, password):
        try:
            self.create_connection()
            if self.check_if_email_exists(email):
                return "email exists"

            sql_command = "INSERT INTO users(username, email, password) VALUES ('{}', '{}', '{}')".format(
                username, email, password
            )
            self.curr.execute(sql_command)
            self.conn.commit()
            self.close_connection()
            return True

        except Exception as e:
            print("!!! ERROR CREATING NEW USER !!!")
            print(e)
            print("!!! ERROR CREATING NEW USER !!!")
            return False

    
    def restructure_tables(self):
        try:
            self.create_connection()

            drop_tables_commands = ["DROP TABLE users",]
            for command in drop_tables_commands:
                self.curr.execute(command)
            
            create_tables_commands = ["""
            CREATE TABLE users (id serial primary key, username varchar(20), email varchar(30), password varchar(100))
            """]
            for command in create_tables_commands:
                self.curr.execute(command)
            
            self.conn.commit()
            self.close_connection()
            
            return True
        
        except Exception as e:
            print("!!! ERRROR RESTRUCTURING TABLES !!!")
            print(e)
            print("!!! ERRROR RESTRUCTURING TABLES !!!")
            return False

    # authenticates a specific user based on their email and password
    # def authenticate_user(self, email, password):
