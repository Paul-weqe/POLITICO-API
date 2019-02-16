from politico_api.v2.models.DBConnections.UserConnectDb import UserConnection

class User:

    
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def create_user(self):
        new_user = UserConnection()
        user_created = new_user.insert_user(**self.kwargs)
        return user_created
    
    def change_password(self, email, old_password, new_password):
        user = UserConnection()
        return  user.change_user_password(email, old_password, new_password)
        
    def get_user_by_email_and_password(self, email, password):
        user = UserConnection()
        return user.find_user_by_email_and_password(email, password)
