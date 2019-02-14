parties = {

}

# finds out if a particular ID already exists in a list of items deeming it unusable. Searches the 'list_to_search' for the 'id_number'
# returns True if the ID number does not exist and False if the ID number exists

class PartyModel:

    def __init__(self, party_data=None):
        if party_data != None:
            self.party_name = party_data["party_name"]
            self.hq_address = party_data["party_hq_address"]
            self.logo_url = party_data["party_logo_url"]
            self.members = party_data["party_members"]
            self.motto = party_data["party_motto"]
    
    def createParty(self):
        new_party_info = {
            "name": self.party_name, "hqAddress": self.hq_address, "logoUrl": self.logo_url, "motto": self.motto, "members": self.members
        }
        id = len(parties) + 1
        new_party_info["id"] = id
        parties[id] = new_party_info
        return new_party_info
    
    def get_all_parties(self):
        all_parties = []
        for party in parties:
            all_parties.append(parties[party])
        return all_parties
    
    
    def get_single_party(self, party_id):
        if party_id in parties:
            return parties[party_id]
        return None 

    def edit_party(self, party_id, party_name):
        if party_id in parties:
            parties[party_id]["name"] = party_name
            return parties[party_id]
        return False

    def delete_party(self, party_id):
        if party_id in parties:
            del parties[party_id]
            return True
        return False
