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
    
        
users = [
    {
        "id": 1, "first_name": "Paul", "last_name": "Wekesa", "other_name": "Waswa", 
        "email": "paul1tw1@gmail.com", "phone_number": "0712345", "passport_url": "http://paul-url", "is_admin": False
    },
    {
        "id": 2, "first_name": "Gideon", "last_name": "Koima", "other_name": "Kari", "email": "gidi@gidi.com",
        "phone_number": "071273734", "passport_url": "http://gidi-url", "is_admin": False
    },
    {
        "id": 3, "first_name": "Brenda", "last_name": "Sagide", "other_name": "Njeri", "email": "brenda@brenda.com",
        "phone_number": "07127374", "passport_url": "http://brenda-url", "is_admin": True
    },
    {
        "id": 4, "first_name": "Byron", "last_name": "Kibet", "other_name": "Chep", "email": "byron@byron.com", 
        "phone_number": "077273723", "passport_url": "http://byron-url", "is_admin": True
    }
]