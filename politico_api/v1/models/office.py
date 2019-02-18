offices = {
    
}

class OfficeModel:

    def __init__(self, office_data=None):
        if office_data != None:
            self.type = office_data["office_type"]
            self.name = office_data["office_name"]
        
    def create_office(self):
        for office in offices:
            if offices[office]["name"] == self.name:
                return False

        dict_info = {"type": self.type, "name": self.name}
        #dict_info["id"]
        id = len(offices) + 1
        dict_info["id"] = id
        offices[id] = dict_info
        return True
    
    def get_all_offices(self):
        all_offices = []
        for office in offices:
            all_offices.append(offices[office])
        return all_offices

    
    def get_single_office(self, office_id):
        print(offices)
        if office_id in offices:
            return offices[office_id]
        return None 
