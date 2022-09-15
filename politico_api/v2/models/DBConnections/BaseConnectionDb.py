from dataclasses import dataclass
import psycopg2
import os 
import logging

@dataclass
class DbConn:
    conn: object
    curr: object

class BaseConn(object):

    def __init__(self, **kwargs):
        self.db_conn = DbConn(conn=None, curr=None)
        self.kwargs = None
        if len(kwargs['kwargs']) > 0:
            self.kwargs = kwargs['kwargs']
        

    def __enter__(self):

        if self.kwargs == None:
            conn = psycopg2.connect(
                user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host=os.getenv("DATABASE_HOST"), database=os.getenv("DATABASE_NAME")
            )
            curr = conn.cursor()
            self.db_conn = DbConn(conn=conn, curr=curr)
            logging.info("database connection established")
        
        else:
            conn = psycopg2.connect(
                user=self.kwargs["DB_USER"], password=self.kwargs["DB_PASSWORD"], host="localhost", database=self.kwargs["DB_NAME"]
            )
            curr = conn.cursor()
            self.db_conn = DbConn(conn=conn, curr=curr)
            logging.info("Connection  established test")
        
        return self.db_conn

    def __exit__(self, type, value, traceback):
        if (self.db_conn):
            self.db_conn.curr.close()

        logging.error(traceback)


class BaseConnection:
    """
    this class creates a connection to the politico database
    SQL queries can be carried through methods in this class.
    open_connection() and close_connection() will be called at the beginning of every function that performs an SQL query
    """
    def __init__(self, **kwargs):
        self.conn = None 
        self.curr = None 
        self.kwargs = None
        if len(kwargs) > 0:
            self.kwargs = kwargs
        

    def open_connection(self):
        "Opens the cursor to the database that will be used for the rest of the application"
        try:
            # looks for the presence of keyword arguments that may store extra information about the database you may want to use
            # by default it gets the values from os.getenv('') DATABASE SETTINGS
            if self.kwargs==None:
                self.conn = psycopg2.connect(
                    user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host=os.getenv("DATABASE_HOST"), database=os.getenv("DATABASE_NAME")
                )
                self.curr = self.conn.cursor()
                logging.info("connection established")
            else:
                self.conn = psycopg2.connect(
                    user=self.kwargs["DB_USER"], password=self.kwargs["DB_PASSWORD"], host="localhost", database=self.kwargs["DB_NAME"]
                )
                self.curr = self.conn.cursor()
                logging.info("Connection  established test")
        

        except Exception as e:
            logging.error(e)
            logging.error("UNABLE TO CONNECT TO THE DATABASE")
            
    def close_connection(self):
        "Closes the cursor that was being used to connect to the database"
        try:
            if (self.conn):
                self.curr.close()

        except Exception as e:
            logging.error(e)
            logging.error("UNABLE TO CONNECT TO THE DATABASE")

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
