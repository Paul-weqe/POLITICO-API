import os 


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

class ProductionConfig(object):
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_USER = os.getenv("DATABASE_USER")


