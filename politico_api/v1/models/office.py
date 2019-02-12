from random import randint
import sys
sys.path.insert(0,'../../..')

from politico_api.v1.models.model_functions import GeneralModelMethods

offices = {
    
}

class OfficeModel:

    def __init__(self, office_data):
        self.type = office_data["office_type"]
        self.name = office_data["office_name"]
        
    def create_office(self):
        try:
            dict_info = { "type": self.type, "name": self.name }
            GeneralModelMethods.create_item(offices, dict_info)
            return dict_info
        except Exception:
            return False

    @staticmethod
    def get_all_offices():
        return offices

    # gets single items from the list of offices with ID office_id
    # queries the GeneralModelMethods to find the item
    @staticmethod
    def get_single_office(office_id):
        return GeneralModelMethods.get_single_item(offices, office_id)
 