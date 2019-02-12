import sys
sys.path.insert(0, '../../..')

from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection

class UserModel:

    @staticmethod
    def create_user(username, email, password):
        user = UserConnection()
        return user.create_new_user(username, email, password)

    @staticmethod
    def restructure_database():
        user = UserConnection()
        return user.restructure_tables()
    
    @staticmethod
    def find_user_by_email_and_password(email, password):
        user = UserConnection()
        return user.find_user_by_email_and_password(email, password)
