import os 


class Config(object):
    "GENERAL CONFIGS"
    DEBUG=True

class TestConfig(object):
    DEBUG = True
    DATABASE_NAME = os.getenv("TEST_DATABASE_NAME")
    DATABASE_PASSWORD = os.getenv("TEST_DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("TEST_DATABASE_HOST")
    DATABASE_USER = os.getenv("TEST_DATABASE_USER")

class ProductionConfig(object):
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_USER = os.getenv("DATABASE_USER")


