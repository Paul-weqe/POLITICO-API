from random import randint
import sys 
sys.path.insert(0, '../../..')

from politico_api.v1.models.model_functions import GeneralModelMethods

users = [

]

class UserModel:

    def __init__(self, user_data):
        self.user_data = user_data
    
    def create_user(self):
        try:
            GeneralModelMethods.create_item(users, self.user_data)
            return self.user_data
        except Exception:
            return False
    
    # returns a list with all the users and all their details
    @staticmethod
    def get_all_users():
        return users 
    

    @staticmethod
    def get_single_user(user_id):
        return GeneralModelMethods.get_single_item(users, user_id)
    
    @staticmethod
    def delete_user(user_id):
        return GeneralModelMethods.delete_item(users, user_id)
    
 