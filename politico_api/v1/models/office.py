import sys
sys.path.insert(0,'../../..')

offices = {
    
}

class OfficeModel:

    def __init__(self, office_data):
        self.type = office_data["office_type"]
        self.name = office_data["office_name"]
        
    def create_office(self):
        dict_info = {"type": self.type, "name": self.name}
        dict_info["id"] = len(offices) + 1
        offices[id] = dict_info
        return True


    @staticmethod
    def get_all_offices():
        all_offices = []
        for office in offices:
            all_offices.append(offices[office])
        return all_offices

    @staticmethod
    def get_single_office(office_id):
        if office_id in offices:
            return offices[office_id]
        return None 
