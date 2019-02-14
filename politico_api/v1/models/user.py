users = {
    
}

class UserModel:

    def __init__(self, user_data=None):
        if user_data != None:
            self.user_data = user_data
    
    def create_user(self):
        for user in users:
            if users[user]["email"] == self.user_data["email"]:
                return "the email is already in use"

        if self.user_data != None:
            id = len(users) + 1
            self.user_data["id"] = id
            users[id] = self.user_data
            return [{"username": self.user_data["username"], "email": self.user_data["email"]}]
        return None 
        
    
    # returns a list with all the users and all their details
    def get_all_users(self):
        user_list = []
        for user in users:
            user_list.append(users[user])

        return user_list
    
    def get_single_user(self, user_id):
        if user_id in users:
            return users[user_id]
        return None
    
    def get_user_by_email_and_password(self, email, password):
        print(users)
        for user in users:
            if users[user]["email"] == email and users[user]["password"] == password:
                user_info = users[user]
                del user_info["id"]
                return user_info
        
        return None 
    
    def delete_user(self, user_id):
        if user_id in users:
            del users[user_id]
            return "Successfully deleted"
        return None
    