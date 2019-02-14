offices = {
    
}

class OfficeModel:

    def __init__(self, office_data=None):
        if office_data != None:
            self.type = office_data["office_type"]
            self.name = office_data["office_name"]
        
    def create_office(self):
        dict_info = {"type": self.type, "name": self.name}
        dict_info["id"] = len(offices) + 1
        offices[id] = dict_info
        return True
    
    def get_all_offices(self):
        all_offices = []
        for office in offices:
            all_offices.append(offices[office])
        return all_offices

    
    def get_single_office(self, office_id):
        if office_id in offices:
            return offices[office_id]
        return None 
