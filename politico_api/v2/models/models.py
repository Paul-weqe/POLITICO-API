from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection

class User:

    
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args

    def create_user(self):
        new_user = UserConnection()
        user_created = new_user.insert_user(**self.kwargs)
        return user_created
    
    def change_password(self, email, old_password, new_password):
        user = UserConnection()
        return  user.change_user_password(email, old_password, new_password)
        
    