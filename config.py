from dotenv import load_dotenv
import os 

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config(object):
    "GENERAL CONFIGS"
    DEBUG=True
    NAME='paul'

class TestConfig(object):
    DEBUG = True
    TEST_DATABASE_NAME = os.getenv("TEST_DATABASE_NAME")
    TEST_DATABASE_PASSWORD = os.getenv("TEST_DATABASE_PASSWORD")
    TEST_DATABASE_HOST = os.getenv("TEST_DATABASE_HOST")
    TEST_DATABASE_USER = os.getenv("TEST_DATABASE_USER")
    SECRET_KEY = os.getenv("TEST_SECRET_KEY")

class ProductionConfig(object):
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_USER = os.getenv("DATABASE_USER")
    SECRET_KEY = os.getenv("SECRET_KEY")

class WrongTestConfig(TestConfig):
    TEST_DATABASE_NAME = os.getenv('WRONG_TEST_DATABASE_NAME')

