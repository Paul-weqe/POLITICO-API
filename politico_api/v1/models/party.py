from random import randint
import sys
sys.path.insert(0,'../../')

from politico_api.v1.models.model_functions import GeneralModelMethods

parties = [

]

# finds out if a particular ID already exists in a list of items deeming it unusable. Searches the 'list_to_search' for the 'id_number'
# returns True if the ID number does not exist and False if the ID number exists

class PartyModel:

    def __init__(self, party_data):
        self.party_name = party_data["party_name"]
        self.hq_address = party_data["party_hq_address"]
        self.logo_url = party_data["party_logo_url"]
        self.members = party_data["party_members"]
        self.motto = party_data["party_motto"]

    def createParty(self):
        new_party_info = {
            "name": self.party_name, "hqAddress": self.hq_address, "logoUrl": self.logo_url, "motto": self.motto, "members": self.members
        }
        created_party = GeneralModelMethods.create_item(parties, new_party_info)
        if created_party != None:
            return { "id": created_party["id"], "name": created_party["name"]}
        return None 

    @staticmethod
    def get_all_parties():
        return parties
    
    @staticmethod
    def get_single_party(party_id):
        return GeneralModelMethods.get_single_item(parties, party_id)

    @staticmethod
    def edit_party(party_id, party_name):
        return GeneralModelMethods.edit_single_item(parties, party_id, "name", party_name)
    
    @staticmethod
    def delete_party(party_id):
        return GeneralModelMethods.delete_item(parties, party_id)
