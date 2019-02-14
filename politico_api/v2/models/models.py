from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection


class User:

    @staticmethod
    def create_user(**user_info):
        new_user = UserConnection()
        user_created = new_user.insert_user(**user_info)
        return user_created
    


