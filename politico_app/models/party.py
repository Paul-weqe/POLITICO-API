from random import randint
import sys
sys.path.insert(0,'../../')

from politico_app.models.model_functions import GeneralModelMethods

parties = [

]

# finds out if a particular ID already exists in a list of items deeming it unusable. Searches the 'list_to_search' for the 'id_number'
# returns True if the ID number does not exist and False if the ID number exists

class PartyModel:

    def __init__(self, party_name, hq_address, logo_url, members, motto):
        self.party_name = party_name
        self.hq_address = hq_address
        self.logo_url = logo_url
        self.members = members
        self.motto = motto

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

parties += [
    {
        "id": 1, "name": "Party 1", "hqAddress": "Nairobi", "logoUrl": "https://martialartsworldnews.com/wp-content/uploads/2015/11/1.jpg", "motto": "We are one", "members": 2000,
    },
    {
        "id": 2, "name": "Party 2", "hqAddress": "Mombasa", "logoUrl": "https://www.michels.ca/ckfinder/userfiles/images/number2tm.png", "motto": "we are two", "members": 2500,
    },
    {
        "id": 3, "name": "Party 3", "hqAddress": "Kisumu", "logoUrl": "https://vignette.wikia.nocookie.net/opartshunter/images/7/79/3.jpg/revision/latest?cb=20130603053056", "motto": "we are three", "members": 3000,
    }
]